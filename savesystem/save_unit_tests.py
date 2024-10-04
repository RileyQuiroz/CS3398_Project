import unittest
import os
import json
from unittest.mock import patch, mock_open
from save_progress import save_game
from load_progress import load_game


class TestSaveLoadGameState(unittest.TestCase):

    def setUp(self):
        self.save_state = {
            "player_health": 3,
            "current_level": 0,
            "current_weapon": 0,
            "ship_color": 0,
            "score": 0,
            "finish_time": 0
        }
        self.save_file = 'save_data_test.json'
        self.file_path = os.path.join('savesystem/savedata', self.save_file)
        
    # Test if data is saved correctly
    @patch("builtins.open", new_callable=mock_open)
    def test_save_game(self, mock_file):
        save_game(self.save_state, self.save_file)
        mock_file.assert_called_once_with(self.file_path, 'w')

    # Test that loading the game state from a file returns proper data
    @patch("builtins.open", new_callable=mock_open, read_data='{"player_health": 3, "current_level": 0, "current_weapon": 0, "ship_color": 0, "score": 0, "finish_time": 0}')
    @patch("os.path.getsize", return_value=100)
    def test_load_game(self, mock_getsize, mock_file):
        loaded_state, _ = load_game(self.save_file)
        self.assertEqual(loaded_state, self.save_state)

    # Test loading when there is no save data
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.getsize", return_value=0)
    def test_load_game_no_data(self, mock_getsize, mock_file):
        loaded_state, _ = load_game(self.save_file)
        self.assertIsNone(loaded_state)

    # Test loading from a corrupted/invalid JSON save file
    @patch("builtins.open", new_callable=mock_open, read_data='corrupted data')
    @patch("os.path.getsize", return_value=100)
    def test_load_game_corrupted_file(self, mock_getsize, mock_file):
        with self.assertRaises(json.JSONDecodeError):
            load_game(self.save_file)


if __name__ == '__main__':
    unittest.main()