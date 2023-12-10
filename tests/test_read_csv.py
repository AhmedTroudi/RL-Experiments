import tempfile
import os
from unittest.mock import mock_open
import pytest
import numpy as np
from src.rl_experiments.helper import read_csv


def test_data_shape_and_type():
    # Create a temporary CSV file for testing
    csv_content = "1,2,3\n4,5,6\n7,8,9"
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as temp_csv:
        temp_csv.write(csv_content)
        temp_csv_path = temp_csv.name

    try:
        data = read_csv(temp_csv_path)

        # Check if the data is a NumPy array with the expected shape
        assert isinstance(data, np.ndarray)
        assert data.shape == (3, 3)

    finally:
        # Clean up: Delete the temporary CSV file
        os.remove(temp_csv_path)


def test_file_not_found():
    # Test when the specified file is not found
    with pytest.raises(FileNotFoundError):
        read_csv("nonexistent_file.csv")


def test_permission_error(mocker):
    # Use mocker.patch to replace the built-in open function with a mock
    mock_open_func = mock_open()
    mocker.patch("builtins.open", mock_open_func)

    # Set the side_effect to simulate a PermissionError
    mock_open_func.side_effect = PermissionError("Permission denied")

    # Test the function with a mocked file open operation
    with pytest.raises(PermissionError,
                       match="Permission error: Unable to open the file dummy_file.csv."):
        read_csv("dummy_file.csv")
