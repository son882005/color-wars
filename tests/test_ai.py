import unittest

from src.ai.ai import get_ai_move


class TestAI(unittest.TestCase):
    def test_ai_returns_none_when_no_valid_moves(self):
        board = [
            [1, 1],
            [1, 1],
        ]
        dots = [
            [1, 1],
            [1, 1],
        ]

        move = get_ai_move(board, dots)

        self.assertIsNone(move)


if __name__ == "__main__":
    unittest.main()
