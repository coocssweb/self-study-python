a = 50
b = 30
if a > 80:
    print('a > 80')
elif a > 25 and b > 30:
    print('a > 25  and b > 30')
elif a > 25 and b > 10:
    print('a > 25 and b > 10')
else:
    print('a <= 25')




if a > 40:
    if b > 30:
        print('a > 40 并且 b > 30')
    else:
        print('a > 40 并且 b <= 30')
else:
    print('a <= 40')