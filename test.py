#!/usr/bin/env python
a = ["ul", "ur", "dr", "dl", "uf", "ub", "db", "df", "fl", "fr", "br", "bl"]
b = [ 0  ,  1  ,  2  ,  3  ,  4  ,  5  ,  6  ,  7  ,  8  ,  9  ,  10 , 11  ]

def circ(k, indices):
    l = [k[i] for i in indices]
    l.insert(0, l.pop())
    for i in range(len(indices)):
        k[indices[i]] = l[i]
    print(l)
    return k

def crot(cr, indices):
    for i in range(0, len(indices), 2):
        cr[indices[i]] = (cr[indices[i]] + 2) % 3
    for i in range(1, len(indices), 2):
        cr[indices[i]] = (cr[indices[i]] + 1) % 3
    return cr

def erot(cube, axis):
    a = 0 + 4 * axis
    b = 4 + 4 * axis
    for i in range(a, b):
        if i in [cube.ep[a:b]]:
            cube.er[i] = not cube.er[i]
        pass
    return cube


class Cube(object):
    def __init__(self, size):
        self.size = size
        self.cn = ["ufl", "ufr", "ubr", "ubl", "dfl", "dfr", "dbr", "dbl"]
        self.cp = [i for i in range(8)]
        self.cr = [0] * 8
        if size == 3:
            self.en = ["ul", "ur", "dr", "dl", "fl", "fr", "br", "bl", "uf", "ub", "db", "df"]
            self.ep = [i for i in range(12)]
            self.er = [True for i in range(12)]

    def crotate(self, indices):
        l = [self.cn, self.cp, self.cr]
        for i in l:
            circ(i, indices)
        return self

    def erotate(self, indices):
        l = [self.en, self.ep, self.er]
        for i in l:
            circ(i, indices)
        return self

    def F(self):
        crot(self.cr, [0, 1, 5, 4])
        self.crotate([0, 1, 5, 4])
        erot(self, 0)
        self.erotate([8, 5, 11, 4])
        return self

    def F2(self):
        for i in range(2):
            self.F()
        return self

    def Fc(self):
        for i in range(3):
            self.F()
        return self

    def B(self):
        crot(self.cr, [2, 3, 7, 6])
        self.crotate([2, 3, 7, 6])
        erot(self, 0)
        self.erotate([9, 7, 10, 6])
        return self

    def B2(self):
        for i in range(2):
            self.B()
        return self

    def Bc(self):
        for i in range(3):
            self.B()
        return self

    def U(self):
        self.crotate([3, 2, 1, 0])
        erot(self, 1)
        self.erotate([9, 0, 8, 1])
        return self

    def U2(self):
        for i in range(2):
            self.U()
        return self

    def Uc(self):
        for i in range(3):
            self.U()
        return self

    def D(self):
        self.epos([4, 5, 6, 7])
        erot(self, 1)
        self.erotate([11, 2, 10, 3])
        return self

    def D2(self):
        for i in range(2):
            self.D()
        return self

    def Dc(self):
        for i in range(3):
            self.D()
        return self

    def L(self):
        crot(self.cr, [3, 0, 4, 7])
        self.erotate([3, 0, 4, 7])
        return self

    def L2(self):
        for i in range(2):
            self.L()
        return self

    def Lc(self):
        for i in range(3):
            self.L()
        return self

    def R(self):
        crot(self.cr, [1, 2, 6, 5])
        self.erotate([1, 2, 6, 5])
        return self

    def R2(self):
        for i in range(2):
            self.R()
        return self

    def Rc(self):
        for i in range(3):
            self.R()
        return self

    def printit(self):
        for i in [self.cn, self.cp, self.cr, self.en, self.ep, self.er]:
            print i


c = Cube(3)
c.F()
c.printit()
print 12 / 3
