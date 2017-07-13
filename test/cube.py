import unittest

import tess

class CubeTestCase(unittest.TestCase):
    def test_superflip(self):
        c = tess.cube.Cube(3)
        c.move([0, 16, 6, 9, 15, 10, 15, 1, 12, 10, 15, 2, 5, 16, 6, 17, 12, 10, 1, 7])
        self.assertTrue(c.cp == list(range(8)))
        self.assertTrue(c.cr == [0] * 8)
        self.assertTrue(c.ep == list(range(12)))
        self.assertTrue(c.er == [False] * 12)

if __name__ == "__main__":
    unittest.main()

""" u r r f b r b b r u u l b b r u' d' r r f l' r b b u u f f"""
""" u r2 f b r b2 r u2 l b2 r u' d' r2 f l' r b2 u2 f2""" # aaaaahhhh it's r' l instead of l' r
""" 0, 16, 6, 9, 15, 10, 15, 1, 12, 10, 15, 2, 5, 16, 6, 14, 15, 10, 1, 7"""
# U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2
# 0,16,6,9,15,10,15,1,12,10,15,2,5,16,6,17,12,10,1,7

#  U  U2  Uc     D  D2  Dc     F  F2  Fc     B  B2  Bc     L  L2  Lc     R  R2  Rc
#  0   1   2     3   4   5     6   7   8     9  10  11    12  13  14    15  16  17
