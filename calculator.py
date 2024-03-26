from basic_functions import str_to_int, verify_level, generate_numbers

MAX_LEVEL = 5
MIN_LEVEL = 0

OPPERATIONS = ["+", "-", "*", "/"]


def main():
    play_calculator_sw()



# def choose_level(level: str) -> int:
def choose_level():
    """
    This function is only used if the user plays on the software(WITHOUT ANY HARDWARE) and
    it gets the level the user wants to play.

    return: int -> the level what will be played
    """
    level = input("What level do you want to play? ")
    # level = str_to_int(level)
    return verify_level(level, MIN_LEVEL + 1, MAX_LEVEL)


def choose_sign():
    """
    This function is only used if the user plays on the software(WITHOUT ANY HARDWARE) and
    it gets the mathematical symbol. If the user inputs a nonvalid operation symbol than
    the program will raise an error

    return: sign => str -> the mathematical symbol.
    """
    sign = input("What opperation do you want to exercise?\n1.+\n2.-\n3.*\n4./\n")
    sign = str_to_int(sign)
    if 1 <= sign and sign <= 4:
        return OPPERATIONS[sign - 1]
    raise ValueError("Not a valid opperations!")


# def get_opperands(level: int):
def get_opperands(level, opperation):
    """
    This function will create the 2 operands.

    param: level => int -> the level of the game because the opperands will depend
    on the level
    return int[] -> an array with the 2 opperands
    """
    number1 = generate_numbers(level)
    number2 = generate_numbers(level)
    while opperation == "/" and number2 == 0:
        number2 = generate_numbers(level)
    return [number1, number2]


# def check_answear(opperation, level, result, *args) -> bool:
def check_answear(opperation, result, *args):
    """
    This function is used to verify if the user number is the same with the actual
    equation solution

    param: opperation => str -> the mathematical symbol
    param: result => int -> user's solution
    param: *args => int[] -> the array with the operands

    return: bool -> the user's solution is also the actual solution or not
    """
    if result == correct_resp(opperation, *args):
        return True
    return False


def correct_resp(sign, *args):
    """
    This function will calculate the correct answear of the equation

    param: sign => str -> the opperation symbol
    param: args => int[] -> the array with the 2 operands
    return int -> the integet result of the equation
    """
    if sign == "+":
        return args[0] + args[1]
    elif sign == "-":
        return args[0] - args[1]
    elif sign == "*":
        return args[0] * args[1]
    elif sign == "/":
        return int(args[0] / args[1])

def play_calculator_sw():
    level = choose_level()
    level = verify_level(level, MIN_LEVEL + 1, MAX_LEVEL)
    while level == False:
        level = input("Level range [{}, {}]:".format(MIN_LEVEL + 1, MAX_LEVEL))
        level = verify_level(level, MIN_LEVEL + 1, MAX_LEVEL)
    opperation = choose_sign()
    opperations = 10
    lives = 3
    while opperations != 0:
        numbers = get_opperands(level, opperation)
        while lives != 0:
            result = raw_input(("{} {} {} = ".format(numbers[0], opperation, numbers[1])))
            while not result:
                result = raw_input(("{} {} {} = ".format(numbers[0], opperation, numbers[1])))
            result = str_to_int(result)

            # print(result)
            if check_answear(opperation, result, *numbers):
                opperations -= 1
                break
            else:
                lives -= 1
        if lives == 0:
            break
    end_game(lives, correct_resp(opperation, *numbers))

def end_game(lives, number):
    if lives == 0:
        print("Of! You lost! Better Luck next time!\nThe number was {}.".format(number))
    else:
        print("Yey you won and you have left {} lives".format(lives))
if __name__ == "__main__":
    main()
