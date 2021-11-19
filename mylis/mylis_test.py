import io

from pytest import mark, raises

from evaluator import standard_env, evaluate
from parser import s_expr, parse

from mylis import (
    env_from_args, run_file,
    multiline_input, multiline_repl, QuitRequest)

from mytypes import Expression, UnexpectedCloseParen

from dialogue import Dialogue, normalize

############### enhanced and new built-ins

@mark.parametrize('obj, expected', [
    (0, '0'),
    (1, '1'),
    (False, '#f'),
    (True, '#t'),
    (1.5, '1.5'),
    ('sin', 'sin'),
    (['+', 1, 2], '(+ 1 2)'),
    (['if', ['<', 'a', 'b'], True, False], '(if (< a b) #t #f)'),
    ([], '()'),
    (None, 'None'),
    (..., 'Ellipsis'),
])
def test_s_expr(obj: object, expected: str) -> None:
    got = s_expr(obj)
    assert got == expected


@mark.parametrize('source, expected', [
    ('(+ 1 2)', 3),
    ('(+ 1)', 1),
    ('(+ 1 2 3)', 6),
    ('(+)', 0),
])
def test_add(source: str, expected: Expression) -> None:
    got = evaluate(parse(source), standard_env())
    assert got == expected


@mark.parametrize('source, expected', [
    ('(- 5 2)', 3),
    ('(- 7)', -7),
    ('(- 4 3 2 1)', -2),
])
def test_sub(source: str, expected: Expression) -> None:
    got = evaluate(parse(source), standard_env())
    assert got == expected


@mark.parametrize('source, expected', [
    ('(* 5 2)', 10),
    ('(* 1 2 3 4 5)', 120),
    ('(*)', 1),
])
def test_mul(source: str, expected: Expression) -> None:
    got = evaluate(parse(source), standard_env())
    assert got == expected


@mark.parametrize('source, expected', [
    ('(/ 6 2)', 3),
    ('(/ 2)', .5),
    ('(/ 60 5 4 3 2)', .5),
])
def test_truediv(source: str, expected: Expression) -> None:
    got = evaluate(parse(source), standard_env())
    assert got == expected


@mark.parametrize('source, expected', [
    ('(/ 6 2)', 3),
    ('(/ 2)', .5),
    ('(/ 60 5 4 3 2)', .5),
])
def test_truediv(source: str, expected: Expression) -> None:
    got = evaluate(parse(source), standard_env())
    assert got == expected


@mark.parametrize('source, expected', [
    ('(= 3 3)', True),
    ('(= 1 3)', False),
    ('(= 2 2 2)', True),
    ('(= 2 2 1)', False),
])
def test_op_eq(source: str, expected: Expression) -> None:
    got = evaluate(parse(source), standard_env())
    assert got == expected


@mark.parametrize('source, expected', [
    ('(< 3 3)', False),
    ('(< 1 3)', True),
    ('(< 1 2 2)', False),
    ('(< 1 2 3)', True),
    ('(<= 3 3)', True),
    ('(<= 1 3)', True),
    ('(<= 1 2 2)', True),
    ('(<= 1 2 3)', True),
    ('(<= 1 2 1)', False),
    ('(> 3 3)', False),
    ('(> 3 1)', True),
    ('(> 2 1 2)', False),
    ('(> 3 2 1)', True),
    ('(>= 3 1)', True),
    ('(>= 1 3)', False),
    ('(>= 3 2 1)', True),
    ('(>= 3 2 2)', True),
    ('(>= 2 1 2)', False),
])
def test_variadic_comparison(source: str, expected: Expression) -> None:
    got = evaluate(parse(source), standard_env())
    assert got == expected


############### multi-line REPL


@mark.parametrize("session, result", [
    ("""
     1|3
     """, '3'),
    ("""
     1|(a
     2| b)
     """, '(a\n b)'),
])
def test_multiline_input(capsys, session, result):
    dlg = Dialogue(session)
    got = multiline_input('1|', '2|', input_fn=dlg.fake_input)
    assert result == got
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)


@mark.parametrize("session", [
    """
    >Q
    """,
])
def test_multiline_input_quit(session):
    dlg = Dialogue(session)
    with raises(QuitRequest):
        multiline_input('>', '', quit_cmd='Q', input_fn=dlg.fake_input)


@mark.parametrize("session, error_str", [
    ("""
     )
     """, ')'),
    ("""
     (a
      b))
     """, ' b))'),
    ("""
     (a
      very long line that will be cut))
     """, '…t will be cut))'),
])
def test_multiline_input_unexpected_close_paren(session, error_str):
    dlg = Dialogue(session)
    with raises(UnexpectedCloseParen) as excinfo:
        multiline_input('', '', input_fn=dlg.fake_input)
    want_msg = f'Unexpected close parenthesis: {error_str!r}'
    assert want_msg == str(excinfo.value)


def test_repl_quit(capsys):
    dlg = Dialogue('> .q\n')
    multiline_repl(input_fn=dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)


@mark.parametrize("session", [
    """
    >
    > .q
    """,
    """
    > (
    ... .q
    """,
    """
    > 3
    3
    > .q
    """,
])
def test_repl_quit_other_cases(capsys, session):
    dlg = Dialogue(session)
    multiline_repl(input_fn=dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)


def test_repl_gcd_example(capsys):
    session = """
    > (define (mod m n) (- m (* n (quotient m n))))
    > (define (gcd a b) (if (= b 0) a (gcd b (mod a b))))
    > (gcd 84 210)
    42
    """
    dlg = Dialogue(session)
    multiline_repl(input_fn=dlg.fake_input)
    captured = capsys.readouterr()
    assert normalize(captured.out) == dlg.session


def test_repl_gcd_example_multiline(capsys):
    session = """
    > (define (mod m n)
    ... (- m (* n (quotient m n))))
    > (define (gcd a b)
    ... (if (= b 0)
    ...   a
    ...   (gcd b (mod a b))))
    > (gcd 84 210)
    42
    """
    dlg = Dialogue(session)
    multiline_repl(input_fn=dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)


# Note: flip-flop keeps state in a global variable
# `state` because lis.py has no `let` form, and there is
# no "maker" function surrounding the function.
# Contrast with make-counter in examples_test.py
# where each call to (make-counter) creates a new procedure
# with its own closure.
# Based on first set! example from
# R. Kent Dybvig--The Scheme Programming Language, Fourth Edition
# https://scheme.com/tspl4/binding.html#./binding:s28
def test_repl_flip_flop(capsys):
    session = """
    > (define flip-flop
    ... (begin
    ...   (define state #f)
    ...   (lambda ()
    ...     (set! state (not state))
    ...     state)))
    > (flip-flop)
    #t
    > (flip-flop)
    #f
    > (flip-flop)
    #t
    > (flip-flop)
    #f
    """
    dlg = Dialogue(session)
    multiline_repl(input_fn=dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)


############### command-line integration

@mark.parametrize("args, global_env", [
    ([], {}),
    (['x'], {}),
    (['a=2'], {'a': 2}),
    (['=', 'a=.5', 'flavor=banana', 'max=999', '=='],
     {'a': 0.5, 'flavor':'banana', 'max': 999}),
])
def test_env_from_args(args, global_env):
    got = env_from_args(args)
    assert got == global_env


def test_run_file(capsys):
    source = """
    (define (! n)
        (if (<= n 1)
            1
            (* n (! (- n 1)))))
    (display (! x))
    """
    file = io.StringIO(source)
    env = env_from_args(['x=5'])
    got = run_file(file, env)
    assert got is None
    captured = capsys.readouterr()
    assert captured.out == '120\n'
