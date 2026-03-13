a = {
    'id': 'a12b3c32',
    'name': 'light stick',
    'rooId': 'room_01'
}
for x in a: print(x)
for x in a: print(a[x])

a = range(5, 9, 2)
print(a)
for x in a: print(x)

sum = 0
count = 100
while count > 0:
    sum = sum + count
    count = count -1
print(sum)


for x in range(1, 10):
    for y in range(1 , x + 1):
        print('{} * {} = {}\t'.format(y, x, x*y),  end='')
    print()