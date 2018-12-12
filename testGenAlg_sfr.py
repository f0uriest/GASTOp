import unittest
import numpy as np
import numpy.testing as npt

import GenAlg
import Truss

class TestGenAlg(unittest.TestCase):

    def testTruss(self):
        GA = GenAlg()
        pop_test = GA.initialize_population(10)

        fos = [i.fos for i in pop_test] #extracts fos for each truss object in population


        #note to susan: look up map() and filter()
if __name__ == "__main__":
    unittest.main()
