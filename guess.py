import sys
from basic_functions import str_to_int, verify_level, generate_numbers, check_range

MAX_NUMBER = 10000
MIN_NUMBER = 0
MAX_LEVEL = 5


# if use python grather than 3.5 comment the bellow function definition and uncomment the next:
# def verify_guess(guess: str, generated: int, level: int) -> bool:
def verify_guess(guess, generated, level):
    """
    This function is used to check if the guessed number is equal with the generated number.

    param: guess => int/str -> the player guess
    param: generated => int -> the number that needs to be guessed
    param: lv => int -> the current level

    return: bool -> the player guess is equal with the generated number
    """
    guess = str_to_int(guess)
    guess = out_of_range(guess, 10**level)
    # print(guess)
    if guess == -1:
        return False
    elif guess == generated:
        return True
    return False


# if use python grather tha 3.5 comment the bellow function definition and uncomment the next:
def out_of_range(number, max):
    """
    This function is used to check if the guessed number is in the expected range.
    The function is made to allow user enter a numbur of maximum 3 times to have the number in the
    expected interval.

    param: number => int/str -> the player guess
    param: max => int -> the maximum value the guess can be

    return: number => int -> the player guess
    """
    # def out_of_range(number: int, max: int) -> int:
    tries = 1
    while number > max or number < MIN_NUMBER:
        if tries > 3:
            return -1
        number = input("Out of range! Again: ")

        # can't use str_to_int because of mocking test cases
        try:
            number = int(number)
            # number = decode_Keys(max))
            if check_range(number, MIN_NUMBER, max):
                # print(number)
                return number
        except:
            raise ValueError("Not a number!")
        tries += 1
    return number



def main():
    play_guess_sw()

def play_guess_sw():
   # get the level
    lv = input("What level will you play? ")
    lv = verify_level(lv, MIN_NUMBER, MAX_LEVEL)
    while lv == False:
        lv = input("Level range [{}, {}]:".format(MIN_NUMBER, MAX_LEVEL))
        lv = verify_level(lv, MIN_NUMBER, MAX_LEVEL)
    # generate number
    nr_to_guess = generate_numbers(lv)
    print(nr_to_guess)
    tries = 0
    guess = input("Enter a number: ")
    min = MIN_NUMBER
    max = MAX_LEVEL
    while not verify_guess(guess, nr_to_guess, lv):
        tries += 1
        if tries > 4:
            break
        if nr_to_guess > guess:
            min = guess
        elif nr_to_guess < guess:
            max = guess
        guess = input("Range: [{}, {}]! Enter a number: ".format(min, max))

    if tries == 5:
        print("Too bad you lost!")
        return
    print("Congrats! You have guessed in {} tries".format(tries + 1))
# this shall work for pc tests
if __name__ == "__main__":
    main()
