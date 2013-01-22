class A(object):
    def __init__(self):
        print "A.__init__"
    def a(self):
        print "A.a"

class Mixin(object):
    def __init__(self):
        print "Mixin.__init__"
    def a(self):
        print "Mixin.a"

class C(A,Mixin):
    """
    Demonstrates that A.a is not overriden by Mixin.a when
    mixin is second class.
    """
    def __init__(self):
        print "C.__init__"

class D(Mixin,A):
    def __init__(self):
        print "D.__init__"

class E(Mixin,A):
    """
    Demonstrates that A.__init__ is not caused when use
    mixin as first class.
    """

    def __init__(self):
        super(E, self).__init__()
        print "E.__init__"

c = C()
c.a()

d = D()
d.a()

e = E()
e.a()
