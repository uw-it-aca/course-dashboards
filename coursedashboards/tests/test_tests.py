from unittest import TestCase


# Just a dummy test to make sure our travis builds will have something to run
class TestTestRunner(TestCase):

    def test_tests(self):
        self.assertEqual(2, 1 + 1)