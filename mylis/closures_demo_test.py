"""

# EXAMPLES: CLOSURE VARIABLE NOT UPDATED

The `make_inc` and `make_inc2` functions have a closure
enclosing a `step` variable that is never updated:

    >>> inc3 = make_inc(3)
    >>> inc3(5)
    8
    >>> inc10 = make_inc_anon(10)
    >>> inc10(8)
    18
    >>> inc100 = make_inc_anon(100)
    >>> inc100(8)
    108
"""

def make_inc(step):
    def inc(n):
        return n + step
    return inc


def make_inc_anon(step):
    return lambda n: n + step


__doc__ += """

Let's inspect the closure:

    >>> dir(inc10)  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    ['__annotations__', '__builtins__', '__call__', '__class__',
     '__closure__', '__code__', '__defaults__', ...]
    >>> inc10.__closure__  # doctest: +ELLIPSIS
    (<cell at 0x...: int object at 0x...>,)
    >>> dir(inc10.__closure__[0])  # doctest: +ELLIPSIS
    ['__class__', ..., 'cell_contents']
    >>> inc10.__closure__[0].cell_contents
    10

`10` is the value, but to find the corresponding variable we need
to check the `__code__` object of the function.

    >>> inc10.__code__  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    <code object <lambda> at 0x..., file "...", line ...>
    >>> dir(inc10.__code__)  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    ['__class__', ..., 'co_argcount', ..., 'co_code', ...
     'co_freevars', 'co_kwonlyargcount', ... 'co_nlocals', ...
     'co_varnames'...]
    >>> inc10.__code__.co_varnames
    ('n',)
    >>> inc10.__code__.co_freevars
    ('step',)


The code object is the same for every function made by the same
function factory:

    >>> inc10.__code__ is inc100.__code__
    True


Now `make-inc` in Scheme:

```
(define (make-inc step)
    (lambda (n) (+ n step)))
```

Similar to this in Python:

```
def make_inc(step):
    return lambda n: n + step
```

Using the Scheme version of `make_inc`:

```
(define inc10 (make-inc 10))
(inc10 8)
18
```

Testing it:

    >>> inc_demo_src = '''
    ... (define (make-inc step)
    ...     (lambda (n) (+ n step)))
    ... (define inc10 (make-inc 10))
    ... (inc10 8)
    ... '''
    >>> from mylis import run
    >>> run(inc_demo_src)
    18


## EXAMPLES: CLOSURE VARIABLES UPDATED

The `make_averager` function (below) has a closure enclosing
two variables that need to be updated, `count` and `total`:

    >>> avg = make_averager()
    >>> avg(10)
    10.0
    >>> avg(11)
    10.5
    >>> avg(12)
    11.0

"""

def make_averager():
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    return averager


__doc__ += """

Now `make-averager` in Scheme:

```
(define (make-averager)
    (define count 0)
    (define total 0)
    (lambda (new-value)
        (set! count (+ count 1))
        (set! total (+ total new-value))
        (/ total count)))
```

Testing it:

    >>> avg_demo_src = '''
    ... (define (make-averager)
    ...     (define count 0)
    ...     (define total 0)
    ...     (lambda (new-value)
    ...         (set! count (+ count 1))
    ...         (set! total (+ total new-value))
    ...         (/ total count)))
    ... (define avg (make-averager))
    ... (avg 10)
    ... (avg 11)
    ... (avg 12)
    ... '''
    >>> run(avg_demo_src)
    11.0

"""
