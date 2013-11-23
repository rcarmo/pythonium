def func():
    return 1,2,3

def main():
    a = func()
    print(a[0])
    print(a[1])
    print(a[2])

    a,b,c = func()
    print(a)
    print(b)
    print(c)

main()
