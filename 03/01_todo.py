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
