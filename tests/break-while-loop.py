index = 0
while index < 10:
    index += 1
    if index / 2 == 0:
        break
    print(index)


I0 = 0
I1 = 0
while I0 < 10:
    I0 += 1
    while I1 < 10:
        I1 += 1
        if I0 * I1 > 5:
            break
        print(I0, I1)
