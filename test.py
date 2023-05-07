import unittest
from fibonacci import fibonacci

class TestFibonacci(unittest.TestCase):

    def test_fibonacci(self):
        self.assertEqual(fibonacci(1), [0])
        self.assertEqual(fibonacci(2), [0, 1])
        self.assertEqual(fibonacci(5), [0, 1, 1, 2, 3])
        self.assertEqual(fibonacci(7), [0, 1, 1, 2, 3, 5, 8])

    def test_negative(self):
        with self.assertRaises(ValueError):
            fibonacci(-1)
        with self.assertRaises(ValueError):
            fibonacci(0)

if __name__ == '__main__':
    unittest.main()