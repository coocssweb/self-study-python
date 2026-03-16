# ============================================================
# Python 模块与包 (Module & Package) 完整知识点
# ============================================================

# ---- 为什么学这个? ----
# 前面所有代码都写在单个文件里，但真实项目需要把代码拆分到多个文件
# 模块就是 Python 组织和复用代码的方式


# 1. 什么是模块 — 一个 .py 文件就是一个模块
print("1. 什么是模块:")
print("   每个 .py 文件就是一个模块")
print("   比如 01_def.py 就是一个模块，里面的函数可以被其他文件 import")


# 2. import 的几种写法
print("\n2. import 的几种写法:")

# 2.1 import 整个模块
import math
print("   import math:", math.sqrt(16), math.pi)

# 2.2 from ... import ... (只导入需要的)
from math import ceil, floor
print("   from math import:", ceil(3.2), floor(3.8))

# 2.3 from ... import * (导入所有公开名称，不推荐!)
# from math import *  # 会污染命名空间，容易冲突

# 2.4 import ... as ... (起别名)
import math as m
print("   import as:", m.pow(2, 10))

# 2.5 from ... import ... as ...
from math import factorial as fac
print("   from import as:", fac(5))


# 3. 模块搜索路径
print("\n3. 模块搜索路径:")
import sys
print("   sys.path (前3个):")
for p in sys.path[:3]:
    print(f"     {p}")
print("   ...")
# Python 按 sys.path 的顺序查找模块:
# 1) 当前目录
# 2) PYTHONPATH 环境变量
# 3) 标准库目录
# 4) site-packages (第三方库)


# 4. __name__ 和 __main__ — 最经典的 Python 惯用法
print("\n4. __name__ 和 __main__:")
print(f"   当前模块的 __name__ = '{__name__}'")

# 当直接运行文件时: __name__ == "__main__"
# 当被其他文件 import 时: __name__ == "模块名"

# 所以常见写法:
# if __name__ == "__main__":
#     main()  # 只在直接运行时执行，被 import 时不执行

def demo_main():
    print("   这个函数只在直接运行时才会被调用")

if __name__ == "__main__":
    demo_main()


# 5. 常用标准库模块速览
print("\n5. 常用标准库模块:")

# 5.1 os — 操作系统交互
import os
print("   os.getcwd():", os.getcwd())
print("   os.name:", os.name)  # nt(Windows) 或 posix(Linux/Mac)

# 5.2 os.path — 路径操作
print("   os.path.join:", os.path.join("folder", "file.txt"))
print("   os.path.exists('.'):", os.path.exists("."))

# 5.3 sys — 系统相关
import sys
print("   sys.version:", sys.version.split()[0])
print("   sys.platform:", sys.platform)

# 5.4 json — JSON 处理
import json
data = {"name": "小明", "age": 18, "scores": [90, 85, 95]}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print("   json.dumps:")
print("  ", json_str.replace("\n", "\n   "))

parsed = json.loads(json_str)
print("   json.loads:", parsed["name"], parsed["scores"])

# 5.5 datetime — 日期时间
from datetime import datetime, timedelta
now = datetime.now()
print(f"   现在: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   3天后: {(now + timedelta(days=3)).strftime('%Y-%m-%d')}")

# 5.6 random — 随机数
import random
random.seed(42)  # 固定种子，结果可复现
print("   random.randint(1,100):", random.randint(1, 100))
print("   random.choice:", random.choice(["苹果", "香蕉", "橘子"]))
print("   random.sample:", random.sample(range(10), 3))

# 5.7 collections — 增强容器
from collections import Counter, defaultdict, namedtuple

# Counter — 计数器
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
print("   Counter:", Counter(words))
print("   最常见:", Counter(words).most_common(2))

# defaultdict — 带默认值的字典
dd = defaultdict(list)
dd["水果"].append("苹果")
dd["水果"].append("香蕉")
dd["蔬菜"].append("白菜")
print("   defaultdict:", dict(dd))

# namedtuple — 具名元组
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(f"   namedtuple: Point({p.x}, {p.y})")


# 6. 包 (Package) — 用文件夹组织模块
print("\n6. 包 (Package):")
print("""   包就是一个包含 __init__.py 的文件夹
   
   my_package/
     __init__.py      # 标记这是一个包 (可以为空)
     module_a.py
     module_b.py
     sub_package/
       __init__.py
       module_c.py
   
   使用方式:
     import my_package.module_a
     from my_package import module_b
     from my_package.sub_package import module_c
""")


# 7. __init__.py 的作用
print("7. __init__.py 的作用:")
print("""   1) 标记目录为 Python 包
   2) 包被 import 时自动执行
   3) 可以在里面定义 __all__ 控制 from package import * 的行为
   4) Python 3.3+ 支持"命名空间包"(没有 __init__.py)，但建议还是加上
""")


# 8. __all__ — 控制 from xxx import * 的导出
print("8. __all__:")
print("   在模块里定义 __all__ = ['func1', 'func2']")
print("   这样 from module import * 只会导入列表里的名称")
print("   没有 __all__ 时，导入所有不以 _ 开头的名称")

# 示例 (假设在某个模块里):
# __all__ = ["public_func", "PublicClass"]
# def public_func(): ...
# def _private_func(): ...  # 不会被 import *


# 9. 相对导入 vs 绝对导入
print("\n9. 相对导入 vs 绝对导入:")
print("""   绝对导入 (推荐):
     from my_package.module_a import func
   
   相对导入 (包内部使用):
     from . import module_b        # 同级目录
     from .. import module_c       # 上级目录
     from .sub import helper       # 子目录
   
   注意: 相对导入只能在包内使用，不能在直接运行的脚本里用
""")


# 10. 模块的重新加载
print("10. 模块重新加载:")
print("   import 只会执行一次，重复 import 不会重新加载")
print("   需要重新加载时:")
print("   from importlib import reload")
print("   reload(module_name)")


# 11. 模块中的特殊属性
print("\n11. 模块特殊属性:")
print(f"   __name__: {__name__}")
print(f"   __file__: {__file__}")
# __doc__: 模块的文档字符串
# __package__: 模块所属的包
# __spec__: 模块的导入规格


# 12. 实用技巧: 延迟导入 (Lazy Import)
print("\n12. 延迟导入:")

def process_data(data):
    """只在真正需要时才导入，加快启动速度"""
    import json  # 在函数内部导入
    return json.dumps(data)

print("   延迟导入结果:", process_data({"key": "value"}))
print("   适用场景: 模块很重但不一定每次都用到")


# 13. 用 dir() 和 help() 探索模块
print("\n13. 探索模块:")
import math
print("   dir(math) 前10个:", dir(math)[:10])
print("   math.sqrt.__doc__:", math.sqrt.__doc__)
# help(math)  # 交互式查看完整文档 (内容很长，这里不执行)


# ============================================================
# 总结: 模块与包知识图谱
# ============================================================
# 基础: import, from import, as 别名
# 核心: __name__ == "__main__", 模块搜索路径 sys.path
# 包: __init__.py, __all__, 相对导入 vs 绝对导入
# 标准库: os, sys, json, datetime, random, collections
# 技巧: 延迟导入, dir() 探索, reload() 重载
# ============================================================
