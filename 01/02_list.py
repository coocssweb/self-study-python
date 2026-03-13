
list = ['a', 'b', 'c', 'd', 'e', 'f']
print('list: ', list)
print('list[3]: ', list[3])

print('list[0:3]: ', list[0:3])

print('list[1:3]: ', list[1:3])

list[3] = 'dd'
print("list[3] = 'dd': ", list)

list.append('g')
print("list.append('g'): ", list)

del(list[4])
print("del(list[4]): ", list)

list.insert(4, 'd')
print("list.insert(4, 'd'): ", list)

list.pop()
print("list.pop(): ", list)

list.pop(0)
print("list.pop(0): ", list)

print('list.count: ', list.count('a'))
print('list.index: ', list.index('b'))

print("len(list): ", len(list))
print([1, 2, 3] + [10, 10, 10, 10])
print([1] * 4)
print(3 in [1, 2, 3])

for x in [1, 2, 3]: print(x)