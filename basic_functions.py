from random import randint

MIN_NUMBER = 0

# def str_to_int(s: str) -> int:
def str_to_int(s):
    # verify if the entered string can be converted into a number
    """
    This function will change a string into an int. If the string can't be converted
    than the function will raise an error.

    param: s => str/int -> the string from the user (may also be an integer)
    return: s => int -> the int value of the string offered as input
    """
    try:
        s = int(s)
    except ValueError:
        # sys.exit("Not a number!")
        raise ValueError("Not a number!")
    return s


# def verify_range(number : int, min : int, max : int) -> int:
def check_range(number, min, max):
    """
    This function veirifies if a number is in the indicated range

    param: number => int -> the number
    param: min => int -> the minimal value of the interval
    param: max => int -> the maximum value of the interval

    return: bool -> if the number is between min and max or not
    """
    if number < min or number > max:
        return False
        # raise ValueError(
        #     "Level must be grather than {} and less than {}!".format(min, max + 1)
        # )
        # level = input("Level must be grather than {} and less than {}!\nPlease enter a valid level! ".format(MIN_NUMBER, MAX_LEVEL + 1))
        # return verify_level(level)
    else:
        return number
        # return True


# def verify_level(level, min : int, max : int) -> int:
def verify_level(level, min, max):
    """
    This function verifies if the level is in the range or not. If it is in the range it
    will return the number, else it will return False.
    """
    level = str_to_int(level)
    # verify if the entered number is in the range
    return check_range(level, min, max)


# def generate_numbers(level: int) -> int:
def generate_numbers(level):
    """
    This function is used to generate a number inn the specified interval
    """
    number = randint(MIN_NUMBER, 10**level)
    # print(f"{MIN_NUMBER}
    # <= guess <= {10 ** level}")
    return number
