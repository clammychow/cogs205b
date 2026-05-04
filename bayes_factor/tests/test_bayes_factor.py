import unittest
from bayes_factor import BayesFactor

class TestBayesFactor(unittest.TestCase):
    def setUp(self):
        self.bf_chance = BayesFactor(2, 1)
        self.bf_success = BayesFactor(3, 3)
        self.bf_fail = BayesFactor(3, 0)
        self.bf_big_n = BayesFactor(1000000, 0)
        self.bf_zeros = BayesFactor(0, 0)

    # Input and state validation
    def test_initialization(self):
        self.assertEqual(self.bf_chance.n, 2)
        self.assertEqual(self.bf_chance.k, 1)

    def test_invalid_n_type(self):
        with self.assertRaises(TypeError) as exception_context:
            bf_float_n = BayesFactor(7.2, 1)
        self.assertEqual(str(exception_context.exception),
            "n must be an integer")
        with self.assertRaises(TypeError):
            bf_bool_n = BayesFactor(True, 1)

    def test_invalid_k_type(self):
        with self.assertRaises(TypeError) as exception_context:
            bf_float_k = BayesFactor(7, 1.2)
        self.assertEqual(str(exception_context.exception), 
            "k must be an integer")
        with self.assertRaises(TypeError):
            bf_bool_k = BayesFactor(7, False)
    
    def test_invalid_n_range(self):
        with self.assertRaises(ValueError) as exception_context:
            bf_negative_k = BayesFactor(-1, 7)
        self.assertEqual(str(exception_context.exception),
            "n and k cannot be negative")
    
    def test_invalid_k_range(self):
        with self.assertRaises(ValueError) as exception_context:
            bf_negative_k = BayesFactor(1, -7)
        self.assertEqual(str(exception_context.exception),
            "n and k cannot be negative")
    
    def test_n_larger_than_k(self):
        with self.assertRaises(ValueError) as exception_context:
            bf_big_k = BayesFactor(5, 10)
        self.assertEqual(str(exception_context.exception), 
            "k cannot be larger than n")
    
    # API behavior and return contracts
    def test_methods_callable(self):
        self.assertIsCall
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
            self.bf_chance.likelihood("0.5")
        self.assertEqual(str(exception_context.exception),
            "Theta must be an integer or float")

    def test_likelihood_theta_invalid_range(self):
        with self.assertRaises(ValueError) as exception_context:
            self.bf_chance.likelihood(-1)
        self.assertEqual(str(exception_context.exception),
            "Theta must be within the range [0, 1]")
        with self.assertRaises(ValueError):
            self.bf_chance.likelihood(1.1)

    def test_likelihood_at_theta_extremes(self):
        self.assertEqual(self.bf_fail.likelihood(0), 1)
        self.assertEqual(self.bf_success.likelihood(1), 1)
    
    def test_impossible_likelihood_at_theta_extremes(self):
        self.assertEqual(self.bf_success.likelihood(0), 0)
        self.assertEqual(self.bf_fail.likelihood(1), 0)

    def test_bayes_factor_zero_division(self):
        with self.assertRaises(ValueError) as exception_context:
            self.bf_big_n.bayes_factor()
        self.assertEqual(str(exception_context.exception),
            "Bayes Factor undefined; slab evidence ≈ 0")

    def test_bayes_factor_same_prior(self):
        self.assertAlmostEqual(self.bf_zeros.evidence_spike(), self.bf_zeros.evidence_slab())
        self.assertAlmostEqual(self.bf_zeros.bayes_factor(), 1)

    # intentionally failing test
    def test_evidence_spike_bounds(self):
        self.assertAlmostEqual(b - a, 0)
        
if __name__ == '__main__':
    unittest.main()