from typing import Any, TypeAlias

from mytypes import (Symbol, Atom, Expression, UnexpectedCloseParen, UnexpectedEndOfSource)


BRACKETS = {
    '(': ')',
    '[': ']',
    '{': '}',
}


def parse(source: str) -> Expression:
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(source))


def tokenize(s: str) -> list[str]:
    "Convert a string into a list of tokens."
    for left, right in BRACKETS.items():
        s = s.replace(left, f' {left} ').replace(right, f' {right} ')
    return s.split()


def read_from_tokens(tokens: list[str]) -> Expression:
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise UnexpectedEndOfSource()
    token = tokens.pop(0)
    close_bracket = None
    if token in BRACKETS:
        close_bracket = BRACKETS[token]
        exp = []
        while tokens and tokens[0] != close_bracket:
            exp.append(read_from_tokens(tokens))
        if not tokens:
            raise UnexpectedEndOfSource()
        tokens.pop(0)  # discard ')'
        return exp
    elif token in BRACKETS.values():
        raise UnexpectedCloseParen()
    else:
        return parse_atom(token)


def parse_atom(token: str) -> Atom:
    "Numbers become numbers; every other token is a symbol."
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def s_expr(obj: object) -> str:
    """Convert Python object into Lisp s-expression.

    This is the inverse function of `parse()`"""
    match obj:
        case True:
            return '#t'
        case False:
            return '#f'
        case list(obj):
            items = ' '.join(s_expr(x) for x in obj)
            return f'({items})'
        case Symbol(x):
            return x
        case _:
            return repr(obj)