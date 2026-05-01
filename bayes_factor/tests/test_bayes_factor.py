import unittest
from bayes_factor import BayesFactor

class TestBayesFactor(unittest.TestCase):
    def setUp(self):
        self.bf_chance = BayesFactor(2, 1)
        self.bf_success = BayesFactor(3, 3)
        self.bf_fail = BayesFactor(3, 0)
    
    # core methods
    def test_likelihood(self):
        self.assertAlmostEqual(self.bf_chance.likelihood(0.5), 0.5)

    def test_evidence_slab(self):
        self.assertAlmostEqual(self.bf_chance.evidence_slab(), 1/3)

    def test_evidence_spike(self):
        self.assertAlmostEqual(self.bf_chance.evidence_spike(), 1/2)

    # input validation/edge cases
    def test_likelihood_thetaError(self):
        with self.assertRaises(TypeError) as exception_context:
            self.bf_chance.likelihood("string")
        self.assertEqual(str(exception_context.exception),
            "Theta must be an integer or float")
        with self.assertRaises(ValueError) as exception_context:
            self.bf_chance.likelihood(-1)
        self.assertEqual(str(exception_context.exception),
            "Theta must be within the range [0, 1]")
        
if __name__ == '__main__':
    unittest.main()