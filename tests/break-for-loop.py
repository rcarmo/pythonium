for i in [1,2,3]:
    print(i)
    if i == 2:
        break

for i in [1,2,3]:
    print(i)
    for j in [3,4,5]:
        print(i*j)
        if i*j > 8:
            print('youpla!')
            break
