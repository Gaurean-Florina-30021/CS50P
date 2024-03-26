from remote_control import init_irw, next_key
from lcd_setup import init_lcd
from guess import verify_guess
from basic_functions import verify_level, generate_numbers, check_range
import time
from common_hw_functions import (
    decoder,
    level_choose,
    action_choose,
    play_again,
    print_navigations,
    game_menu,
)
from basic_functions import verify_level, generate_numbers


MAX_NUMBER = 10000
MIN_NUMBER = 0
MAX_LEVEL = 5
DELAY = 2
lcd = ""


def game_start_guess(index, lcd1):
    """
    This function will run as long as the game is in progress. This function is used
    to choose if the player really wants to play this game or would rather go back.

    param: index => int -> the index of the firs action
    param: lcd -> the initialized LCD. If it is already initialized it is not
    necessary to initialize it again.
    """
    global lcd
    if lcd == "":
        lcd = lcd1
    game_index = None
    while True:
        game_menu(index, lcd)
        key = next_key()
        game_index, index = action_choose(index, key)
        if game_index != None:
            break
    lcd.clear()
    lcd.cursor_pos = (0, 0)  # line 1 coloumn 0
    if game_index == 0:
        start_game()


def start_game():
    """
    This function is represented by the game itself. The lifespam of this function is
    equal with the game lifespam so until the user decide to not play again.
    """
    lv = level_choose(lcd, MIN_NUMBER + 1, MAX_LEVEL)
    lv = verify_level(lv, MIN_NUMBER + 1, MAX_LEVEL)
    if lv == False:
        return
    while True:
        nr_to_guess = generate_numbers(lv)
        play(lv, nr_to_guess)
        if play_again(lcd) == 1:
            break


def play(lv, nr_to_guess):
    """
    This function is used to get the guessed value from the usser and compare it
    with the actual value. This function will count how many tries has the user and
    will decide if the player wins or not.

    param: lv => int -> the played level
    param: nr_to_guess => int -> the number that needs to be guessed
    """
    min = 0
    max = 10**lv
    guess = decode_Keys(min, max)
    tries = 0

    while not verify_guess(guess, nr_to_guess, lv):
        if guess < nr_to_guess:
            min = guess
        elif guess > nr_to_guess:
            max = guess
        tries += 1
        if tries > 4:
            break
        guess = decode_Keys(min, max)

    if tries == 5:
        lost(nr_to_guess)
    else:
        win(tries + 1)


def decode_Keys(min, max):
    """
    This function will decode the number entered and will check if the number is in the specified
    interval. If not, than the user will have 2 other chances before actually lose one life.
    """
    number = 0
    tries = 3
    while True:
        number = get_number(0, min, max)
        if check_range(number, min, max):
            break
        else:
            # if number > max or number < min:
            tries -= 1
            print_out_of_range(tries)
            print_range(min, max)
            lcd.cursor_pos = (1, 0)
            lcd.write_string("{}".format(number))
        if tries == 0:
            break
    if number > max:
        return max
    elif number < min:
        return min
    return number


def print_range(min, max):
    """
    This function is used to print the actual range on the LCD

    param: min => int -> the minimal value
    param: max => int -> the maximum value
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("{}<=x<={}".format(min, max))


def print_out_of_range(tries):
    """
    This function displays on the LCD a message if the user enter a number out of range

    param: tries => int -> the number of tries left
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Out of range!")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("{} tries left".format(tries))
    time.sleep(DELAY)


def get_number(number, min, max):
    """
    This function is used to get the number from the lcd and send it to the rest of the functions.

    param: number => int -> the current value for the number
    param: min => int -> the minimal value for the number
    param: max => int -> the maximal value for the number
    """
    while True:
        print_range(min, max)
        lcd.cursor_pos = (1, 0)
        lcd.write_string("{}".format(number))
        key = next_key()
        if key == "EQUAL_BUTTON":
            break
        else:
            number = decoder(number, key)
    return number


def lost(number):
    """
    This function print a corresponding message on the lcd in case of lose.

    param: number => int -> the value for the number that needed to be guessed
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("You lost!")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Nr: {}".format(number))
    time.sleep(DELAY)


def win(tries):
    """
    This function print a corresponding message on the lcd in case of win.

    param: tries => int -> the number of tries left
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("You WON!")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Used {} tries".format(tries))
    time.sleep(DELAY)


def main():
    init_irw()
    global lcd
    lcd = init_lcd()
    lcd.clear()
    lcd.cursor_pos = (0, 0)  # line 1 coloumn 3
    # Write text
    print_navigations(lcd)
    index = 0
    game_start_guess(index, lcd)


if __name__ == "__main__":
    main()
