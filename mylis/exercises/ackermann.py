"""This module contains a code example related to

Think Python, 2nd Edition
by Allen Downey
http://thinkpython2.com

Copyright 2015 Allen Downey

License: http://creativecommons.org/licenses/by/4.0/
"""

def ackermann(m, n):
    """Computes the Ackermann function A(m, n)

    See http://en.wikipedia.org/wiki/Ackermann_function

    n, m: non-negative integers
    """
    global calls
    calls += 1
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))


if __name__ == '__main__':

    # NOTE:
    # Clear the cache before each iteration to avoid
    # cached results from previous iterations affecting
    # the counting of calls.

    import sys, functools

    if len(sys.argv) > 1:
        ackermann = functools.cache(ackermann)

    for m in range(0, 5):
        for n in range(0, 10):
            if hasattr(ackermann, 'cache_clear'):
                ackermann.cache_clear()
            calls = 0
            try:
                res = ackermann(m, n)
            except RecursionError:
                res = '...'
            print(f'A({m}, {n}) = {res:>4}\t[{calls:,.0f} calls]')

    if len(sys.argv) == 1:
        print(f'To enable caching, pass the "c" command-line option.')
