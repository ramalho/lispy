# Exercises doable with Mylis

## 1. Temperature converter

Write a function `c-to-f` to convert a temperature from Celsius to
Fahrenheit.

This is the formula using infix notation, which you'll need to rewrite in prefix notation:

`f = (9 / 5) * c + 32`

Some examples:

* 0°C is 32°F
* 20°C is 68°F
* 100°C is 212°F
* -20°C is -4°F

### Challenge 1.1

> **TIP**: The challenge exercises are optional. Do them if you have time and are motivated to learn more.

Write a function `f-to-c` to convert from Fahrenheit to Celsius.
The formula is:

`c = (f − 32) * 5 / 9`


### Challenge 2.2

After you make each of those functions work in the REPL,
turn each of them into a script using the trick
of having a top-level expression like `(display c-to-f c)`,
where `c` is not defined at the global level,
which will make the interpreter suggest that the user provide it.

See [`mylis/examples/fibo-n.scm`](https://github.com/fluentpython/lispy/blob/main/mylis/examples/fibo-n.scm)
for an example that does this:

```
$ ./mylis.py examples/fibo-n.scm
🚨  'n' was not defined.
    You can define it as an option:
    $ ./mylis.py examples/fibo-n.scm n=<value>
```

## 2. Fibonacci by rounding

In the [`mylis/examples`](https://github.com/fluentpython/lispy/tree/main/mylis/examples)
directory you'll find the
[`fibo-n.scm`](https://github.com/fluentpython/lispy/blob/main/mylis/examples/fibo-n.scm)
which given `n`, displays the N<sup>th</sup> number
in the Fibonacci sequence, starting at 0.

```
$ ./mylis.py examples/fibo-n.scm n=70
190392490709135
```

Write an alternative script, `fibo-round.scm` using the
[Computation by rounding](https://en.wikipedia.org/wiki/Fibonacci_number#Computation_by_rounding) formula.

A few examples:

* `n=0` → `0`
* `n=2` → `1`
* `n=10` → `55`
* `n=22` → `17711`

For reference, this Python code uses that formula:

```python
import math

def fibonacci_round(n):
    """This works only for n<=70 with 64 bit floats"""
    assert n <= 70, 'Not enough precision for n >= 70'
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    return round(phi ** n / sqrt5)
```

> **TIP**: In Mylis, Python's `math` functions are built-in, so you don't need to import them:
>
> ```
> ▷  (sqrt 5)
> 2.23606797749979
> ```

### Challenge 2.1

Note that the formula only works for `n <= 70`,
because of the limited precision of the 64-bit `float` type used in Python and Mylis.
Include a test to display an error message instead of the wrong value
if the user provides some `n > 70` in the command line.

>  **TIP**: The highly inefficient
  [fibo-rec.scm](https://github.com/fluentpython/lispy/blob/main/mylis/examples/fibo-rec.scm)
  example displays a message when `n >= 20` and proceeds to compute the number.
  In this exercise, we want to display a message but not compute the number if `n > 70`.

## 3. Ackermann function

Implement the Ackermann–Péter function.

The
[Ackermann function](http://en.wikipedia.org/wiki/Ackermann_function)
is a deeply recursive function from computability theory.
Besides its theoretical relevance, it has also been used to benchmark
"a compiler's ability to optimize recursion" according to its [Wikipedia article](http://en.wikipedia.org/wiki/Ackermann_function).

One of its variations, the Ackermann–Péter function,
can be coded in Python as:

```python
def ackermann(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))
```

The arguments `m` and `n` must non-negative integers.

In practice, they must be very small, especially the `m` parameter.
Computing A(3, 2) requires 541 calls to `ackermann`, and the result is 29.
Wikipedia says "A(4, 2) is an integer of 19,729 decimal digits."

In Python 3.10, the two largest combinations of `(m, n)` that
I could compute with the implementation above are:

* A(3, 6) = 509 (requires 172,233 calls)
* A(4, 0) = 13 (requires 107 calls)

Using memoization with `functools.cache`, the largest combinations are:

* A(3, 7) = 1021 (requires 2,558 calls)
* A(4, 0) = 13 (requires 33 calls)

See
[exercises/ackermann.py](https://github.com/fluentpython/lispy/blob/main/mylis/exercises/ackermann.py)
for a Python script that iterates over small values of `(m, n)` and
counts the number of calls required.

### Challenge 3.1

Write a script to compute the Ackermann function for A(m, n), with both m and n ranging from 0 to 3 inclusive.
The output would look like this:

```
((A 0 0) = 1)
((A 0 1) = 2)
((A 0 2) = 3)
((A 0 3) = 4)
((A 1 0) = 2)
((A 1 1) = 3)
((A 1 2) = 4)
((A 1 3) = 5)
((A 2 0) = 3)
((A 2 1) = 5)
((A 2 2) = 7)
((A 2 3) = 9)
((A 3 0) = 5)
((A 3 1) = 13)
((A 3 2) = 29)
((A 3 3) = 61)
```

### Challenge 3.2

Find out what are the maximum values for `(m, n)` that your program (or Mylis itself) can compute,
considering that computing A(3, 3) takes 2,432 recursive calls,
and Python itself can only go as high as A(3, 6) and A(4, 0)
without memoization or changing its default configuration with
[`sys.setrecursionlimit`](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit).


### Challenge 3.3

Implement memoization using nested lists—because Mylis has no `dict` type.
How high can you go then?

(Understanding what this means is part of the challenge ;-)

----

_LR_

São Paulo, August 9, 2021
