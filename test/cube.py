import unittest

import tess

class CubeTestCase(unittest.TestCase):
    def test_superflip(self):
        c = tess.cube.Cube(3)
        tess.cube.move(c, [6, 16, 0, 3, 15, 4, 15, 7, 12, 4, 15, 8, 11, 16, 0, 17, 12, 4, 7, 1])
        self.assertTrue(c.cp == list(range(8)))
        self.assertTrue(c.cr == [0] * 8)
        self.assertTrue(c.ep == list(range(12)))
        self.assertTrue(c.er == [False] * 12)

if __name__ == "__main__":
    unittest.main()