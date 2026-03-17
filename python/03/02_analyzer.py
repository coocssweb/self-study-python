# ============================================================
# 实战案例 2: 文本文件分析器
# ============================================================
# 综合运用: 文件读写, 字符串处理, 正则表达式, 字典, 推导式, 排序
# 运行: python 03/02_analyzer.py
# 会分析自身源码作为演示

import re
import os
from collections import Counter


def analyze_file(filepath):
    """分析一个文本文件，返回统计信息"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines()

    # 基础统计
    total_lines = len(lines)
    blank_lines = sum(1 for line in lines if not line.strip())
    comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
    code_lines = total_lines - blank_lines - comment_lines

    # 字符统计
    total_chars = len(content)
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", content))
    english_words = re.findall(r"[a-zA-Z_]\w*", content)

    # 词频统计 (英文标识符)
    word_freq = Counter(w.lower() for w in english_words)

    # 最长行
    longest_line = max(lines, key=len) if lines else ""
    longest_len = len(longest_line)

    # 查找所有函数定义
    functions = re.findall(r"def\s+(\w+)\s*\(", content)

    # 查找所有类定义
    classes = re.findall(r"class\s+(\w+)", content)

    # 查找所有 import
    imports = re.findall(r"^(?:from\s+\S+\s+)?import\s+.+", content, re.MULTILINE)

    return {
        "filepath": filepath,
        "total_lines": total_lines,
        "code_lines": code_lines,
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
        "total_chars": total_chars,
        "chinese_chars": chinese_chars,
        "unique_words": len(word_freq),
        "top_words": word_freq.most_common(10),
        "longest_line_len": longest_len,
        "functions": functions,
        "classes": classes,
        "imports": imports,
    }


def print_report(stats):
    """打印分析报告"""
    print("=" * 50)
    print(f"  文件分析报告: {stats['filepath']}")
    print("=" * 50)

    print(f"\n  📊 行数统计:")
    print(f"     总行数:   {stats['total_lines']}")
    print(f"     代码行:   {stats['code_lines']}")
    print(f"     注释行:   {stats['comment_lines']}")
    print(f"     空白行:   {stats['blank_lines']}")

    if stats["total_lines"] > 0:
        code_pct = stats["code_lines"] / stats["total_lines"]
        print(f"     代码占比:  {code_pct:.0%}")

    print(f"\n  📝 字符统计:")
    print(f"     总字符:   {stats['total_chars']}")
    print(f"     中文字符: {stats['chinese_chars']}")
    print(f"     不同单词: {stats['unique_words']}")
    print(f"     最长行:   {stats['longest_line_len']} 字符")

    if stats["functions"]:
        print(f"\n  🔧 函数 ({len(stats['functions'])} 个):")
        for fn in stats["functions"]:
            print(f"     def {fn}()")

    if stats["classes"]:
        print(f"\n  📦 类 ({len(stats['classes'])} 个):")
        for cls in stats["classes"]:
            print(f"     class {cls}")

    if stats["imports"]:
        print(f"\n  📥 导入 ({len(stats['imports'])} 个):")
        for imp in stats["imports"]:
            print(f"     {imp.strip()}")

    print(f"\n  🔤 高频词 TOP 10:")
    for word, count in stats["top_words"]:
        bar = "█" * min(count, 30)
        print(f"     {word:<15} {count:>3} {bar}")


def analyze_directory(dirpath, ext=".py"):
    """分析目录下所有指定扩展名的文件"""
    results = []
    for root, dirs, files in os.walk(dirpath):
        for fname in sorted(files):
            if fname.endswith(ext):
                fpath = os.path.join(root, fname)
                try:
                    stats = analyze_file(fpath)
                    results.append(stats)
                except Exception as e:
                    print(f"  跳过 {fpath}: {e}")
    return results


def print_summary(results):
    """打印目录汇总"""
    print("\n" + "=" * 60)
    print("  项目汇总")
    print("=" * 60)

    total_code = sum(r["code_lines"] for r in results)
    total_comment = sum(r["comment_lines"] for r in results)
    total_blank = sum(r["blank_lines"] for r in results)
    total_funcs = sum(len(r["functions"]) for r in results)
    total_classes = sum(len(r["classes"]) for r in results)

    print(f"\n  文件数:   {len(results)}")
    print(f"  代码行:   {total_code}")
    print(f"  注释行:   {total_comment}")
    print(f"  空白行:   {total_blank}")
    print(f"  总行数:   {total_code + total_comment + total_blank}")
    print(f"  函数数:   {total_funcs}")
    print(f"  类数:     {total_classes}")

    # 按代码行数排序
    print(f"\n  各文件代码行数:")
    for r in sorted(results, key=lambda x: x["code_lines"], reverse=True):
        name = os.path.relpath(r["filepath"])
        bar = "█" * (r["code_lines"] // 5)
        print(f"    {name:<30} {r['code_lines']:>4} 行 {bar}")


if __name__ == "__main__":
    # 演示 1: 分析自身
    print("【演示 1: 分析单个文件 (自身)】")
    stats = analyze_file(__file__)
    print_report(stats)

    # 演示 2: 分析整个项目
    project_root = os.path.dirname(os.path.dirname(__file__))
    print("\n\n【演示 2: 分析整个项目】")
    results = analyze_directory(project_root)
    if results:
        print_summary(results)
