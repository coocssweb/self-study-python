# ============================================================
# Python 异常处理 (Exception) 完整知识点
# ============================================================

# ---- 为什么学这个? ----
# 你在 class 里已经用过 raise ValueError 和 try/except StopIteration
# 现在系统学一下，把这块补完整


# 1. 基础 try/except
print("1. 基础 try/except:")

try:
    result = 10 / 0
except ZeroDivisionError:
    print("   不能除以零!")


# 2. 捕获异常信息
print("\n2. 捕获异常信息:")

try:
    int("abc")
except ValueError as e:
    print(f"   错误信息: {e}")


# 3. 多个 except (从具体到宽泛)
print("\n3. 多个 except:")

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("   除以零!")
    except TypeError:
        print("   类型错误!")
    except Exception as e:
        print(f"   其他错误: {e}")

safe_divide(10, 0)
safe_divide("10", 2)


# 4. 一个 except 捕获多种异常
print("\n4. 一个 except 捕获多种异常:")

try:
    num = int("abc")
except (ValueError, TypeError) as e:
    print(f"   捕获到: {type(e).__name__}: {e}")


# 5. else — 没有异常时执行
print("\n5. else 子句:")

try:
    result = 10 / 3
except ZeroDivisionError:
    print("   出错了!")
else:
    print(f"   没有异常，结果是: {result:.2f}")


# 6. finally — 无论如何都会执行 (清理资源)
print("\n6. finally 子句:")

def read_number(text):
    try:
        return int(text)
    except ValueError:
        print("   转换失败!")
        return None
    finally:
        print("   finally 总是执行 (适合关闭文件、释放资源)")

read_number("abc")


# 7. raise — 主动抛出异常
print("\n7. raise 主动抛出异常:")

def set_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数")
    if age > 150:
        raise ValueError("年龄不合理")
    return age

try:
    set_age(-1)
except ValueError as e:
    print(f"   捕获: {e}")


# 8. 自定义异常类
print("\n8. 自定义异常类:")

class InsufficientFundsError(Exception):
    """余额不足异常"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"余额{balance}元，无法支付{amount}元")

class Wallet:
    def __init__(self, balance):
        self.balance = balance

    def pay(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return self.balance

wallet = Wallet(100)
try:
    wallet.pay(200)
except InsufficientFundsError as e:
    print(f"   {e}")
    print(f"   差额: {e.amount - e.balance}元")


# 9. 异常链 — raise ... from ... (保留原始异常)
print("\n9. 异常链 (raise from):")

def load_config(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"配置加载失败: {path}") from e

try:
    load_config("不存在的文件.txt")
except RuntimeError as e:
    print(f"   {e}")
    print(f"   原始异常: {e.__cause__}")


# 10. 常见内置异常层级 (部分)
print("\n10. 常见内置异常:")
print("""
   BaseException
    ├── KeyboardInterrupt     # Ctrl+C
    ├── SystemExit            # sys.exit()
    └── Exception
         ├── ValueError       # 值不对 (int("abc"))
         ├── TypeError        # 类型不对 ("1" + 1)
         ├── KeyError         # 字典键不存在
         ├── IndexError       # 列表索引越界
         ├── AttributeError   # 属性不存在
         ├── FileNotFoundError# 文件不存在
         ├── ZeroDivisionError# 除以零
         ├── StopIteration    # 迭代器耗尽 (你在 03_iter.py 见过)
         ├── RuntimeError     # 通用运行时错误
         └── OSError          # 系统相关错误
""")
# 提示: 永远不要 except BaseException，会把 Ctrl+C 也吞掉


# 11. 上下文管理器处理异常 (和 class 里学的 __exit__ 呼应)
print("11. 上下文管理器处理异常:")

class SafeBlock:
    def __enter__(self):
        print("   进入安全块")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"   捕获到异常: {exc_type.__name__}: {exc_val}")
            return True  # 返回 True 表示吞掉异常，不再向外传播
        print("   正常退出")
        return False

with SafeBlock():
    print("   执行一些操作...")
    raise ValueError("测试异常")

print("   程序继续运行 (异常被 __exit__ 吞掉了)")


# 12. 实用模式: EAFP vs LBYL
print("\n12. EAFP vs LBYL:")

data = {"name": "小明", "age": 18}

# LBYL (Look Before You Leap) — 先检查再操作
if "score" in data:
    print("   LBYL:", data["score"])
else:
    print("   LBYL: 键不存在")

# EAFP (Easier to Ask Forgiveness than Permission) — 先做再说，出错再处理
# Python 社区更推荐这种风格!
try:
    print("   EAFP:", data["score"])
except KeyError:
    print("   EAFP: 键不存在")


# 13. assert — 调试断言 (开发时用，生产环境可被 -O 关闭)
print("\n13. assert 断言:")

def calculate_average(scores):
    assert len(scores) > 0, "成绩列表不能为空"
    return sum(scores) / len(scores)

print("   平均分:", calculate_average([90, 85, 95]))

try:
    calculate_average([])
except AssertionError as e:
    print(f"   断言失败: {e}")


# ============================================================
# 总结: 异常处理知识图谱
# ============================================================
# 基础: try / except / else / finally
# 捕获: 单个异常, 多个异常, as e 获取信息
# 抛出: raise, raise ... from ...
# 自定义: 继承 Exception 创建自己的异常类
# 层级: BaseException → Exception → 具体异常
# 模式: EAFP (推荐) vs LBYL
# 关联: 上下文管理器 (__exit__), assert 断言
# ============================================================
