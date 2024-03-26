import pytest
from calculator import (
    choose_level,
    choose_sign,
    get_opperands,
    check_answear,
    correct_resp,
)
from unittest.mock import patch


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
