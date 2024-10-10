import unittest
from score_counter import Score

class TestScore(unittest.TestCase):

    def setUp(self):
        """Set up the test environment before each test."""
        self.score_system = Score()

    def test_initial_score(self):
        """Test if the initial score is zero."""
        self.assertEqual(self.score_system.get_score(), 0)

    def test_increase_score(self):
        """Test increasing the score by a specific value."""
        self.score_system.increase(10)
        self.assertEqual(self.score_system.get_score(), 10)

        # Increase by another value and check again
        self.score_system.increase(5)
        self.assertEqual(self.score_system.get_score(), 15)

    def test_reset_score(self):
        """Test resetting the score to zero."""
        self.score_system.increase(20)
        self.score_system.reset()
        self.assertEqual(self.score_system.get_score(), 0)

if __name__ == '__main__':
    # Run the tests with more detailed output
    unittest.main(verbosity=2)
