# ============================================================
# Python 函数 (def) 完整知识点
# ============================================================

# 1. 基础函数定义
def add(a, b):
    return a + b

print("1. 基础函数:", add(1, 2))


# 2. 默认参数
def greet(name, greeting="你好"):
    return f"{greeting}, {name}!"

print("2. 默认参数:", greet("小明"))
print("2. 覆盖默认:", greet("小明", "嗨"))


# 3. 关键字参数 (调用时指定参数名，顺序随意)
def user_info(name, age, city):
    return f"{name}, {age}岁, 来自{city}"

print("3. 关键字参数:", user_info(age=25, city="北京", name="小红"))


# 4. *args — 可变位置参数 (接收任意数量的位置参数，打包成元组)
def sum_all(*args):
    return sum(args)

print("4. *args:", sum_all(1, 2, 3, 4, 5))


# 5. **kwargs — 可变关键字参数 (接收任意数量的关键字参数，打包成字典)
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"   {key} = {value}")

print("5. **kwargs:")
print_info(name="小明", age=25, lang="Python")


# 6. 参数顺序规则: 普通参数 → *args → 关键字参数 → **kwargs
def full_example(a, b, *args, key="默认值", **kwargs):
    print(f"   a={a}, b={b}")
    print(f"   args={args}")
    print(f"   key={key}")
    print(f"   kwargs={kwargs}")

print("6. 参数顺序规则:")
full_example(1, 2, 3, 4, key="自定义", x=10, y=20)


# 7. 仅限关键字参数 (* 后面的参数必须用关键字传递)
def keyword_only(a, b, *, mode, verbose=False):
    if verbose:
        print(f"   mode={mode}")
    return a + b if mode == "add" else a - b

print("7. 仅限关键字参数:", keyword_only(10, 3, mode="add"))
# keyword_only(10, 3, "add")  # 这样会报错!


# 8. 仅限位置参数 (/ 前面的参数只能按位置传递, Python 3.8+)
def pos_only(a, b, /, c):
    return a + b + c

print("8. 仅限位置参数:", pos_only(1, 2, c=3))
# pos_only(a=1, b=2, c=3)  # 这样会报错!


# 9. 多返回值 (本质是返回元组)
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 4, 1, 5, 9])
print(f"9. 多返回值: 最小={lo}, 最大={hi}")


# 10. 函数文档字符串 (docstring)
def calculate(a, b, operation="add"):
    """
    执行两个数的运算。

    Args:
        a: 第一个数
        b: 第二个数
        operation: 运算类型，支持 "add", "sub", "mul", "div"

    Returns:
        运算结果

    Raises:
        ValueError: 不支持的运算类型
    """
    ops = {"add": a + b, "sub": a - b, "mul": a * b, "div": a / b}
    if operation not in ops:
        raise ValueError(f"不支持的运算: {operation}")
    return ops[operation]

print("10. docstring:", calculate(6, 3, "mul"))
print("    查看文档:", calculate.__doc__[:20], "...")


# 11. 类型注解 (Type Hints, 不强制但提高可读性)
def divide(a: float, b: float) -> float:
    return a / b

print("11. 类型注解:", divide(10, 3))


# 12. lambda 匿名函数 (一行简单函数)
square = lambda x: x ** 2
print("12. lambda:", square(5))

# lambda 常用于排序
students = [("小明", 90), ("小红", 85), ("小刚", 95)]
students.sort(key=lambda s: s[1], reverse=True)
print("    lambda排序:", students)


# 13. 函数是一等公民 (可以赋值、传参、作为返回值)
def apply(func, value):
    return func(value)

print("13. 函数传参:", apply(square, 8))


# 14. 闭包 (内部函数引用外部函数的变量)
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)
print("14. 闭包: double(5)=", double(5), "triple(5)=", triple(5))


# 15. 装饰器 (本质是接收函数并返回新函数的高阶函数)
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"    {func.__name__} 耗时: {end - start:.4f}秒")
        return result
    return wrapper

@timer  # 等价于 slow_add = timer(slow_add)
def slow_add(a, b):
    time.sleep(0.1)
    return a + b

print("15. 装饰器:", slow_add(1, 2))


# 16. 带参数的装饰器
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def say_hi(name):
    return f"Hi, {name}"

print("16. 带参装饰器:", say_hi("小明"))


# 17. functools.wraps (保留被装饰函数的元信息)
from functools import wraps

def smart_timer(func):
    @wraps(func)  # 没有这个的话，函数名会变成 "wrapper"
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"    {func.__name__} 耗时: {time.time() - start:.4f}秒")
        return result
    return wrapper

@smart_timer
def my_func():
    """这是我的函数"""
    pass

print("17. wraps保留元信息:", my_func.__name__, my_func.__doc__)


# 18. 递归 (函数调用自身)
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print("18. 递归 5!=", factorial(5))


# 19. 生成器函数 (yield 代替 return，惰性求值，节省内存)
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print("19. 生成器:", list(fibonacci(10)))


# 20. 全局变量与 nonlocal
count = 0

def increment():
    global count  # 声明使用全局变量
    count += 1

increment()
increment()
print("20. global:", count)

def outer():
    x = 10
    def inner():
        nonlocal x  # 声明使用外层函数的变量
        x += 5
    inner()
    return x

print("    nonlocal:", outer())


# 21. 可变默认参数陷阱 (经典坑!)
# 错误写法 — 默认列表在函数定义时只创建一次，后续调用共享同一个对象
def bad_append(item, lst=[]):
    lst.append(item)
    return lst

print("21. 可变默认参数陷阱:")
print("    第一次:", bad_append(1))
print("    第二次:", bad_append(2))  # 输出 [1, 2] 而不是 [2]!

# 正确写法
def good_append(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print("    正确第一次:", good_append(1))
print("    正确第二次:", good_append(2))


# 22. 解包传参
def point(x, y, z):
    return f"({x}, {y}, {z})"

coords = [1, 2, 3]
print("22. *解包列表:", point(*coords))

config = {"x": 4, "y": 5, "z": 6}
print("    **解包字典:", point(**config))


# ============================================================
# 总结: 从基础到资深，def 的知识图谱
# ============================================================
# 基础: 定义、参数、返回值、默认参数
# 进阶: *args, **kwargs, 仅限关键字/位置参数, 类型注解
# 高级: 闭包, 装饰器, 生成器, 递归
# 陷阱: 可变默认参数
# 工程: docstring, functools.wraps, 解包传参
# ============================================================
