def fibonacci(count):
    a, b = 1, 1
    while count > 0:
        yield a
        a, b = b, a + b
        count -= 1
