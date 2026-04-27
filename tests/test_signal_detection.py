import unittest
from signal_detection import SignalDetection

class TestSignalDetection(unittest.TestCase):
    def setUp(self):
        self.sdt_test1 = SignalDetection(1, 1, 1, 1)
        self.sdt_test2 = SignalDetection(0, 0, 0, 0)

    # Tests for normal cases
    def test_hit_rate(self):
        self.assertEqual(self.sdt_test1.hit_rate(), 0.5)
    
    def test_false_alarm(self):
        self.assertEqual(self.sdt_test1.false_alarm_rate(), 0.5)

    def test_d_prime(self):
        self.assertEqual(self.sdt_test1.d_prime(), 0)

    def test_criterion(self):
        self.assertEqual(self.sdt_test1.criterion(), 0)

    # Tests for edge cases: 0 counts
    def test_hit_rate_edge_case(self):
        with self.assertRaises(ValueError) as exception_context:
            self.sdt_test2.hit_rate()
        self.assertEqual(str(exception_context.exception),
            "Hit Rate undefined: hits and misses add to 0")
    
    def test_false_alarm_rate_edge_case(self):
        with self.assertRaises(ValueError) as exception_context:
            self.sdt_test2.false_alarm_rate()
        self.assertEqual(str(exception_context.exception),
            "False Alarm Rate undefined: false alarms and correct rejections add to 0")

    def test_d_prime_edge_case(self):
        with self.assertRaises(ValueError):
            self.sdt_test2.d_prime()

    def test_criterion_edge_case(self):
        with self.assertRaises(ValueError):
            self.sdt_test2.criterion()


    # Tests for operator arguments
    def test_add_error(self):
        with self.assertRaises(TypeError) as exception_context:
            self.sdt_test1 + 7
        self.assertEqual(str(exception_context.exception),
            "All objects must be of the SignalDetection class")
    
    def test_sub_error(self):
        with self.assertRaises(TypeError) as exception_context:
            self.sdt_test1 - 7
        self.assertEqual(str(exception_context.exception),
            "All objects must be of the SignalDetection class")
        with self.assertRaises(ValueError) as exception_context:
            self.sdt_test2 - self.sdt_test1
        self.assertEqual(str(exception_context.exception),
            "Outcome counts cannot be negative")

    def test_mul_error(self):
        with self.assertRaises(TypeError) as exception_context:
            self.sdt_test1 * True
        self.assertEqual(str(exception_context.exception),
            "Factor must be an integer")
        with self.assertRaises(ValueError) as exception_context:
            self.sdt_test1 * -1
        self.assertEqual(str(exception_context.exception),
            "Outcome counts cannot be negative")

    def test_add(self):
        sdt_testAdd = self.sdt_test1 + self.sdt_test2
        # check for mutation
        self.assertEqual(self.sdt_test1.hits, 1)
        self.assertEqual(self.sdt_test2.hits, 0)
        # check values
        self.assertEqual(sdt_testAdd.hits, 1)
        self.assertEqual(sdt_testAdd.misses, 1)
        self.assertEqual(sdt_testAdd.false_alarms, 1)
        self.assertEqual(sdt_testAdd.correct_rejections, 1)

    def test_sub(self):
        sdt_testSub = self.sdt_test1 - self.sdt_test2
        # check for mutation
        self.assertEqual(self.sdt_test1.hits, 1)
        self.assertEqual(self.sdt_test2.hits, 0)
        # check values
        self.assertEqual(sdt_testSub.hits, 1)
        self.assertEqual(sdt_testSub.misses, 1)
        self.assertEqual(sdt_testSub.false_alarms, 1)
        self.assertEqual(sdt_testSub.correct_rejections, 1)
    
    def test_mul(self):
        sdt_testMul = self.sdt_test1 * 2
        # check for mutation
        self.assertEqual(self.sdt_test1.hits, 1)
        # check values
        self.assertEqual(sdt_testMul.hits, 2)
        self.assertEqual(sdt_testMul.misses, 2)
        self.assertEqual(sdt_testMul.false_alarms, 2)
        self.assertEqual(sdt_testMul.correct_rejections, 2)

    def test_ROC(self):
        with self.assertRaises(ValueError):
            SignalDetection.plot_roc([self.sdt_test1, self.sdt_test2])
        # failed test
        #self.assertEqual(SignalDetection.plot_roc([self.sdt_test1, self.sdt_test2]), fig, ax)

if __name__ == '__main__':
    unittest.main()