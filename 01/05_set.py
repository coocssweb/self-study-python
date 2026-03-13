a = set([1, 2, 3, 4])
print('a: ', a)

a.add(5)
print('a:', a)

a.add(5)
print('a:', a)

a.remove(5)
print('a:', a)

b = set([3, 4, 5, 6, 7])

print('a | b: ', a | b)

print('a & b: ', a & b)

print('a - b: ', a - b)

print('b - a: ', b - a)
