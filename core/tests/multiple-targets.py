def func():
    return 1,2,3

def main():
    a = func()
    print(a)

    a,b,c = func()
    print(a)
    print(b)
    print(c)

main()
