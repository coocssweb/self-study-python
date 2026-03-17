# ============================================================
# 任务五：装饰器计时器 (纯 Python)
# ============================================================
# 难度: ⭐⭐
# 知识点: 装饰器, time.time(), functools.wraps
# ============================================================
#
# 要求:
# 1. 写一个 @timer 装饰器，自动打印函数执行时间
# 2. 用 functools.wraps 保留原函数名
# 3. 用它装饰两个函数:
#    - loop_sum(): 用 for 循环累加 1 到 1000000
#    - builtin_sum(): 用 sum(range(1000001))
# 4. 对比两种方式的耗时
#
# 提示:
# - 参考 python/02/01_def.py 里的装饰器部分
# - start = time.time() ... end = time.time()
# - 打印格式: "函数名 执行耗时: 0.0123秒"
# - functools.wraps(func) 让装饰后的函数保留原名
#
# 期望输出类似:
#   loop_sum 执行耗时: 0.0456秒
#   结果: 500000500000
#   builtin_sum 执行耗时: 0.0123秒
#   结果: 500000500000
# ============================================================

import time
import functools

# 在下面写你的代码 👇
def timer(func):
    """计时装饰器"""
    pass


@timer
def loop_sum():
    """用 for 循环累加"""
    pass


@timer
def builtin_sum_fn():
    """用内置 sum() 累加"""
    pass


if __name__ == "__main__":
    result1 = loop_sum()
    print(f"结果: {result1}\n")

    result2 = builtin_sum_fn()
    print(f"结果: {result2}")
