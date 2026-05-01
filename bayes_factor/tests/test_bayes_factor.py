import unittest
from bayes_factor import BayesFactor

class TestBayesFactor(unittest.TestCase):
    def setUp(self):
        self.bf_1 = BayesFactor(2, 1)
    
    # core methods
    def test_likelihood(self):
        self.assertAlmostEqual(self.bf_1.likelihood(0.5), 0.5)

    def test_evidence_slab(self):
        self.assertAlmostEqual(self.bf_1.evidence_slab(), 1/3)

    # input validation/edge cases
    def test_likelihood_thetaError(self):
        with self.assertRaises(TypeError) as exception_context:
            self.bf_1.likelihood("string")
        self.assertEqual(str(exception_context.exception),
            "Theta must be an integer or float")
        with self.assertRaises(ValueError) as exception_context:
            self.bf_1.likelihood(-1)
        self.assertEqual(str(exception_context.exception),
            "Theta must be within the range [0, 1]")
        
if __name__ == '__main__':
    unittest.main()