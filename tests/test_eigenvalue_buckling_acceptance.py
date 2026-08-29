from __future__ import annotations
import math
import unittest
from scripts.structural.run_eigenvalue_buckling_acceptance import mode_vectors

class EulerBucklingTests(unittest.TestCase):
    def critical(self,E=70e9,b=.01,h=.01,L=.2,K=2.0):
        return math.pi**2*E*(b*h**3/12)/(K*L)**2
    def test_declared_cantilever_reference_and_scaling(self):
        base=self.critical();self.assertAlmostEqual(3598.2932712304946,base)
        self.assertAlmostEqual(2*base,self.critical(E=140e9))
        self.assertAlmostEqual(base/4,self.critical(L=.4))
        self.assertAlmostEqual(8*base,self.critical(h=.02))
    def test_frd_displacement_mode_parser(self):
        text="""  100CL  102 3.7E+01 2 4 2 1
 -4  DISP        4    1
 -5  D1          1    2    1    0
 -1         1 1.00000E-03 2.00000E-03-3.00000E-03
 -1         2 0.00000E+00 4.00000E-03 5.00000E-03
 -3
"""
        modes=mode_vectors(text);self.assertEqual(1,len(modes));self.assertEqual((.001,.002,-.003),modes[0][1][0])
if __name__=='__main__':unittest.main()
