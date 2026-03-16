# ============================================================
# Python 文件操作 (File I/O) 完整知识点
# ============================================================

# ---- 为什么学这个? ----
# 读写文件是最常见的实际需求: 读配置、写日志、处理数据...
# 你在 05_exception.py 里已经见过 open() 和 FileNotFoundError
# 现在系统学一下文件操作

import os
import json
import tempfile

# 用临时目录存放演示文件，运行完自动清理
DEMO_DIR = tempfile.mkdtemp(prefix="py_file_demo_")
print(f"演示目录: {DEMO_DIR}\n")


# 1. 基础: open() 和 with 语句
print("1. 基础读写:")

file_path = os.path.join(DEMO_DIR, "hello.txt")

# 写入文件
with open(file_path, "w", encoding="utf-8") as f:
    f.write("你好，世界!\n")
    f.write("Hello, World!\n")
    f.write("第三行\n")

# 读取文件
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    print("   read():", repr(content))

# 为什么用 with? 它会自动调用 f.close()，即使出异常也不会忘记关闭
# 等价于你在 04_class.py 学的上下文管理器 __enter__ / __exit__


# 2. 读取方式对比
print("\n2. 读取方式对比:")

with open(file_path, "r", encoding="utf-8") as f:
    # read() — 一次读完整个文件 (小文件用)
    all_text = f.read()
    print("   read():", all_text.replace("\n", "\\n"))

with open(file_path, "r", encoding="utf-8") as f:
    # readline() — 读一行
    line1 = f.readline()
    print("   readline():", repr(line1))

with open(file_path, "r", encoding="utf-8") as f:
    # readlines() — 读所有行，返回列表
    lines = f.readlines()
    print("   readlines():", lines)

with open(file_path, "r", encoding="utf-8") as f:
    # 最推荐: 直接遍历文件对象 (内存友好，适合大文件)
    print("   逐行遍历:")
    for line in f:
        print(f"     {line.strip()}")


# 3. 写入模式对比
print("\n3. 写入模式:")
print("""   'r'  — 只读 (默认)
   'w'  — 写入 (覆盖已有内容!)
   'a'  — 追加 (在末尾添加)
   'x'  — 独占创建 (文件已存在则报错)
   'r+' — 读写
   'w+' — 写读 (先清空)
   'a+' — 追加读
   'b'  — 二进制模式 (如 'rb', 'wb')
""")

# 追加模式演示
append_path = os.path.join(DEMO_DIR, "append.txt")
with open(append_path, "w", encoding="utf-8") as f:
    f.write("第一次写入\n")

with open(append_path, "a", encoding="utf-8") as f:
    f.write("追加的内容\n")

with open(append_path, "r", encoding="utf-8") as f:
    print("   追加结果:", f.read().strip())


# 4. writelines() — 写入多行
print("\n4. writelines():")

lines_path = os.path.join(DEMO_DIR, "lines.txt")
lines = ["苹果\n", "香蕉\n", "橘子\n"]

with open(lines_path, "w", encoding="utf-8") as f:
    f.writelines(lines)  # 注意: 不会自动加换行符!

with open(lines_path, "r", encoding="utf-8") as f:
    print("   writelines:", f.read().strip())


# 5. 文件指针操作: tell() 和 seek()
print("\n5. tell() 和 seek():")

with open(file_path, "r", encoding="utf-8") as f:
    print("   初始位置:", f.tell())
    f.read(6)  # 读6个字符 ("你好，世界!" 中文占3字节)
    print("   读取后位置:", f.tell())
    f.seek(0)  # 回到开头
    print("   seek(0)后:", f.readline().strip())


# 6. 编码问题 — encoding 很重要!
print("\n6. 编码:")
print("   永远指定 encoding='utf-8'，不要依赖系统默认编码")
print("   Windows 默认是 gbk，Linux/Mac 默认是 utf-8")
print("   不指定编码 → 跨平台就会出乱码")

# 查看默认编码
import locale
print(f"   当前系统默认编码: {locale.getpreferredencoding()}")


# 7. 二进制模式
print("\n7. 二进制模式:")

bin_path = os.path.join(DEMO_DIR, "data.bin")

# 写入二进制
with open(bin_path, "wb") as f:
    f.write(b"\x00\x01\x02\x03\xff")
    f.write("你好".encode("utf-8"))

# 读取二进制
with open(bin_path, "rb") as f:
    data = f.read()
    print("   bytes:", data)
    print("   hex:", data.hex())
    print("   长度:", len(data), "字节")


# 8. os 和 os.path — 文件系统操作
print("\n8. 文件系统操作:")

# 创建目录
sub_dir = os.path.join(DEMO_DIR, "sub", "deep")
os.makedirs(sub_dir, exist_ok=True)  # exist_ok=True 已存在不报错
print("   创建目录:", sub_dir)

# 路径操作
print("   os.path.basename:", os.path.basename("/home/user/file.txt"))
print("   os.path.dirname:", os.path.dirname("/home/user/file.txt"))
print("   os.path.splitext:", os.path.splitext("photo.jpg"))
print("   os.path.abspath('.'):", os.path.abspath("."))

# 判断
print("   os.path.exists:", os.path.exists(file_path))
print("   os.path.isfile:", os.path.isfile(file_path))
print("   os.path.isdir:", os.path.isdir(DEMO_DIR))

# 文件信息
size = os.path.getsize(file_path)
print(f"   文件大小: {size} 字节")

# 列出目录内容
print("   目录内容:", os.listdir(DEMO_DIR))


# 9. pathlib — 更现代的路径操作 (Python 3.4+, 推荐)
print("\n9. pathlib (推荐):")

from pathlib import Path

# 创建路径对象
p = Path(DEMO_DIR) / "pathlib_demo.txt"

# 写入 (一行搞定)
p.write_text("pathlib 写入的内容\n第二行", encoding="utf-8")

# 读取 (一行搞定)
print("   read_text:", p.read_text(encoding="utf-8").replace("\n", "\\n"))

# 路径操作
print("   name:", p.name)
print("   stem:", p.stem)          # 不带扩展名的文件名
print("   suffix:", p.suffix)      # 扩展名
print("   parent:", p.parent)

# 遍历目录
print("   遍历目录:")
for item in Path(DEMO_DIR).iterdir():
    tag = "[目录]" if item.is_dir() else "[文件]"
    print(f"     {tag} {item.name}")

# glob 模式匹配
print("   glob *.txt:", [f.name for f in Path(DEMO_DIR).glob("*.txt")])


# 10. 读写 JSON 文件 (实际项目最常见)
print("\n10. JSON 文件读写:")

json_path = os.path.join(DEMO_DIR, "config.json")

config = {
    "app_name": "我的应用",
    "version": "1.0.0",
    "features": ["登录", "注册", "搜索"],
    "database": {
        "host": "localhost",
        "port": 3306
    }
}

# 写入 JSON
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
    print("   写入成功")

# 读取 JSON
with open(json_path, "r", encoding="utf-8") as f:
    loaded = json.load(f)
    print("   读取:", loaded["app_name"], loaded["version"])
    print("   features:", loaded["features"])


# 11. 读写 CSV (不用第三方库)
print("\n11. CSV 文件:")

import csv

csv_path = os.path.join(DEMO_DIR, "students.csv")

# 写入 CSV
students = [
    ["姓名", "年龄", "成绩"],
    ["小明", 18, 90],
    ["小红", 17, 95],
    ["小刚", 19, 85],
]

with open(csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(students)

# 读取 CSV
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)  # 第一行是表头
    print(f"   表头: {header}")
    for row in reader:
        print(f"   {row[0]} — 年龄{row[1]}, 成绩{row[2]}")

# DictReader — 用字典方式读取 (更方便)
print("   DictReader:")
with open(csv_path, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(f"     {row['姓名']}: {row['成绩']}分")


# 12. tempfile — 临时文件 (本脚本就在用)
print("\n12. tempfile 临时文件:")

import tempfile

# 临时文件 (用完自动删除)
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
    tmp.write("临时内容")
    print(f"   临时文件: {tmp.name}")
    tmp_name = tmp.name

# 读回来验证
with open(tmp_name, "r", encoding="utf-8") as f:
    print(f"   内容: {f.read()}")
os.unlink(tmp_name)  # 手动删除
print("   已清理")


# 13. 文件复制、移动、删除
print("\n13. 文件操作:")

import shutil

# 复制文件
src = file_path
dst = os.path.join(DEMO_DIR, "hello_copy.txt")
shutil.copy2(src, dst)  # copy2 保留元数据
print("   复制:", os.path.exists(dst))

# 移动/重命名
new_dst = os.path.join(DEMO_DIR, "hello_moved.txt")
shutil.move(dst, new_dst)
print("   移动:", os.path.exists(new_dst))

# 删除文件
os.remove(new_dst)
print("   删除:", not os.path.exists(new_dst))

# 删除目录树
# shutil.rmtree(some_dir)  # 危险操作! 递归删除整个目录


# 14. 大文件处理技巧
print("\n14. 大文件处理:")
print("   小文件: f.read() 一次读完")
print("   大文件: 逐行遍历 for line in f")
print("   超大文件: 分块读取 ↓")

# 分块读取示例
big_path = os.path.join(DEMO_DIR, "big.txt")
with open(big_path, "w", encoding="utf-8") as f:
    for i in range(100):
        f.write(f"这是第 {i+1} 行数据\n")

total_chars = 0
with open(big_path, "r", encoding="utf-8") as f:
    while True:
        chunk = f.read(1024)  # 每次读 1024 个字符
        if not chunk:
            break
        total_chars += len(chunk)
print(f"   分块读取: 共 {total_chars} 个字符")


# 清理演示目录
shutil.rmtree(DEMO_DIR)
print(f"\n已清理演示目录: {DEMO_DIR}")


# ============================================================
# 总结: 文件操作知识图谱
# ============================================================
# 基础: open(), with 语句, read/write/append 模式
# 读取: read(), readline(), readlines(), 逐行遍历
# 写入: write(), writelines(), print(file=f)
# 编码: 永远指定 encoding="utf-8"
# 路径: os.path (传统) vs pathlib (推荐)
# 格式: JSON (json.load/dump), CSV (csv.reader/writer)
# 操作: shutil (复制/移动), os (删除/重命名)
# 技巧: 大文件分块读取, tempfile 临时文件
# ============================================================
