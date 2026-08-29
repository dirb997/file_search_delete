import os
from unittest.mock import patch
import pytest

# Import the functions from the search_tool script
from search_tool import search_files, main

def test_search_files(tmp_path):
    # 1. Create a temporary folder structure inside the pytest environment
    (tmp_path / "subfolder").mkdir()
    
    # 2. Create dummy files
    (tmp_path / "steam_config.txt").write_text("data")
    (tmp_path / "subfolder" / "SteamApp.exe").write_text("data")
    (tmp_path / "subfolder" / "random_photo.png").write_text("data")
    
    # 3. Run the search function
    matches = search_files("steam", str(tmp_path))
    
    # 4. Assert the results are correct and case-insensitive
    assert len(matches) == 2
    assert any("steam_config.txt" in match for match in matches)
    assert any("SteamApp.exe" in match for match in matches)
    assert not any("random_photo.png" in match for match in matches)

def test_search_files_no_match(tmp_path):
    (tmp_path / "document.pdf").write_text("data")
    
    matches = search_files("unknown_term", str(tmp_path))
    
    assert len(matches) == 0

@patch("search_tool.questionary.confirm")
@patch("search_tool.questionary.text")
@patch("search_tool.os.remove")
def test_main_full_execution(mock_remove, mock_text, mock_confirm, tmp_path):
    # 1. Setup a fake file to be "found"
    target_file = tmp_path / "steam_test.txt"
    target_file.write_text("dummy data")
    
    # 2. Mock the text inputs: First ask() returns "steam", second ask() returns the tmp_path
    mock_text.return_value.ask.side_effect = ["steam", str(tmp_path)]
    
    # 3. Mock the confirmation prompt to return True (simulates pressing "Y")
    mock_confirm.return_value.ask.return_value = True
    
    # 4. Execute the main function
    main()
    
    # 5. Verify os.remove was triggered with the correct file path, without actually deleting anything
    mock_remove.assert_called_once_with(str(target_file))

@patch("search_tool.questionary.text")
def test_main_empty_search(mock_text):
    # Simulate the user entering nothing for the search term
    mock_text.return_value.ask.return_value = ""
    
    # The function should exit early and not crash
    main()