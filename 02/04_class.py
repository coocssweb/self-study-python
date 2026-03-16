# ============================================================
# Python 类 (class) 完整知识点
# ============================================================

# 1. 最基础的类
print("1. 基础类定义:")

class Dog:
    """一只狗"""
    def __init__(self, name, age):
        self.name = name    # 实例属性
        self.age = age

    def bark(self):
        return f"{self.name} 说: 汪汪!"

dog = Dog("旺财", 3)
print("  ", dog.bark())
print("   名字:", dog.name, "年龄:", dog.age)


# 2. 类属性 vs 实例属性
print("\n2. 类属性 vs 实例属性:")

class Cat:
    species = "猫科动物"   # 类属性 — 所有实例共享

    def __init__(self, name):
        self.name = name   # 实例属性 — 每个实例独立

c1 = Cat("小白")
c2 = Cat("小黑")
print("   类属性:", c1.species, c2.species)
print("   实例属性:", c1.name, c2.name)

Cat.species = "猫猫"  # 修改类属性，所有实例都受影响
print("   修改后:", c1.species, c2.species)


# 3. 私有属性和私有方法 (名称改写 name mangling)
print("\n3. 私有属性和私有方法:")

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner        # 公开属性
        self.__balance = balance  # 私有属性 (双下划线开头)

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            self.__log("存款", amount)  # 调用私有方法

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            self.__log("取款", amount)
        else:
            print("    余额不足!")

    def get_balance(self):
        """公开方法访问私有属性"""
        return self.__balance

    def __log(self, action, amount):
        """私有方法 — 外部无法直接调用"""
        print(f"    [日志] {self.owner} {action} {amount}元")

acc = BankAccount("小明", 1000)
acc.deposit(500)
acc.withdraw(200)
print("   余额:", acc.get_balance())

# acc.__balance       # AttributeError! 无法直接访问
# acc.__log(...)      # AttributeError! 无法直接调用
# 但 Python 的私有是"君子协定"，其实可以通过 _类名__属性名 访问:
print("   强制访问私有:", acc._BankAccount__balance)  # 不推荐!


# 4. 单下划线约定 (_protected) vs 双下划线 (__private)
print("\n4. 单下划线 vs 双下划线:")

class MyClass:
    def __init__(self):
        self.public = "公开"          # 谁都能访问
        self._protected = "受保护"    # 约定: 子类和内部使用，外部别碰
        self.__private = "私有"       # 名称改写: 变成 _MyClass__private

obj = MyClass()
print("   public:", obj.public)
print("   _protected:", obj._protected)       # 能访问，但不建议
# print(obj.__private)                        # AttributeError
print("   __private:", obj._MyClass__private)  # 能访问，但别这么干


# 5. @property — 把方法变成属性访问 (getter/setter)
print("\n5. @property:")

class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        """getter — 读取时自动调用"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """setter — 赋值时自动调用，可以加验证"""
        if value < 0:
            raise ValueError("半径不能为负数")
        self._radius = value

    @property
    def area(self):
        """只读属性 (没有 setter)"""
        return 3.14159 * self._radius ** 2

c = Circle(5)
print("   半径:", c.radius)
print("   面积:", c.area)
c.radius = 10                # 触发 setter
print("   修改后面积:", c.area)
# c.area = 100              # AttributeError! 只读属性不能赋值


# 6. 继承
print("\n6. 继承:")

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def info(self):
        return f"{self.name}: {self.speak()}"

class Dog2(Animal):
    def speak(self):       # 重写父类方法
        return "汪汪!"

class Cat2(Animal):
    def speak(self):
        return "喵喵~"

animals = [Dog2("旺财"), Cat2("咪咪")]
for a in animals:
    print("  ", a.info())  # 多态: 同一个方法，不同行为


# 7. super() — 调用父类方法
print("\n7. super():")

class Vehicle:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed

class ElectricCar(Vehicle):
    def __init__(self, brand, speed, battery):
        super().__init__(brand, speed)  # 调用父类的 __init__
        self.battery = battery

    def info(self):
        return f"{self.brand} 时速{self.speed}km/h 电池{self.battery}kWh"

car = ElectricCar("特斯拉", 250, 100)
print("  ", car.info())


# 8. 多重继承 和 MRO (方法解析顺序)
print("\n8. 多重继承 和 MRO:")

class A:
    def who(self):
        return "A"

class B(A):
    def who(self):
        return "B"

class C(A):
    def who(self):
        return "C"

class D(B, C):  # 多重继承
    pass

d = D()
print("   D.who():", d.who())          # B — 按 MRO 顺序
print("   MRO:", [cls.__name__ for cls in D.__mro__])  # D → B → C → A → object


# 9. 类方法 (@classmethod) 和 静态方法 (@staticmethod)
print("\n9. @classmethod 和 @staticmethod:")

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_str):
        """类方法 — 第一个参数是类本身 (cls)，常用作工厂方法"""
        y, m, d = map(int, date_str.split("-"))
        return cls(y, m, d)

    @staticmethod
    def is_valid(date_str):
        """静态方法 — 不需要 self 或 cls，就是放在类里的普通函数"""
        parts = date_str.split("-")
        return len(parts) == 3 and all(p.isdigit() for p in parts)

    def __str__(self):
        return f"{self.year}年{self.month}月{self.day}日"

print("   验证:", Date.is_valid("2024-01-15"))
d = Date.from_string("2024-01-15")
print("   工厂方法:", d)


# 10. 魔术方法 (dunder methods) — 让类支持内置操作
print("\n10. 魔术方法:")

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        """开发者看到的表示 (repr)"""
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        """用户看到的表示 (print)"""
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        """支持 + 运算"""
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        """支持 * 运算"""
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        """支持 == 比较"""
        return self.x == other.x and self.y == other.y

    def __len__(self):
        """支持 len()"""
        return int((self.x ** 2 + self.y ** 2) ** 0.5)

    def __bool__(self):
        """支持 bool() 和 if 判断"""
        return self.x != 0 or self.y != 0

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print("   v1:", v1)
print("   v1 + v2:", v1 + v2)
print("   v1 * 3:", v1 * 3)
print("   v1 == v2:", v1 == v2)
print("   len(v2):", len(v2))
print("   bool(Vector(0,0)):", bool(Vector(0, 0)))


# 11. __slots__ — 限制实例属性，节省内存
print("\n11. __slots__:")

class Point:
    __slots__ = ("x", "y")  # 只允许这两个属性

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print("   Point:", p.x, p.y)
# p.z = 3  # AttributeError! __slots__ 不允许添加新属性
print("   优点: 比普通类省内存，访问更快")


# 12. 抽象基类 (ABC) — 强制子类实现某些方法
print("\n12. 抽象基类 (ABC):")

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        """子类必须实现这个方法"""
        pass

    @abstractmethod
    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)

# shape = Shape()  # TypeError! 不能实例化抽象类
rect = Rectangle(3, 4)
print("   面积:", rect.area(), "周长:", rect.perimeter())


# 13. dataclass — 自动生成 __init__, __repr__, __eq__ 等 (Python 3.7+)
print("\n13. dataclass:")

from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    age: int
    scores: list = field(default_factory=list)  # 可变默认值要用 field

    @property
    def average(self):
        return sum(self.scores) / len(self.scores) if self.scores else 0

s1 = Student("小明", 18, [90, 85, 95])
s2 = Student("小明", 18, [90, 85, 95])
print("  ", s1)
print("   平均分:", s1.average)
print("   s1 == s2:", s1 == s2)  # dataclass 自动生成 __eq__


# 14. 描述符 (Descriptor) — @property 的底层原理
print("\n14. 描述符:")

class Positive:
    """描述符: 确保值为正数"""
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.storage, 0)

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError(f"{self.name} 不能为负数")
        setattr(obj, self.storage, value)

class Product:
    price = Positive()    # 使用描述符
    quantity = Positive()

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price        # 触发 Positive.__set__
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity

p = Product("苹果", 5, 10)
print(f"   {p.name}: 单价{p.price} 数量{p.quantity} 总价{p.total()}")
# p.price = -1  # ValueError!


# 15. __call__ — 让实例可以像函数一样调用
print("\n15. __call__:")

class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count

counter = Counter()
print("  ", counter())  # 1
print("  ", counter())  # 2
print("  ", counter())  # 3
print("   callable?", callable(counter))  # True


# 16. 上下文管理器 — __enter__ 和 __exit__
print("\n16. 上下文管理器:")

class Timer:
    import time as _time

    def __enter__(self):
        self.start = self._time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = self._time.time() - self.start
        print(f"    耗时: {self.elapsed:.4f}秒")
        return False  # 不吞掉异常

import time
with Timer():
    time.sleep(0.1)
    total = sum(range(100000))
print("   计算结果:", total)


# ============================================================
# 总结: class 知识图谱
# ============================================================
# 基础: __init__, self, 实例属性, 类属性
# 封装: 私有属性 (__), 受保护 (_), @property
# 继承: 单继承, 多重继承, super(), MRO
# 多态: 方法重写, 鸭子类型
# 特殊: @classmethod, @staticmethod, __slots__
# 魔术方法: __str__, __repr__, __add__, __eq__, __len__, __call__
# 高级: ABC 抽象类, dataclass, 描述符, 上下文管理器
# ============================================================
