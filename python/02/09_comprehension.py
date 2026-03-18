# ============================================================
# Python 推导式与函数式编程技巧 (Comprehension & Functional)
# ============================================================

# ---- 为什么学这个? ----
# 你在前面的文件里零散见过列表推导式、lambda、map/filter
# 这里把它们系统整理一下，写出更 Pythonic 的代码

names = ["小明", "小红", "小刚"]
scores = [90, 85, 95]
ages = [18, 17, 19]
print(list(zip(names, scores, ages)))
for name, score, age in zip(names, scores, ages):
    print(f"   {name}: {score}分, {age}岁")


# # 1. 列表推导式 (List Comprehension)
# print("1. 列表推导式:")

# # 基础: [表达式 for 变量 in 可迭代对象]
# squares = [x ** 2 for x in range(6)]
# print("   平方:", squares)

# # 带条件: [表达式 for 变量 in 可迭代对象 if 条件]
# evens = [x for x in range(10) if x % 2 == 0]
# print("   偶数:", evens)

# # 带 if-else (注意位置不同!)
# labels = ["偶" if x % 2 == 0 else "奇" for x in range(6)]
# print("   奇偶:", labels)
# # if 在 for 后面 → 过滤
# # if-else 在 for 前面 → 转换


# # 2. 嵌套推导式
# print("\n2. 嵌套推导式:")

# # 二维展平
# matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# flat = [x for row in matrix for x in row]
# print("   展平:", flat)
# # 等价于:
# # for row in matrix:
# #     for x in row:
# #         flat.append(x)

# # 生成坐标对
# coords = [(x, y) for x in range(3) for y in range(3) if x != y]
# print("   坐标:", coords)

# # 矩阵转置
# transposed = [[row[i] for row in matrix] for i in range(3)]
# print("   转置:", transposed)


# # 3. 字典推导式 (Dict Comprehension)
# print("\n3. 字典推导式:")

# # {键表达式: 值表达式 for 变量 in 可迭代对象}
# names = ["小明", "小红", "小刚"]
# scores = [90, 85, 95]
# grade_book = {name: score for name, score in zip(names, scores)}
# print("   成绩:", grade_book)

# # 带条件
# passed = {k: v for k, v in grade_book.items() if v >= 90}
# print("   及格:", passed)

# # 键值互换
# inverted = {v: k for k, v in grade_book.items()}
# print("   互换:", inverted)

# # 从列表构建索引
# words = ["apple", "banana", "cherry"]
# index = {word: i for i, word in enumerate(words)}
# print("   索引:", index)


# # 4. 集合推导式 (Set Comprehension)
# print("\n4. 集合推导式:")

# # {表达式 for 变量 in 可迭代对象}  — 和字典推导式的区别是没有冒号
# text = "hello world"
# unique_chars = {c for c in text if c != " "}
# print("   去重字符:", sorted(unique_chars))

# # 实用: 提取所有文件扩展名
# files = ["a.py", "b.txt", "c.py", "d.json", "e.txt"]
# extensions = {f.rsplit(".", 1)[-1] for f in files}
# print("   扩展名:", extensions)


# # 5. 生成器表达式 (Generator Expression)
# print("\n5. 生成器表达式:")

# # 用圆括号 — 惰性求值，不会一次性占用内存
# gen = (x ** 2 for x in range(6))
# print("   类型:", type(gen))
# print("   list:", list(gen))

# # 直接传给函数时可以省略外层括号
# total = sum(x ** 2 for x in range(10))
# print("   sum:", total)

# # 对比内存占用
# import sys
# list_size = sys.getsizeof([x for x in range(10000)])
# gen_size = sys.getsizeof(x for x in range(10000))
# print(f"   列表占用: {list_size} 字节")
# print(f"   生成器占用: {gen_size} 字节")  # 小得多!


# # 6. 推导式 vs 循环 — 什么时候该用推导式?
# print("\n6. 推导式 vs 循环:")
# print("   推导式适合: 简单的映射/过滤，一两行能搞定的")
# print("   循环适合: 复杂逻辑、多步操作、需要 break/continue")
# print("   原则: 可读性优先，别写超过一行的推导式")

# # 反面教材 — 太复杂的推导式不如用循环
# # bad = [x if x > 0 else -x for xs in matrix for x in xs if isinstance(x, int)]
# # 这种就该老老实实写循环


# # 7. lambda 回顾与进阶
# print("\n7. lambda:")

# # 基础 (01_def.py 学过)
# add = lambda a, b: a + b
# print("   基础:", add(3, 5))

# # lambda 最常见的用途: 作为排序/过滤的 key
# students = [
#     {"name": "小明", "age": 18, "score": 90},
#     {"name": "小红", "age": 17, "score": 95},
#     {"name": "小刚", "age": 19, "score": 85},
# ]

# # 按成绩排序
# by_score = sorted(students, key=lambda s: s["score"], reverse=True)
# print("   按成绩:", [(s["name"], s["score"]) for s in by_score])

# # 多条件排序 (先按成绩降序，再按年龄升序)
# by_multi = sorted(students, key=lambda s: (-s["score"], s["age"]))
# print("   多条件:", [(s["name"], s["score"], s["age"]) for s in by_multi])


# # 8. map() — 对每个元素应用函数
# print("\n8. map():")

# nums = [1, 2, 3, 4, 5]

# # map 返回迭代器
# doubled = list(map(lambda x: x * 2, nums))
# print("   map:", doubled)

# # 多个可迭代对象
# sums = list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30]))
# print("   map多参:", sums)

# # 对比推导式 — 推导式通常更清晰
# doubled2 = [x * 2 for x in nums]
# print("   推导式:", doubled2)  # 推荐这种写法


# # 9. filter() — 过滤元素
# print("\n9. filter():")

# nums = range(10)

# # filter 返回迭代器
# evens = list(filter(lambda x: x % 2 == 0, nums))
# print("   filter:", evens)

# # filter(None, ...) — 过滤掉假值
# mixed = [0, 1, "", "hello", None, [], [1], False, True]
# truthy = list(filter(None, mixed))
# print("   filter(None):", truthy)

# # 对比推导式
# evens2 = [x for x in nums if x % 2 == 0]
# print("   推导式:", evens2)  # 同样推荐这种


# # 10. sorted() 进阶
# print("\n10. sorted() 进阶:")

# # 基础排序
# print("   基础:", sorted([3, 1, 4, 1, 5, 9]))
# print("   降序:", sorted([3, 1, 4, 1, 5, 9], reverse=True))

# # 按长度排序
# words = ["banana", "pie", "apple", "fig", "cherry"]
# print("   按长度:", sorted(words, key=len))

# # 按最后一个字母排序
# print("   按末字母:", sorted(words, key=lambda w: w[-1]))

# # 稳定排序: 相等元素保持原始顺序
# # Python 的 sort 是稳定的 (TimSort)

# # operator 模块 — 比 lambda 更快更清晰
# from operator import itemgetter, attrgetter

# pairs = [(1, "b"), (3, "a"), (2, "c")]
# print("   itemgetter:", sorted(pairs, key=itemgetter(1)))

# # 对字典列表排序
# print("   字典排序:", sorted(students, key=itemgetter("score"), reverse=True))


# # 11. reduce() — 累积计算
# print("\n11. reduce():")

# from functools import reduce

# # reduce(函数, 可迭代对象, 初始值)
# # 把列表"折叠"成一个值
# nums = [1, 2, 3, 4, 5]

# # 累加 (等价于 sum)
# total = reduce(lambda a, b: a + b, nums)
# print("   累加:", total)

# # 累乘
# product = reduce(lambda a, b: a * b, nums)
# print("   累乘:", product)

# # 找最大值 (等价于 max)
# biggest = reduce(lambda a, b: a if a > b else b, nums)
# print("   最大:", biggest)

# # 实用: 展平嵌套列表
# nested = [[1, 2], [3, 4], [5, 6]]
# flat = reduce(lambda a, b: a + b, nested)
# print("   展平:", flat)

# # 提示: 大多数情况下 sum/max/min 比 reduce 更清晰
# # reduce 适合没有内置函数对应的累积操作


# # 12. any() 和 all()
# print("\n12. any() 和 all():")

# nums = [2, 4, 6, 8, 10]

# # any — 任意一个为 True 就返回 True (短路)
# print("   any(>5):", any(x > 5 for x in nums))
# print("   any(>20):", any(x > 20 for x in nums))

# # all — 全部为 True 才返回 True (短路)
# print("   all(偶数):", all(x % 2 == 0 for x in nums))
# print("   all(>5):", all(x > 5 for x in nums))

# # 实用: 验证数据
# users = [
#     {"name": "小明", "age": 18},
#     {"name": "小红", "age": 17},
#     {"name": "", "age": 20},
# ]
# all_valid = all(u["name"] and u["age"] > 0 for u in users)
# has_minor = any(u["age"] < 18 for u in users)
# print(f"   全部有效: {all_valid}")
# print(f"   有未成年: {has_minor}")


# # 13. enumerate() 和 zip() 技巧
# print("\n13. enumerate 和 zip 技巧:")

# # enumerate 带起始值
# fruits = ["苹果", "香蕉", "橘子"]
# for i, fruit in enumerate(fruits, start=1):
#     print(f"   第{i}个: {fruit}")

# # zip 打包多个列表
# names = ["小明", "小红", "小刚"]
# scores = [90, 85, 95]
# ages = [18, 17, 19]
# for name, score, age in zip(names, scores, ages):
#     print(f"   {name}: {score}分, {age}岁")

# # zip 解包 (转置)
# pairs = [("a", 1), ("b", 2), ("c", 3)]
# letters, numbers = zip(*pairs)
# print("   解包:", letters, numbers)

# # dict(zip(...)) — 快速构建字典
# print("   构建字典:", dict(zip(names, scores)))


# # 14. 链式操作模式
# print("\n14. 链式操作:")

# data = ["  Apple ", "BANANA", " cherry ", "", "  ", "Date"]

# # 清洗 → 过滤 → 转换 → 排序，一气呵成
# result = sorted(
#     [s.strip().lower() for s in data if s.strip()],
# )
# print("   清洗排序:", result)

# # 用生成器避免中间列表 (大数据时更省内存)
# # 但对于小数据，列表推导式更直观


# # ============================================================
# # 总结: 推导式与函数式编程知识图谱
# # ============================================================
# # 推导式: 列表[], 字典{k:v}, 集合{}, 生成器()
# # 高阶函数: map, filter, sorted, reduce
# # 工具: lambda, any, all, enumerate, zip
# # 排序: key参数, operator.itemgetter/attrgetter
# # 原则: 推导式优先于 map/filter, 可读性优先于简洁
# # ============================================================
