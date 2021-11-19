# Mylis: a tiny Scheme interpreter

**Mylis** is derived from a Python 3.10
[fork](https://github.com/fluentpython/lispy/tree/main/original/py3.10) of Peter Norvig's
[**lis.py**](https://norvig.com/lispy.html),
adding some features for demonstration purposes.

## Interactive use

Running `mylis.py` without arguments opens a REPL.

**Mylis** has limited error handling.
Simple mistakes will crash the interpreter.

```
$ ./mylis.py
To exit type .q
▷  x
🚨  Undefined symbol: 'x'
▷  pi
3.141592653589793
▷  (/ pi 2)
1.5707963267948966
▷  (define (half x) (/ x 2))
▷  (cos (half pi))
6.123233995736766e-17
▷  (sin (half pi))
1.0
▷  (define (! n)
⋯    (if (< n 2)
⋯        1
⋯        (* n (! (- n 1)))
⋯    ))
▷  (! 5)
120
▷  (! 42)
1405006117752879898543142606244511569936384000000000
▷  .q
$
```

For longer experiments, use source files and
command-line arguments, as presented next.


## Command-line integration

You can run programs written in the supported Scheme subset from the
command-line, like this:

```
./mylis.py examples/fibo-seq.scm n=20
(1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765)

```

The `n=20` option creates an `n` global variable with the given value.

If you read [examples/fibo-seq.scm](examples/fibo-seq.scm)
you'see that the last line is:

```scheme
(display (fibo-seq n))
```

The `n` is not defined in the program,
so it must be given as a command-line argument: `n=...`

Any command-line option with the syntax `symbol=value`
will be interpreted as a global definition—with
the limitation that `value` must be an integer or a float:

```scheme
(define symbol value)
```

If you forget to provide a required argument,
the interpreter will make a suggestion
(but currently it stops at the first undefined variable found):

```
$ ./mylis.py examples/fibo-seq.scm
🚨  'n' was not defined.
    You can define it as an option:
    $ ./mylis.py examples/fibo-seq.scm n=<value>
$ ./mylis.py examples/fibo-seq.scm n=20
(1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765)

```

_LR_

São Paulo, August 15, 2021
