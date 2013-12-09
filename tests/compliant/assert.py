assert 1 == 1, 'BAD'

try:
    assert 1 != 2, 'GOOD'
except:
    print(__exception__)

assert 2 == 2

try:
    assert 2 != 3
except:
    print('GOOD')
