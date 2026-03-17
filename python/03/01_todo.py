# ============================================================
# 实战案例 1: 命令行待办事项管理器
# ============================================================
# 综合运用: 字典, 列表, 文件读写(JSON), 异常处理, 函数, 字符串格式化
# 运行: python 03/01_todo.py

import json
import os
from datetime import datetime

# 数据文件路径 (和脚本同目录)
DATA_FILE = os.path.join(os.path.dirname(__file__), "todo_data.json")


def load_todos():
    """从 JSON 文件加载待办列表"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("  [警告] 数据文件损坏，已重置")
        return []


def save_todos(todos):
    """保存待办列表到 JSON 文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def add_todo(todos, title, priority="中"):
    """添加待办事项"""
    todo = {
        "id": max((t["id"] for t in todos), default=0) + 1,
        "title": title,
        "priority": priority,
        "done": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    todos.append(todo)
    save_todos(todos)
    print(f"  ✓ 已添加: [{todo['id']}] {title} (优先级: {priority})")


def list_todos(todos, show_done=False):
    """显示待办列表"""
    filtered = todos if show_done else [t for t in todos if not t["done"]]
    if not filtered:
        print("  (空空如也)")
        return

    # 按优先级排序: 高 > 中 > 低
    priority_order = {"高": 0, "中": 1, "低": 2}
    filtered.sort(key=lambda t: (t["done"], priority_order.get(t["priority"], 9)))

    print(f"  {'ID':<4} {'状态':<4} {'优先级':<6} {'标题':<20} {'创建时间'}")
    print("  " + "-" * 56)
    for t in filtered:
        status = "✓" if t["done"] else "○"
        print(f"  {t['id']:<4} {status:<4} {t['priority']:<6} {t['title']:<20} {t['created']}")


def done_todo(todos, todo_id):
    """标记完成"""
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = True
            save_todos(todos)
            print(f"  ✓ 已完成: {t['title']}")
            return
    print(f"  ✗ 找不到 ID={todo_id}")


def delete_todo(todos, todo_id):
    """删除待办"""
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            removed = todos.pop(i)
            save_todos(todos)
            print(f"  ✓ 已删除: {removed['title']}")
            return
    print(f"  ✗ 找不到 ID={todo_id}")


def search_todos(todos, keyword):
    """搜索待办"""
    results = [t for t in todos if keyword.lower() in t["title"].lower()]
    if results:
        print(f"  找到 {len(results)} 条:")
        for t in results:
            status = "✓" if t["done"] else "○"
            print(f"    [{t['id']}] {status} {t['title']}")
    else:
        print(f"  没有找到包含 '{keyword}' 的待办")


def stats(todos):
    """统计信息"""
    total = len(todos)
    done = sum(1 for t in todos if t["done"])
    by_priority = {}
    for t in todos:
        p = t["priority"]
        by_priority[p] = by_priority.get(p, 0) + 1

    print(f"  总计: {total} 条")
    print(f"  已完成: {done} 条 / 未完成: {total - done} 条")
    if total > 0:
        print(f"  完成率: {done / total:.0%}")
    for p in ["高", "中", "低"]:
        if p in by_priority:
            print(f"  {p}优先级: {by_priority[p]} 条")


def show_help():
    """显示帮助"""
    print("""
  命令列表:
    add <标题> [高/中/低]  — 添加待办 (默认中优先级)
    list                  — 显示未完成
    list all              — 显示全部
    done <ID>             — 标记完成
    del <ID>              — 删除
    search <关键词>       — 搜索
    stats                 — 统计
    help                  — 帮助
    quit                  — 退出
""")


def main():
    """主循环"""
    todos = load_todos()
    print("=" * 40)
    print("  待办事项管理器")
    print("  输入 help 查看命令")
    print("=" * 40)

    while True:
        try:
            cmd = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  再见!")
            break

        if not cmd:
            continue

        parts = cmd.split(maxsplit=1)
        action = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if action == "quit":
            print("  再见!")
            break
        elif action == "help":
            show_help()
        elif action == "add":
            if not arg:
                print("  用法: add <标题> [高/中/低]")
                continue
            # 检查最后一个词是否是优先级
            words = arg.rsplit(maxsplit=1)
            if len(words) == 2 and words[1] in ("高", "中", "低"):
                add_todo(todos, words[0], words[1])
            else:
                add_todo(todos, arg)
        elif action == "list":
            list_todos(todos, show_done=(arg == "all"))
        elif action == "done":
            try:
                done_todo(todos, int(arg))
            except ValueError:
                print("  用法: done <ID>")
        elif action == "del":
            try:
                delete_todo(todos, int(arg))
            except ValueError:
                print("  用法: del <ID>")
        elif action == "search":
            if arg:
                search_todos(todos, arg)
            else:
                print("  用法: search <关键词>")
        elif action == "stats":
            stats(todos)
        else:
            print(f"  未知命令: {action}，输入 help 查看帮助")


if __name__ == "__main__":
    main()
