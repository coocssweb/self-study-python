# ============================================================
# 任务一：单词频率统计器 (纯 Python)
# ============================================================
# 难度: ⭐
# 知识点: dict, str.lower(), str.split(), sorted()
# ============================================================
#
# 要求:
# 1. 用下面的 text 变量作为输入
# 2. 统计每个单词出现的次数 (忽略大小写，"The" 和 "the" 算同一个)
# 3. 用 dict 来存储统计结果
# 4. 按频率从高到低排序输出
#
# 提示:
# - str.lower() 转小写
# - str.split() 按空格分割成单词列表
# - sorted(dict.items(), key=lambda x: x[1], reverse=True) 按值排序
#
# 期望输出类似:
#   the: 3
#   python: 2
#   is: 2
#   ...
# ============================================================
import re

text = """
The quick brown fox jumps over the lazy dog.
The dog barked at the fox and the fox ran away.
Python is great and Python is fun.
"""

# 在下面写你的代码 👇
def wordCount(paragraph): 
    """统计字数并附加到文本后面"""
    words = re.split(r"[\s\n.]+", paragraph.lower())
    statistics = {}
    for word in words:
        if word: #跳过空字符串
            statistics[word] = statistics.get(word, 0) + 1

    for word, count in sorted(statistics.items(), key=lambda x: x[1], reverse=True):
        print(f'    {word}: { count }')


if __name__ == "__main__":
    wordCount(text)

