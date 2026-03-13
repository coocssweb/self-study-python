def fib_yield(n):
    a, b = 0, 1
    for _ in range(n):
        yield a            # 给你一个，然后"暂停"在这里
        a, b = b, a + b 

print(*fib_yield(10))