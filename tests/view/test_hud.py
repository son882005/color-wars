"""Test HUD display and game status rendering."""

import unittest

from src.game.state import GameState
from src.controller import apply_move
from src.engine.rules import PLAYER_BLUE
from src.view.gameplay_scene.hud import get_move_history_entries
from src.view.gameplay_scene.hud import get_control_lines, get_status_lines


class TestHudView(unittest.TestCase):
    """HUD text rendering and info display."""

    def test_control_lines_do_not_contain_difficulty_hotkeys(self):
        """Control hints do not expose difficulty hotkeys."""
        controls = get_control_lines()
        self.assertIn("M: Switch mode", controls)
        self.assertIn("R: Restart", controls)
        self.assertNotIn("1/2/3: EZ/MED/HARD", controls)

    def test_status_lines_include_winner_when_present(self):
        """Winner info appears in HUD when game ends."""
        lines = get_status_lines(game_mode="pvp", difficulty="medium", winner=1)
        self.assertIn("Mode: PVP", lines)
        self.assertIn("Bot: MEDIUM", lines)
        self.assertIn("Winner: Blue", lines)

    def test_move_history_entries_format_recent_moves(self):
        """Recent moves are rendered with player tag and coordinate label."""
        state = GameState()
        apply_move(state, 0, 0, player=PLAYER_BLUE)
        entries = get_move_history_entries(state)

        self.assertEqual(entries[-1], ("B", "A1"))


if __name__ == "__main__":
    unittest.main()
