import unittest
from bayes_factor import BayesFactor

class TestBayesFactor(unittest.TestCase):
    def setUp(self):
        self.bf_chance = BayesFactor(2, 1)
        self.bf_success = BayesFactor(3, 3)
        self.bf_fail = BayesFactor(3, 0)
        self.bf_big_n = BayesFactor(1000000, 0)

    # Input and state validation
    def test_input_type_validation(self):
        with self.assertRaises(TypeError) as exception_context:
            bf_float_n = BayesFactor(1.2, 7)
        self.assertEqual(str(exception_context.exception),
            "n must be an integer")
        with self.assertRaises(TypeError) as exception_context:
            bf_bool_k = BayesFactor(7, True)
        self.assertEqual(str(exception_context.exception), 
            "k must be an integer")
    
    def test_input_range_validation(self):
        with self.assertRaises(ValueError) as exception_context:
            bf_negative_n = BayesFactor(-1, 4)
        self.assertEqual(str(exception_context.exception),
            "n and k cannot be negative")
        with self.assertRaises(ValueError):
            bf_negative_k = BayesFactor(1, -4)
    
    def test_n_larger_than_k_validation(self):
        with self.assertRaises(ValueError) as exception_context:
            bf_big_k = BayesFactor(5, 10)
        self.assertEqual(str(exception_context.exception), 
            "k cannot be larger than n")
    
    # API behavior and return contracts
    def test_likelihood_output(self):
        self.assertAlmostEqual(self.bf_chance.likelihood(0.5), 0.5)
        self.assertIsInstance(self.bf_chance.likelihood(0.5), float)

    def test_evidence_slab_output(self):
        self.assertAlmostEqual(self.bf_chance.evidence_slab(), 1/3)
        self.assertIsInstance(self.bf_chance.evidence_slab(), float)

    def test_evidence_spike_output(self):
        self.assertAlmostEqual(self.bf_chance.evidence_spike(), 1/2)
        self.assertIsInstance(self.bf_chance.evidence_spike(), float)

    def test_bayes_factor_output(self):
        self.assertAlmostEqual(self.bf_chance.bayes_factor(), 3/2)
        self.assertIsInstance(self.bf_chance.bayes_factor(), float)

    # method input validation/edge cases
    def test_likelihood_theta_invalid_type(self):
        with self.assertRaises(TypeError) as exception_context:
            self.bf_chance.likelihood("string")
        self.assertEqual(str(exception_context.exception),
            "Theta must be an integer or float")

    def test_likelihood_theta_invalid_range(self):
        with self.assertRaises(ValueError) as exception_context:
            self.bf_chance.likelihood(-1)
        self.assertEqual(str(exception_context.exception),
            "Theta must be within the range [0, 1]")
        with self.assertRaises(ValueError):
            self.bf_chance.likelihood(1.1)

    def test_zero_likelihood_at_theta_extremes(self):
        self.assertEqual(self.bf_success.likelihood(0), 0)
        self.assertEqual(self.bf_fail.likelihood(1), 0)

    def test_bayes_factor_zero_division(self):
        with self.assertRaises(ValueError) as exception_context:
            self.bf_big_n.bayes_factor()
        self.assertEqual(str(exception_context.exception),
            "Bayes Factor undefined; slab evidence ≈ 0")
        
if __name__ == '__main__':
    unittest.main()