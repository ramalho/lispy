import math

from mylis import run

def fact_rec(n):
    if n < 2:
        return 1
    return n * fact_rec(n - 1)

fact_src = """
{define [! n]
    (if (< n 2)
        1
        (* n (! (- n 1)))
    )
}
(! x)
"""
def test_factorial():
    x = 450
    got = run(fact_src, x=x)
    assert got == math.factorial(x)
    assert got == fact_rec(x)


def fact_tail_rec(n):
    return fact_iter(n, 1)

def fact_iter(n, product):
    if n < 2:
        return product
    return fact_iter(n - 1, n * product)

fact_tail_src = """
{define [! n]
    (factorial-iter n 1)}

{define [factorial-iter n product]
    (if (< n 2)
        product
        (factorial-iter (- n 1) (* n product)))}
(! x)
"""
def test_factorial_tail_rec():
    x = 1000
    got = run(fact_tail_src, x=x)
    assert got == math.factorial(x)
    # assert got == fact_tail_rec(x)  # can't handle x=1000


def gcd(m, n):
    if n == 0:
        return m
    return gcd(n, m % n)


gcd_src = """
{define [mod m n]
    (- m (* n (quotient m n)))}
{define [gcd m n]
    (if (= n 0)
        m
        (gcd n (mod m n)))}
(gcd a b)
"""
def test_gcd():
    a, b = 18, 45
    got = run(gcd_src, a=a, b=b)
    assert got == 9
    assert got == gcd(a, b)



def quicksort_lc(lst):
    """quicksort with list comprehensions"""
    if not lst:
        return lst
    else:
        pivot, *rest = lst
        return (
            quicksort_lc([x for x in rest if x < pivot])
            + [pivot] +
            quicksort_lc([x for x in rest if x >= pivot])
        )

def quicksort(lst):
    """quicksort with filter and lambda"""
    if not lst:
        return lst
    else:
        pivot, *rest = lst
        return (
            quicksort(list(filter(lambda x: x < pivot, rest)))
            + [pivot] +
            quicksort(list(filter(lambda x: x >= pivot, rest)))
        )

quicksort_src = """
{define [quicksort lst]
    {if (null? lst)
        lst
        {begin
            {define pivot (car lst)}
            {define rest (cdr lst)}
            (append
                (quicksort
                    (filter {lambda [x] (< x pivot)} rest))
                (list pivot)
                (quicksort
                    (filter {lambda [x] (>= x pivot)} rest)))
        }
    }
}
(quicksort numbers)
"""
def test_quicksort():
    data = [2, 1, 6, 3, 4, 0, 8, 9, 7, 5]
    want = sorted(data)
    got = run(quicksort_src, numbers=data)
    assert got == want
    assert quicksort(data) == want
    assert quicksort_lc(data) == want


# Example from Structure and Interpretation of Computer Programs
# https://mitpress.mit.edu/sites/default/files/sicp/full-text/sicp/book/node12.html

newton_src = """
{define [sqrt x]
    (sqrt-iter 1.0 x)}
{define [sqrt-iter guess x]
    (if (good-enough? guess x)
        guess
        (sqrt-iter (improve guess x) x))}
{define [good-enough? guess x]
    (< (abs (- (* guess guess) x)) 0.001)}
{define [improve guess x]
    (average guess (/ x guess))}
{define [average x y]
    (/ (+ x y) 2)}
(sqrt 123454321)
"""
def test_newton():
    got = run(newton_src)
    assert math.isclose(got, 11111)


closure_src = """
{define [make-adder increment]
    (lambda (x) (+ increment x))
}
{define inc (make-adder 8)}
(inc 34)
"""
def test_closure():
    got = run(closure_src)
    assert got == 42


closure_with_change_src = """
{define [make-counter]
    (define n 0)
    (lambda ()
        (set! n (+ n 1))
        n)
}
{define counter (make-counter)}
(counter)
(counter)
(counter)
"""
def test_closure_with_change():
    got = run(closure_with_change_src)
    assert got == 3
