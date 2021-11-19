#!/usr/bin/env python3

################ mylis: Tiny Scheme Environment in Python 3.10
## Additional runtime support by Luciano Ramalho for lis.py by
## Peter Norvig (c) 2010-18; See http://norvig.com/lispy.html

import operator as op
import readline  # "unused" import to enable readline in input()
import sys
from collections.abc import Sequence, Iterator
from typing import Any, Protocol, Callable, NoReturn

import parser

from evaluator import Environment, standard_env, evaluate
from mytypes import Expression, UndefinedSymbol, UnexpectedCloseParen, EvaluatorException


################ non-interactive execution


def run_lines(source: str, env: Environment | None = None) -> Iterator[Any]:
    global_env = Environment({}, standard_env())
    if env is not None:
        global_env.update(env)
    tokens = parser.tokenize(source)
    while tokens:
        exp = parser.read_from_tokens(tokens)
        yield evaluate(exp, global_env)


def run(source: str, **env: Expression) -> Any:
    for result in run_lines(source, env):
        pass
    return result


############### multi-line REPL


class QuitRequest(Exception):
    """Signal to quit multi-line input."""


ELLIPSIS = '\N{HORIZONTAL ELLIPSIS}'


def raise_unexpected_paren(line: str) -> NoReturn:
    max_msg_len = 16
    if len(line) < max_msg_len:
        msg = line
    else:
        msg = ELLIPSIS + line[-(max_msg_len-1):]
    raise UnexpectedCloseParen(msg)


QUIT_COMMAND = '.q'
InputFn = Callable[[str], str]

def multiline_input(prompt1: str,
                    prompt2: str,
                    *,
                    quit_cmd: str = QUIT_COMMAND,
                    input_fn: InputFn = input) -> str:

    paren_cnt = 0
    lines = []
    prompt = prompt1
    while True:
        line = input_fn(prompt).rstrip()
        if line == quit_cmd:
            raise QuitRequest()
        for char in line:
            if char == '(':
                paren_cnt += 1
            elif char == ')':
                paren_cnt -= 1
            if paren_cnt < 0:
                raise_unexpected_paren(line)
        lines.append(line)
        prompt = prompt2
        if paren_cnt == 0:
            break

    return '\n'.join(lines)


def multiline_repl(prompt1: str = '> ',
                   prompt2: str = '... ',
                   error_mark: str = '***',
                   *,
                   quit_cmd: str = QUIT_COMMAND,
                   input_fn: InputFn = input) -> None:
    """Read-Eval-Print-Loop"""

    global_env = Environment({}, standard_env())

    print(f'To exit type {QUIT_COMMAND}', file=sys.stderr)

    while True:
        # ___________________________________________ Read
        try:
            source = multiline_input(prompt1, prompt2,
                                     quit_cmd=quit_cmd,
                                     input_fn=input_fn)
        except (EOFError, QuitRequest):
            break
        except UnexpectedCloseParen as exc:
            print(error_mark, exc)
            continue
        if not source:
            continue

        # ___________________________________________ Eval
        current_exp = parser.parse(source)
        try:
            result = evaluate(current_exp, global_env)
        except EvaluatorException as exc:
            print(error_mark, exc)
            continue

        # ___________________________________________ Print
        if result is not None:
            print(parser.s_expr(result))


############### command-line integration

class TextReader(Protocol):
    def read(self) -> str:
        ...


def run_file(source_file: TextReader, env: Environment | None = None) -> Any:
    source = source_file.read()
    return run(source, **env)


def env_from_args(args: Sequence[str]) -> Environment:
    env = {}
    for arg in (a for a in args if '=' in a):
        parts = arg.split('=')
        if len(parts) != 2 or not all(parts):
            continue
        name, val = parts
        try:
            atom = parser.parse_atom(val)
        except ValueError:
            continue
        env[name] = atom
    return env

############### main

PROMPT1 = '\N{WHITE RIGHT-POINTING TRIANGLE}  '
PROMPT2 = '\N{MIDLINE HORIZONTAL ELLIPSIS}    '
ERROR_MARK = '\N{POLICE CARS REVOLVING LIGHT} '


def repl():
    multiline_repl(PROMPT1, PROMPT2, ERROR_MARK)


def main(args: list[str]) -> None:
    if len(args) == 1:
        repl()
    else:
        arg_env = env_from_args(args[1:])
        with open(args[1]) as source_file:
            try:
                run_file(source_file, arg_env)
            except UndefinedSymbol as exc:
                key = exc.args[0]
                print(f'{ERROR_MARK} {key!r} was not defined.')
                cmd = ' '.join(args)
                print('    You can define it as an option:')
                print(f'    $ {cmd} {key}=<value>')


if __name__ == '__main__':
    main(sys.argv)
