a = [i*j for i in [1,2,3,4,5,6] if i % 2 == 0 for j in [1,2,3]  if j >= 3]
for i in a:
    print(i)
