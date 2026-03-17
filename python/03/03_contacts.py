# ============================================================
# 实战案例 3: 通讯录管理系统 (面向对象)
# ============================================================
# 综合运用: 类, 继承, 魔术方法, 异常处理, 文件读写, 推导式, 正则
# 运行: python 03/03_contacts.py

import json
import os
import re
from datetime import datetime


class ValidationError(Exception):
    """数据验证异常"""
    pass


class Contact:
    """联系人"""

    def __init__(self, name, phone, email="", group="默认"):
        self.name = self._validate_name(name)
        self.phone = self._validate_phone(phone)
        self.email = self._validate_email(email) if email else ""
        self.group = group
        self.created = datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def _validate_name(name):
        name = name.strip()
        if not name or len(name) > 20:
            raise ValidationError("姓名不能为空且不超过20字符")
        return name

    @staticmethod
    def _validate_phone(phone):
        phone = re.sub(r"[\s\-]", "", phone)  # 去掉空格和横杠
        if not re.match(r"^\d{7,15}$", phone):
            raise ValidationError(f"手机号格式不正确: {phone}")
        return phone

    @staticmethod
    def _validate_email(email):
        if email and not re.match(r"^[\w.+-]+@[\w-]+\.[\w.]+$", email):
            raise ValidationError(f"邮箱格式不正确: {email}")
        return email

    def to_dict(self):
        """转为字典 (用于 JSON 序列化)"""
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "group": self.group,
            "created": self.created,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建 (工厂方法)"""
        contact = cls.__new__(cls)
        contact.name = data["name"]
        contact.phone = data["phone"]
        contact.email = data.get("email", "")
        contact.group = data.get("group", "默认")
        contact.created = data.get("created", "未知")
        return contact

    def __str__(self):
        parts = [f"{self.name} | {self.phone}"]
        if self.email:
            parts.append(self.email)
        parts.append(f"[{self.group}]")
        return " | ".join(parts)

    def __repr__(self):
        return f"Contact({self.name!r}, {self.phone!r})"

    def __eq__(self, other):
        if not isinstance(other, Contact):
            return False
        return self.phone == other.phone

    def __hash__(self):
        return hash(self.phone)


class ContactBook:
    """通讯录"""

    def __init__(self, filepath=None):
        self.filepath = filepath or os.path.join(
            os.path.dirname(__file__), "contacts_data.json"
        )
        self.contacts = []
        self._load()

    def _load(self):
        """从文件加载"""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.contacts = [Contact.from_dict(d) for d in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"  [警告] 加载失败: {e}")
                self.contacts = []

    def _save(self):
        """保存到文件"""
        data = [c.to_dict() for c in self.contacts]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add(self, name, phone, email="", group="默认"):
        """添加联系人"""
        contact = Contact(name, phone, email, group)
        # 检查手机号是否重复
        if contact in self.contacts:
            raise ValidationError(f"手机号 {phone} 已存在")
        self.contacts.append(contact)
        self._save()
        return contact

    def delete(self, name):
        """按姓名删除"""
        before = len(self.contacts)
        self.contacts = [c for c in self.contacts if c.name != name]
        if len(self.contacts) < before:
            self._save()
            return True
        return False

    def search(self, keyword):
        """搜索 (姓名、手机号、邮箱模糊匹配)"""
        keyword = keyword.lower()
        return [
            c for c in self.contacts
            if keyword in c.name.lower()
            or keyword in c.phone
            or keyword in c.email.lower()
        ]

    def get_groups(self):
        """获取所有分组及数量"""
        groups = {}
        for c in self.contacts:
            groups[c.group] = groups.get(c.group, 0) + 1
        return groups

    def list_by_group(self, group):
        """按分组列出"""
        return [c for c in self.contacts if c.group == group]

    def __len__(self):
        return len(self.contacts)

    def __iter__(self):
        return iter(sorted(self.contacts, key=lambda c: c.name))

    def __contains__(self, phone):
        return any(c.phone == phone for c in self.contacts)


# ============================================================
# 演示
# ============================================================

def demo():
    """演示通讯录功能"""
    # 使用临时文件，不污染目录
    import tempfile
    tmp = os.path.join(tempfile.mkdtemp(), "demo_contacts.json")
    book = ContactBook(tmp)

    print("=" * 50)
    print("  通讯录管理系统 演示")
    print("=" * 50)

    # 添加联系人
    print("\n📝 添加联系人:")
    test_data = [
        ("张三", "13800001111", "zhangsan@test.com", "朋友"),
        ("李四", "13900002222", "lisi@test.com", "同事"),
        ("王五", "13700003333", "", "朋友"),
        ("赵六", "13600004444", "zhaoliu@test.com", "家人"),
        ("小明", "13500005555", "", "同事"),
    ]
    for name, phone, email, group in test_data:
        try:
            c = book.add(name, phone, email, group)
            print(f"  ✓ {c}")
        except ValidationError as e:
            print(f"  ✗ {e}")

    # 重复添加测试
    print("\n🚫 重复添加测试:")
    try:
        book.add("张三2号", "13800001111")
    except ValidationError as e:
        print(f"  ✗ 预期错误: {e}")

    # 验证测试
    print("\n🚫 验证测试:")
    for name, phone in [("", "123"), ("测试", "abc")]:
        try:
            book.add(name, phone)
        except ValidationError as e:
            print(f"  ✗ 预期错误: {e}")

    # 搜索
    print("\n🔍 搜索 '张':")
    for c in book.search("张"):
        print(f"  {c}")

    print("\n🔍 搜索 '139':")
    for c in book.search("139"):
        print(f"  {c}")

    # 分组
    print("\n📂 分组统计:")
    for group, count in book.get_groups().items():
        print(f"  {group}: {count} 人")

    print("\n📂 朋友分组:")
    for c in book.list_by_group("朋友"):
        print(f"  {c}")

    # 遍历 (自动按姓名排序)
    print(f"\n📋 全部联系人 (共 {len(book)} 人):")
    for c in book:
        print(f"  {c}")

    # in 操作符
    print(f"\n📱 13800001111 在通讯录中: {'13800001111' in book}")

    # 删除
    print("\n🗑️ 删除王五:")
    book.delete("王五")
    print(f"  剩余 {len(book)} 人")

    # 清理临时文件
    os.unlink(tmp)
    os.rmdir(os.path.dirname(tmp))
    print("\n  演示完成，临时数据已清理")


if __name__ == "__main__":
    demo()
