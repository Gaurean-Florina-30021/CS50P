import pytest
from guess import verify_level, out_of_range, verify_guess
from unittest.mock import patch
from calculator import (
    choose_level,
    choose_sign,
    get_opperands,
    check_answear,
    correct_resp,
)
from basic_functions import generate_numbers, verify_level, str_to_int, check_range


"""
For GUESS
"""
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

"""
For CALCULATOR
"""
def test_verify_number_c():
    with patch("builtins.input", return_value="6"):
        # with pytest.raises(ValueError):
        assert choose_level() == False
    with patch("builtins.input", return_value="-2"):
        # with pytest.raises(ValueError):
        assert choose_level() == False
    with patch("builtins.input", return_value="0"):
        # with pytest.raises(ValueError):
        assert choose_level() == False
    with patch("builtins.input", return_value="Cat"):
        with pytest.raises(ValueError):
            choose_level()
    with patch("builtins.input", return_value=2):
        assert choose_level() == 2
    with patch("builtins.input", return_value=5):
        assert choose_level() == 5
    with patch("builtins.input", return_value=100):
        # with pytest.raises(ValueError):
        assert choose_level() == False



def test_verify_sign():
    with patch("builtins.input", return_value="something"):
        with pytest.raises(ValueError, match="Not a valid opperations!"):
            assert choose_sign()
    with patch("builtins.input", return_value="+"):
        assert choose_sign() == "+"
    with patch("builtins.input", return_value="-"):
        assert choose_sign() == "-"
    with patch("builtins.input", return_value="*"):
        assert choose_sign() == "*"
    with patch("builtins.input", return_value="/"):
        assert choose_sign() == "/"
    with patch("builtins.input", return_value="**"):
        with pytest.raises(ValueError, match="Not a valid opperations!"):
            assert choose_sign()


def test_opperands():
    operands = get_opperands(1, "+")
    for element in operands:
        assert element <= 10 and element >= 0
    operands = get_opperands(2, "/")
    assert operands[1] != 0
    for element in operands:
        assert element <= 100 and element >= 0
    operands = get_opperands(3, "*")
    for element in operands:
        assert element <= 1000 and element >= 0
    operands = get_opperands(4, "-")
    for element in operands:
        assert element <= 10000 and element >= 0
    operands = get_opperands(5, "+")
    for element in operands:
        assert element <= 100000 and element >= 0
    operands = get_opperands(6, "/")
    assert operands[1] != 0
    for element in operands:
        assert element < 1000000 and element >= 0


def test_answear():
    with patch("builtins.input", result=2):
        assert check_answear("+", 2, 1, 1) == True
    with patch("builtins.input", result=24):
        assert check_answear("*", 24, 2, 12) == True
    with patch("builtins.input", result=-3):
        assert check_answear("-", -3, 21, 24) == True
    with patch("builtins.input", result=0):
        assert check_answear("/", 2, 0, 1) == False
    with patch("builtins.input", result=0):
        assert check_answear("/", 0, 0, 1) == True
    with patch("builtins.input", result=0):
        assert check_answear("/", 5, 4, 1) == False
    with patch("builtins.input", result=2):
        assert check_answear("+", -5, 0, 1) == False
    with patch("builtins.input", result=24):
        assert check_answear("*", 1, 30, 12) == False
    with patch("builtins.input", result=-3):
        assert check_answear("-", 1, 44, 24) == False


def test_corresct_resp():
    assert correct_resp("+", 1, 1) == 2
    assert correct_resp("-", 44, 24) == 20
    assert correct_resp("*", 2, 12) == 24
    assert correct_resp("/", 0, 1) == 0
    assert correct_resp("+", 0, 1) == 1

"""
For BASIC FUNCTIONS
"""
def test_geterate():
    assert generate_numbers(2) <= 100
    assert generate_numbers(2) >= 0
    assert generate_numbers(1) >= 0
    assert generate_numbers(5) >= 0
    assert generate_numbers(3) <= 1000
    assert generate_numbers(4) <= 10000
    assert generate_numbers(5) <= 100000
    assert generate_numbers(1) <= 10
    assert generate_numbers(1) <= 10
    assert generate_numbers(1) <= 10
    assert generate_numbers(1) <= 10
    assert generate_numbers(1) <= 10
    assert generate_numbers(1) <= 10


def test_check_range():
    with pytest.raises(TypeError):
        assert check_range("31", 21, 30)
    assert check_range(1, 0, 10) == 1
    # with pytest.raises(ValueError):
    #     assert check_range(6, 1, 5)
    # with pytest.raises(ValueError):
    #     assert check_range(-2, 1, 5)
    # with pytest.raises(ValueError):
        # assert check_range(0, 1, 5)
    assert check_range(6, 1, 5) == False
    assert check_range(-2, 1, 5) == False
    assert check_range(0, 1, 5) == False


def test_range():
    # with pytest.raises(ValueError):
        # assert verify_level("81", 21, 30)
    assert verify_level("81", 21, 30) == False
    # with pytest.raises(
    #     ValueError, match="Level must be grather than 21 and less than 31!"
    # ):
        # assert verify_level(31, 21, 30)
    # with pytest.raises(
    #     ValueError, match="Level must be grather than 1 and less than 11!"
    # ):
    #     assert verify_level(0, 1, 10)
    assert verify_level(81, 21, 30) == False
    assert verify_level(31, 21, 30) == False
    assert verify_level(0, 0, 10) == False
    assert verify_level(1, 0, 10) == 1
    assert verify_level(10, 0, 11) == 10
    assert verify_level("10", 0, 11) == 10
    assert verify_level(41, 12, 48) == 41


def test_int_conversion():
    assert str_to_int("11") == 11
    assert str_to_int(551) == 551
    assert str_to_int("-21") == -21
    assert str_to_int("0") == 0
    with pytest.raises(ValueError, match="Not a number!"):
        assert str_to_int("Cat")
    with pytest.raises(ValueError, match="Not a number!"):
        assert str_to_int("Hello World!")
