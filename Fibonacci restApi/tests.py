import unittest
from callhub import fab_function as fab


class testing(unittest.TestCase):
    def positive_test(self):
        try:
            self.assertEqual(fab(1), 1)
            self.assertEqual(fab(6), 8)
            self.assertEqual(fab(8), 21)
            self.assertEqual(fab(16), 987)
            self.assertEqual(fab(18), 2584)
            self.assertEqual(fab(50), 12586269025)
            self.assertEqual(fab(60), 1548008755920)
            print("All Positive Tests passed")
        except Exception as e:
            print("Positive Test Failed by message ",e)

    def negative_test(self):
        try:
            self.assertNotEqual(fab(1), 0)
            self.assertNotEqual(fab(6), 9)
            self.assertNotEqual(fab(8), 22)
            self.assertNotEqual(fab(16), 986)
            self.assertNotEqual(fab(18), 2525)
            self.assertNotEqual(fab(50), 12586269036)
            print("All Negative Tests passed")
        except Exception as e:
            print("Negative Test Failed by message ",e)


test = testing()
test.positive_test()
test.negative_test()
