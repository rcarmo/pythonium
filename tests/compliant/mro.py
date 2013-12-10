print(object.mro())

class A: pass
class B(A): pass
class C(B): pass
class D(C): pass
print(D.mro())


class F: pass
class E: pass
class D: pass
class C(D, F): pass
class B(D, E): pass
class A(B, C): pass
print(A.mro())


class F: pass
class E: pass
class D: pass
class C(D, F): pass
class B(E, D): pass
class A(B, C): pass
print(A.mro())


class A: pass
class B: pass
class C: pass
class D: pass
class E: pass
class K1(A, B, C): pass
class K2(D, B, E): pass
class K3(D, A): pass
class Z(K1, K2, K3): pass

for klass in (A, B, C, D, E, K1, K2, K3, Z):
    print(klass.mro())
