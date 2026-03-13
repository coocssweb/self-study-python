a = {
    'id': 'a12b3c32',
    'name': 'light stick',
    'rooId': 'room_01'
}

print('a: ', a)
print("a['id']: ", a['id'])

a['id'] = 'bbbbbbb'
print("a: ", a)

del a['id']
# print("a['id']: ", a['id'])
a['room_name'] = '卧室'
print('a: ', a)

print('len(a): ', len(a))

print('str(a): ', str(a))

print('a.values(): ', a.values())