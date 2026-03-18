# ============================================================
# 任务四：CSV 解析器 (纯 Python)
# ============================================================
# 难度: ⭐⭐
# 知识点: str.split(), zip(), list[dict]
# ============================================================
#
# 要求:
# 1. 用下面的 csv_text 变量作为输入
# 2. 写一个 parse_csv(text) -> list[dict] 函数
# 3. 第一行是表头，后面是数据
# 4. 不用 csv 模块，纯字符串操作
#
# 提示:
# - str.strip() 去掉首尾空白
# - str.split('\n') 按行分割
# - str.split(',') 按逗号分割
# - zip(headers, values) 把表头和数据配对
# - dict(zip(...)) 直接生成字典
#
# 期望输出:
#   {'name': '小明', 'age': '25', 'city': '北京'}
#   {'name': '小红', 'age': '30', 'city': '上海'}
#   {'name': '小王', 'age': '28', 'city': '深圳'}
# ============================================================

csv_text = """name,age,city
小明,25,北京
小红,30,上海
小王,28,深圳"""

# 在下面写你的代码 👇
def parse_csv(text):
    """解析 CSV 文本，返回 list[dict]"""
    strip_text = text.strip()
    text_lines = strip_text.split('\n')
    arr = []
    for text_line in text_lines:
        arr.append(text_line.split(','))
    column_headers = arr[0]
    column_values =arr[1:]
    # 表头数据匹配，生成字典
    # 插入list
    return [dict(zip(column_headers, item)) for item in column_values]

if __name__ == "__main__":
    records = parse_csv(csv_text)
    for record in records:
        print(record)

