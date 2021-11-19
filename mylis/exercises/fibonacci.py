import math


def fibonacci_gen():
    """Idiomatic Fibonacci sequence generator"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def fibonacci_round(n):
    """This works only for n<=70 with 64 bit floats"""
    assert n <= 70, 'Not enough precision for n >= 70'
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    return round(phi ** n / sqrt5)


if __name__ == '__main__':

    for i, fg in zip(range(100), fibonacci_gen()):
        fr = fibonacci_round(i)
        print(f'{i:3}\t{fr}\t{fr - fg}')
