def range(a, b=None):
    if b:
        index = a
        end = b
    else:
        index = 0
        end = a
    out = list()
    print(index, end)
    while index < end:
        print('ok')
        out.append(index)
        index += 1
    return out

LOOPS = range(0)

print(LOOPS.jsobject)
for i in LOOPS:
    print(i.jsobject)
