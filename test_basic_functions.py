from basic_functions import generate_numbers, verify_level, str_to_int, check_range
import pytest


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
    with pytest.raises(ValueError):
        assert check_range(6, 1, 5)
    with pytest.raises(ValueError):
        assert check_range(-2, 1, 5)
    with pytest.raises(ValueError):
        assert check_range(0, 1, 5)
    # assert check_range(6, 1, 5) == False
    # assert check_range(-2, 1, 5) == False
    # assert check_range(0, 1, 5) == False


def test_range():
    with pytest.raises(ValueError):
        assert verify_level("81", 21, 30)
    # assert verify_level("81", 21, 30) == False
    with pytest.raises(
        ValueError, match="Level must be grather than 21 and less than 31!"
    ):
        assert verify_level(31, 21, 30)
    with pytest.raises(
        ValueError, match="Level must be grather than 1 and less than 11!"
    ):
        assert verify_level(0, 1, 10)
    # assert verify_level(81, 21, 30) == False
    # assert verify_level(31, 21, 30) == False
    # assert verify_level(0, 0, 10) == False
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
