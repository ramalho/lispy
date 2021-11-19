#!/usr/bin/env python3

################ lis.py: Scheme Interpreter in Python 3.10
## (c) Peter Norvig, 2010-18; See http://norvig.com/lispy.html
## Minor edits for Fluent Python, Second Edition (O'Reilly, 2021)
## by Luciano Ramalho, adding type hints and pattern matching.

################ imports and types
import functools as ft
import itertools as it
import math
import operator as op
from collections import ChainMap
from collections.abc import MutableMapping
from typing import Any, TypeAlias

from mytypes import (
    Expression, Symbol,
    UndefinedSymbol, InvalidSyntax, EvaluatorException,
)

import parser

TCO_ENABLED = True


class Environment(ChainMap):
    "A ChainMap that allows updating an item in-place."

    def change(self, key: Symbol, value: object) -> None:
        "Find where key is defined and change the value there."
        for map in self.maps:
            if key in map:
                map[key] = value
                return
        raise KeyError(key)


class Procedure:
    "A user-defined Scheme procedure."

    def __init__(
        self, parms: list[Symbol], body: list[Expression], env: Environment
    ):
        self.parms = parms
        self.body = body
        self.definition_env = env

    def application_env(self, args: list[Expression]) -> Environment:
        local_env = dict(zip(self.parms, args))
        return Environment(local_env, self.definition_env)

    def __call__(self, *args: Expression) -> Any:
        env = self.application_env(args)
        for exp in self.body:
            result = evaluate(exp, env)
        return result


################ global environment

def display(obj: object) -> str:
    output = parser.s_expr(obj)
    print(output)


def variadic_sub(first, *rest):
    if rest:
        return first - sum(rest)
    else:
        return -first


def variadic_truediv(first, *rest):
    if rest:
        return first / math.prod(rest)
    else:
        return 1 / first


def variadic_comparison(op, current, *rest):
    for arg in rest:
        if not op(current, arg):
            return False
        current = arg
    return True


def standard_env() -> Environment:
    "An environment with some Scheme standard procedures."
    env = Environment()
    env.update(vars(math))   # sin, cos, sqrt, pi, ...
    env.update({
        '#f': False,
        '#t': True,
        '+':  lambda *args: sum(args),
        '-':  variadic_sub,
        '*':  lambda *args: math.prod(args),
        '/':  variadic_truediv,
        'quotient': op.floordiv,
        '=':  lambda first, *rest: all(first == x for x in rest),
        '<':  ft.partial(variadic_comparison, op.lt),
        '>':  ft.partial(variadic_comparison, op.gt),
        '<=': ft.partial(variadic_comparison, op.le),
        '>=': ft.partial(variadic_comparison, op.ge),
        'abs': abs,
        'append': lambda *args: list(it.chain(*args)),
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'display': display,
        'eq?': op.is_,
        'equal?': op.eq,
        'filter': lambda *args: list(filter(*args)),
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map': lambda *args: list(map(*args)),
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, (int, float)),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env


################ special forms

def cond_form(clauses: list[Expression], env: Environment) -> Any:
    "Special form: (cond (test exp)* (else eN)?)."
    for clause in clauses:
        match clause:
            case ['else', *body]:
                for exp in body:
                    result = evaluate(exp, env)
                return result
            case [test, *body] if evaluate(test, env):
                for exp in body:
                    result = evaluate(exp, env)
                return result


def or_form(expressions: list[Expression], env: Environment) -> Any:
    "Special form: (or exp*)"
    value = False
    for exp in expressions:
        value = evaluate(exp, env)
        if value:
            return value
    return value


def and_form(expressions: list[Expression], env: Environment) -> Any:
    "Special form: (and exp*)"
    value = True
    for exp in expressions:
        value = evaluate(exp, env)
        if not value:
            return value
    return value

################ eval

KEYWORDS_1 = ['quote', 'if', 'define', 'lambda']
KEYWORDS_2 = ['set!', 'cond', 'or', 'and', 'begin']
KEYWORDS = KEYWORDS_1 + KEYWORDS_2

# Quantifiers in syntax descriptions:
#   * : 0 or more
#   + : 1 or more
#   ? : 0 or 1

def evaluate(exp: Expression, env: Environment) -> Any:
    "Evaluate an expression in an environment."
    while True:
        match exp:
            case int(x) | float(x):                             # number literal
                return x
            case Symbol(var):                                   # variable reference
                try:
                    return env[var]
                except KeyError as exc:
                    raise UndefinedSymbol(var) from exc
            case ['quote', exp]:                                # (quote exp)
                return exp
            case ['if', test, consequence, alternative]:        # (if test consequence alternative)
                if evaluate(test, env):
                    exp = consequence
                else:
                    exp = alternative
            case ['define', Symbol(var), value_exp]:            # (define var exp)
                env[var] = evaluate(value_exp, env)
                return
            case ['set!', Symbol(var), value_exp]:              # (set! var exp)
                env.change(var, evaluate(value_exp, env))
                return
            case ['define', [Symbol(name), *parms], *body       # (define (name parm*)) body+)
                ] if len(body) > 0:
                env[name] = Procedure(parms, body, env)
                return
            case ['lambda', [*parms], *body] if len(body) > 0:  # (lambda (parm*) body+)
                return Procedure(parms, body, env)
            case ['cond', *clauses]:                            # (cond (t1 e1)* (else eN)?)
                return cond_form(clauses, env)
            case ['or', *expressions]:                          # (or exp*)
                return or_form(expressions, env)
            case ['and', *expressions]:                         # (and exp*)
                return and_form(expressions, env)
            case ['begin', *expressions]:                       # (begin exp+)
                for exp in expressions[:-1]:
                    evaluate(exp, env)
                exp = expressions[-1]
            case [op, *args] if op not in KEYWORDS:             # (proc exp*)
                proc = evaluate(op, env)
                values = [evaluate(arg, env) for arg in args]
                if TCO_ENABLED and isinstance(proc, Procedure):
                     exp = ['begin', *proc.body]
                     env = proc.application_env(values)
                else:
                    try:
                        return proc(*values)
                    except TypeError as exc:
                        source = parser.s_expr(exp)
                        msg = (f'{exc!r}\ninvoking: {proc!r}({args!r}):'
                               f'\nsource: {source}\nAST: {exp!r}')
                        raise EvaluatorException(msg) from exc
            case _:
                source = parser.s_expr(exp)
                raise InvalidSyntax(source)
