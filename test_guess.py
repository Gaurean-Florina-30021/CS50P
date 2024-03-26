import pytest
from guess import verify_level, out_of_range, verify_guess
from unittest.mock import patch
import random

MIN_NUMBER = 0
MAX_LEVEL = 5


def test_verify_number():
    # with pytest.raises(ValueError):
    verify_level("6", MIN_NUMBER, MAX_LEVEL) == False
    # with pytest.raises(ValueError):
    verify_level("-2", MIN_NUMBER, MAX_LEVEL) == False
    # with pytest.raises(ValueError):
    verify_level("0", MIN_NUMBER + 1, MAX_LEVEL) == False
    with pytest.raises(ValueError):
        verify_level("Cat", MIN_NUMBER, MAX_LEVEL) == False
    assert verify_level("2", MIN_NUMBER, MAX_LEVEL) == 2
    assert verify_level("5", MIN_NUMBER, MAX_LEVEL) == 5


def test_number_range():
    with patch("builtins.input", return_value="123"):
        assert out_of_range(200, 100) == -1
    with patch("builtins.input", side_effect=["123", "99"]):
        assert out_of_range(200, 100) == 99
    with patch("builtins.input", return_value=["-1", "Red"]):
        with pytest.raises(ValueError):
            assert out_of_range(200, 100)
    with patch("builtins.input", return_value="Cat"):
        with pytest.raises(ValueError):
            assert out_of_range(200, 100)
    with patch("builtins.input", return_value="10"):
        assert out_of_range(200, 100) == 10


def test_verify_guess():
    assert verify_guess("2", 1, 1) == False
    assert verify_guess("10", 10, 2) == True
    with patch("builtins.input", side_effect=["123", "99"]):
        verify_guess("110", 99, 2) == True
    with patch("builtins.input", side_effect=["123", "99"]):
        verify_guess("110", 88, 2) == False
    with pytest.raises(ValueError):
        verify_guess("CAR", 21, 2)

    with patch("basic_functions.generate_numbers", return_value=19) as mock_generate:
        number = mock_generate(3)
        assert verify_guess("19", number, 3) == True
        assert verify_guess("29", number, 3) == False
