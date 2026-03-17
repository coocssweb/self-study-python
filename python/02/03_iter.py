# ============================================================
# Python 迭代器 (Iterator) 完整知识点
# ============================================================

# ---- 核心概念 ----
# 可迭代对象 (Iterable): 能用 for 循环遍历的东西，如 list, str, dict, set, tuple, range
# 迭代器 (Iterator): 带有 __next__() 方法的对象，每次调用返回下一个值，没了就抛 StopIteration
# 关系: 可迭代对象 通过 iter() 得到 迭代器


# 1. iter() 和 next() — 最基础的用法
print("1. iter() 和 next():")
nums = [10, 20, 30]
it = iter(nums)          # 从列表获取迭代器

print("  ", next(it))    # 10
print("  ", next(it))    # 20
print("  ", next(it))    # 30
# next(it)               # 再调用就会抛 StopIteration


# 2. for 循环的本质 — 就是在用迭代器
# for x in nums:  等价于:
print("2. for 循环的本质:")
it = iter(nums)
while True:
    try:
        x = next(it)
        print("  ", x)
    except StopIteration:
        break


# 3. 自定义迭代器 — 实现 __iter__ 和 __next__
print("3. 自定义迭代器 (倒计时):")

class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self  # 迭代器返回自身

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

for n in Countdown(5):
    print("  ", n, end="")
print()


# 4. 生成器就是迭代器的简写
print("4. 生成器 vs 自定义迭代器:")

# 上面的 Countdown 用生成器写只需要:
def countdown(start):
    while start > 0:
        yield start
        start -= 1

print("  ", list(countdown(5)))


# 5. 生成器表达式 (类似列表推导式，但用圆括号，惰性求值)
print("5. 生成器表达式:")

squares_list = [x ** 2 for x in range(5)]   # 列表推导 — 立刻算完，占内存
squares_gen = (x ** 2 for x in range(5))    # 生成器表达式 — 惰性，省内存

print("   列表推导:", squares_list)
print("   生成器:", list(squares_gen))       # 用 list() 消费掉
print("   类型对比:", type(squares_list), type(squares_gen))


# 6. 迭代器是一次性的!
print("6. 迭代器是一次性的:")

gen = (x for x in [1, 2, 3])
print("   第一次:", list(gen))   # [1, 2, 3]
print("   第二次:", list(gen))   # [] — 已经耗尽了!

# 列表可以反复遍历，因为每次 for 都会调用 iter() 创建新迭代器
# 迭代器的 __iter__ 返回自身，所以用完就没了


# 7. itertools — 迭代器工具箱 (标准库，非常实用)
import itertools

print("7. itertools 常用工具:")

# 7.1 chain — 把多个可迭代对象串起来
print("   chain:", list(itertools.chain([1, 2], [3, 4], [5])))

# 7.2 islice — 对迭代器切片 (迭代器不能用 [1:3] 这种语法)
print("   islice:", list(itertools.islice(range(100), 5, 10)))

# 7.3 count — 无限计数器
counter = itertools.count(start=1, step=2)  # 1, 3, 5, 7, ...
print("   count:", [next(counter) for _ in range(5)])

# 7.4 cycle — 无限循环
colors = itertools.cycle(["红", "绿", "蓝"])
print("   cycle:", [next(colors) for _ in range(7)])

# 7.5 repeat — 重复
print("   repeat:", list(itertools.repeat("嗨", 3)))

# 7.6 zip_longest — 不等长也能 zip
from itertools import zip_longest
a = [1, 2, 3]
b = ["a", "b"]
print("   zip:        ", list(zip(a, b)))              # 短的截断
print("   zip_longest:", list(zip_longest(a, b, fillvalue="?")))  # 用 ? 填充


# 7.7 product — 笛卡尔积 (嵌套循环的替代)
print("   product:", list(itertools.product("AB", [1, 2])))
# 等价于: [(a,b) for a in "AB" for b in [1,2]]

# 7.8 permutations — 排列
print("   permutations:", list(itertools.permutations("ABC", 2)))

# 7.9 combinations — 组合
print("   combinations:", list(itertools.combinations("ABC", 2)))

# 7.10 groupby — 分组 (数据需要先排序!)
data = [("水果", "苹果"), ("水果", "香蕉"), ("蔬菜", "白菜"), ("蔬菜", "萝卜")]
print("   groupby:")
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"     {key}: {[item[1] for item in group]}")


# 8. 内置函数中的迭代器用法
print("8. 内置函数配合迭代器:")

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map — 对每个元素应用函数 (返回迭代器)
print("   map:", list(map(lambda x: x * 2, nums)))

# filter — 过滤 (返回迭代器)
print("   filter:", list(filter(lambda x: x % 2 == 0, nums)))

# enumerate — 带索引遍历
print("   enumerate:")
for i, v in enumerate(["a", "b", "c"], start=1):
    print(f"     第{i}个: {v}")

# zip — 并行遍历
names = ["小明", "小红", "小刚"]
scores = [90, 85, 95]
print("   zip:", dict(zip(names, scores)))

# any / all — 短路判断
print("   any:", any(x > 5 for x in nums))   # 有一个满足就 True
print("   all:", all(x > 0 for x in nums))   # 全部满足才 True

# sum / min / max 也接受迭代器
print("   sum:", sum(x ** 2 for x in range(5)))  # 不需要先建列表


# 9. iter() 的双参数形式 (冷门但有用)
print("9. iter(callable, sentinel):")
import random
random.seed(42)

# iter(函数, 哨兵值): 不断调用函数，直到返回值等于哨兵值就停止
# 模拟: 不断掷骰子，直到掷出 6
rolls = list(iter(lambda: random.randint(1, 6), 6))
print("   掷到6之前:", rolls)


# 10. yield from — 委托生成器 (简化嵌套 yield)
print("10. yield from:")

def flatten(nested):
    """把嵌套列表展平"""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)  # 递归委托
        else:
            yield item

data = [1, [2, 3], [4, [5, 6]], 7]
print("   展平:", list(flatten(data)))


# 11. 无限迭代器 + takewhile/dropwhile
print("11. takewhile / dropwhile:")

from itertools import takewhile, dropwhile

nums = [1, 3, 5, 7, 2, 4, 6]
# takewhile: 从头开始取，条件不满足就停
print("   takewhile(<6):", list(takewhile(lambda x: x < 6, nums)))
# dropwhile: 从头开始丢，条件不满足就开始取
print("   dropwhile(<6):", list(dropwhile(lambda x: x < 6, nums)))


# ============================================================
# 总结: 迭代器知识图谱
# ============================================================
# 基础: iter(), next(), for 循环本质, StopIteration
# 核心: __iter__ + __next__ 自定义迭代器
# 简写: 生成器函数 (yield), 生成器表达式 (x for x in ...)
# 陷阱: 迭代器是一次性的
# 工具: itertools (chain, islice, count, cycle, product, groupby...)
# 内置: map, filter, enumerate, zip, any, all
# 进阶: yield from, iter(callable, sentinel)
# ============================================================
