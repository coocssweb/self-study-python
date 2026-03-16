# ============================================================
# Python 字符串 (String) 完整知识点
# ============================================================

# ---- 为什么学这个? ----
# 01_hello.py 只碰了基础字符串，但实际开发中字符串处理无处不在:
# 解析数据、拼接路径、格式化输出、正则匹配...


# 1. 字符串基础回顾
print("1. 字符串基础:")

s = "Hello, 你好"
print("   长度:", len(s))
print("   索引:", s[0], s[-1])
print("   切片:", s[0:5])
print("   不可变: 字符串不能 s[0] = 'h'，只能创建新字符串")

# 字符串是可迭代对象
print("   遍历:", [c for c in "ABC"])


# 2. 三种引号
print("\n2. 三种引号:")
print('   单引号: \'hello\'')
print("   双引号: \"hello\"")
print("""   三引号: 可以
   跨多行""")

# 原始字符串 (不转义)
print("   普通:", "换行符是\\n")
print("   raw:", r"换行符是\n")  # r 前缀，\n 不会被转义


# 3. 字符串方法 — 查找和判断
print("\n3. 查找和判断:")

s = "Hello World Python"
print("   find:", s.find("World"))       # 6 (找不到返回 -1)
print("   index:", s.index("World"))     # 6 (找不到抛 ValueError)
print("   count:", s.count("o"))         # 2
print("   startswith:", s.startswith("Hello"))
print("   endswith:", s.endswith("Python"))
print("   in:", "World" in s)

# 判断类方法
print("   'abc'.isalpha():", "abc".isalpha())     # 纯字母
print("   '123'.isdigit():", "123".isdigit())     # 纯数字
print("   'abc123'.isalnum():", "abc123".isalnum())  # 字母+数字
print("   '  '.isspace():", "  ".isspace())       # 纯空白
print("   'Hello'.istitle():", "Hello".istitle())  # 首字母大写


# 4. 字符串方法 — 转换
print("\n4. 转换:")

s = "  Hello World  "
print("   upper:", "hello".upper())
print("   lower:", "HELLO".lower())
print("   title:", "hello world".title())
print("   capitalize:", "hello world".capitalize())
print("   swapcase:", "Hello".swapcase())
print("   strip:", repr(s.strip()))       # 去两端空白
print("   lstrip:", repr(s.lstrip()))     # 去左边空白
print("   rstrip:", repr(s.rstrip()))     # 去右边空白
print("   center:", "hi".center(10, "-"))
print("   ljust:", "hi".ljust(10, "-"))
print("   rjust:", "hi".rjust(10, "-"))
print("   zfill:", "42".zfill(5))         # 左边补零


# 5. 字符串方法 — 分割和连接
print("\n5. 分割和连接:")

# split — 分割
print("   split:", "a,b,c,d".split(","))
print("   split(限次):", "a,b,c,d".split(",", 2))
print("   rsplit:", "a,b,c,d".rsplit(",", 2))

# splitlines — 按行分割
text = "第一行\n第二行\n第三行"
print("   splitlines:", text.splitlines())

# join — 连接 (split 的反操作)
words = ["Python", "是", "最好的", "语言"]
print("   join:", " ".join(words))
print("   join路径:", "/".join(["home", "user", "docs"]))

# partition — 分成三部分
print("   partition:", "key=value".partition("="))
print("   rpartition:", "a.b.c".rpartition("."))


# 6. 字符串方法 — 替换
print("\n6. 替换:")

s = "Hello World World"
print("   replace:", s.replace("World", "Python"))
print("   replace(限次):", s.replace("World", "Python", 1))

# translate + maketrans — 字符级替换 (批量替换单个字符)
table = str.maketrans("aeiou", "12345")
print("   translate:", "hello world".translate(table))

# 删除指定字符
table2 = str.maketrans("", "", "aeiou")
print("   删除元音:", "hello world".translate(table2))


# 7. 格式化 — 三种方式
print("\n7. 字符串格式化:")

name = "小明"
age = 18
score = 95.5

# 7.1 % 格式化 (老式，了解即可)
print("   %%格式化: %s 今年 %d 岁, 成绩 %.1f" % (name, age, score))

# 7.2 str.format() (Python 2.6+)
print("   format: {} 今年 {} 岁, 成绩 {:.1f}".format(name, age, score))
print("   format索引: {1} 今年 {0} 岁".format(age, name))
print("   format命名: {n} 今年 {a} 岁".format(n=name, a=age))

# 7.3 f-string (Python 3.6+, 推荐!)
print(f"   f-string: {name} 今年 {age} 岁, 成绩 {score:.1f}")
print(f"   f-string表达式: {age * 2 = }")  # Python 3.8+ 调试技巧


# 8. 格式化 — 常用格式规范
print("\n8. 格式规范 (f-string / format 通用):")

# 数字格式
print(f"   整数: {42:05d}")           # 补零: 00042
print(f"   浮点: {3.14159:.2f}")      # 两位小数: 3.14
print(f"   百分比: {0.856:.1%}")      # 百分比: 85.6%
print(f"   千分位: {1234567:,}")      # 千分位: 1,234,567
print(f"   科学计数: {0.00123:.2e}")  # 科学计数: 1.23e-03
print(f"   二进制: {255:08b}")        # 二进制: 11111111
print(f"   十六进制: {255:#x}")       # 十六进制: 0xff

# 对齐
print(f"   左对齐: {'hi':<10}|")
print(f"   右对齐: {'hi':>10}|")
print(f"   居中:   {'hi':^10}|")
print(f"   填充:   {'hi':*^10}|")


# 9. 正则表达式 — re 模块
print("\n9. 正则表达式 (re):")

import re

text = "我的手机号是 138-1234-5678，邮箱是 test@example.com，生日是 2000-01-15"

# 9.1 re.search — 找第一个匹配
match = re.search(r"\d{3}-\d{4}-\d{4}", text)
if match:
    print(f"   search 手机号: {match.group()}")

# 9.2 re.findall — 找所有匹配
numbers = re.findall(r"\d+", text)
print(f"   findall 所有数字: {numbers}")

# 9.3 re.sub — 替换
masked = re.sub(r"\d{3}-\d{4}-(\d{4})", r"***-****-\1", text)
print(f"   sub 脱敏: {masked}")

# 9.4 re.split — 按模式分割
parts = re.split(r"[,，、\s]+", "苹果, 香蕉，橘子、西瓜 葡萄")
print(f"   split: {parts}")

# 9.5 分组捕获
pattern = r"(\d{4})-(\d{2})-(\d{2})"
match = re.search(pattern, text)
if match:
    print(f"   分组: 年={match.group(1)} 月={match.group(2)} 日={match.group(3)}")

# 9.6 命名分组
pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
match = re.search(pattern, text)
if match:
    print(f"   命名分组: {match.groupdict()}")

# 9.7 编译正则 (多次使用时提高性能)
email_pattern = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
emails = email_pattern.findall(text)
print(f"   编译+findall 邮箱: {emails}")


# 10. 常用正则语法速查
print("\n10. 正则语法速查:")
print("""   .     任意字符 (除换行)
   \\d    数字 [0-9]
   \\w    单词字符 [a-zA-Z0-9_]
   \\s    空白字符
   \\D \\W \\S  上面的取反
   *     0次或多次
   +     1次或多次
   ?     0次或1次
   {n}   恰好n次
   {n,m} n到m次
   ^     开头
   $     结尾
   []    字符集 [abc] [a-z]
   |     或
   ()    分组捕获
   (?:)  非捕获分组
""")


# 11. 字符串编码
print("11. 字符串编码:")

s = "你好"
# 编码: str → bytes
b = s.encode("utf-8")
print(f"   encode: {b}  (长度 {len(b)} 字节)")

# 解码: bytes → str
s2 = b.decode("utf-8")
print(f"   decode: {s2}")

# 常见编码
print("   UTF-8: 中文3字节, 英文1字节 (推荐)")
print("   GBK: 中文2字节 (Windows 中文系统默认)")
print("   ASCII: 只支持英文, 1字节")

# ord 和 chr
print(f"   ord('A'): {ord('A')}")    # 字符 → Unicode 码点
print(f"   chr(65): {chr(65)}")      # Unicode 码点 → 字符
print(f"   ord('中'): {ord('中')}")


# 12. 实用技巧
print("\n12. 实用技巧:")

# 多行字符串拼接 (不用 +)
long_str = ("这是第一部分"
            "这是第二部分"
            "这是第三部分")
print("   隐式拼接:", long_str)

# 字符串乘法
print("   乘法:", "=-" * 10)

# 成员检测
print("   in:", "py" in "python")

# 反转字符串
print("   反转:", "Hello"[::-1])

# 去除指定字符
print("   strip指定:", "###hello###".strip("#"))

# 判断回文
word = "racecar"
print(f"   '{word}' 是回文:", word == word[::-1])


# ============================================================
# 总结: 字符串知识图谱
# ============================================================
# 基础: 索引, 切片, 不可变, 遍历
# 方法: 查找(find/index/in), 判断(is系列), 转换(upper/lower/strip)
# 操作: 分割(split), 连接(join), 替换(replace/translate)
# 格式化: % (老), format (中), f-string (推荐)
# 格式规范: 对齐, 补零, 小数, 百分比, 千分位
# 正则: re.search/findall/sub/split, 分组, 编译
# 编码: encode/decode, UTF-8/GBK, ord/chr
# ============================================================
