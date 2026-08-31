import os
from unittest.mock import patch
import pytest

# Import the functions from your script
from search_tool import search_files, main, get_file_size

def test_get_file_size(tmp_path):
    test_file = tmp_path / "size_test.txt"
    test_file.write_bytes(b"0123456789") 
    
    size_str = get_file_size(str(test_file))
    assert size_str == "10.0 B"

def test_search_files(tmp_path):
    # 1. Create a temporary folder structure
    (tmp_path / "subfolder").mkdir()
    
    # 2. Create dummy files
    (tmp_path / "steam_config.txt").write_text("data")
    (tmp_path / "subfolder" / "SteamApp.exe").write_text("data")
    (tmp_path / "subfolder" / "random_photo.png").write_text("data")
    
    # 3. Run search
    matches = search_files("steam", str(tmp_path))
    
    # 4. Assert correct files are found
    assert len(matches) == 2
    assert any("steam_config.txt" in match for match in matches)
    assert any("SteamApp.exe" in match for match in matches)
    assert not any("random_photo.png" in match for match in matches)

def test_search_files_no_match(tmp_path):
    (tmp_path / "document.pdf").write_text("data")
    matches = search_files("unknown_term", str(tmp_path))
    assert len(matches) == 0

# Mock the UI components from bottom to top
@patch("search_tool.questionary.confirm")
@patch("search_tool.questionary.checkbox")
@patch("search_tool.questionary.path")
@patch("search_tool.questionary.text")
@patch("search_tool.send2trash")
def test_main_full_execution(mock_send2trash, mock_text, mock_path, mock_checkbox, mock_confirm, tmp_path):
    # Setup a test file
    target_file = tmp_path / "steam_test.txt"
    target_file.write_text("dummy data")
    target_path_str = str(target_file)
    
    # Mock the sequential inputs
    mock_text.return_value.ask.return_value = "steam"                 # User inputs search term
    mock_path.return_value.ask.return_value = str(tmp_path)           # User inputs directory
    mock_checkbox.return_value.ask.return_value = [target_path_str]   # User selects the file from the checkbox
    mock_confirm.return_value.ask.return_value = True                 # User confirms deletion (Y)
    
    # Execute main
    main()
    
    # Verify send2trash was targeted at the correct test file
    mock_send2trash.assert_called_once_with(target_path_str)

@patch("search_tool.questionary.text")
def test_main_empty_search(mock_text):
    # Simulate empty search term
    mock_text.return_value.ask.return_value = ""
    main()