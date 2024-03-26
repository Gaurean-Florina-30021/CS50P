import time
from remote_control import init_irw, next_key
from lcd_setup import init_lcd
from common_hw_functions import (
    print_navigations,
    game_menu,
    action_choose,
    level_choose,
    play_again,
    decoder,
)
from calculator import get_opperands, check_answear, correct_resp
from basic_functions import verify_level


MAX_LEVEL = 5
MIN_LEVEL = 1
DELAY = 1
OPPERATIONS = ["+", "-", "*", "/"]

lcd = ""


def game_start_calculator(index, lcd1):
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
    if game_index == 1:
        lcd.write_string("Thanks for")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("playing!")
        time.sleep(DELAY)
    else:
        start_game()


def start_game():
    """
    This function is represented by the game itself. The lifespam of this function is
    equal with the game lifespam so until the user decide to not play again.
    """
    lv = level_choose(lcd, MIN_LEVEL, MAX_LEVEL)
    lv = verify_level(lv, MIN_LEVEL, MAX_LEVEL)
    if lv == False:
        return
    opperation_symbol = equation_choose()
    while True:
        play(lv, opperation_symbol)
        if play_again(lcd) == 1:
            break


def play(lv, symbol):
    """
    This function is used to get the guessed value from the usser and compare it
    with the actual value. This function will count how many tries has the user and
    will decide if the player wins or not.

    param: lv => int -> the played level
    param: symbol => str -> the opperation symbol choosed by the user
    """
    # lives = 3
    opperations = 10
    score = 10
    s = OPPERATIONS[symbol]
    while True:
        lives = 3
        op = get_opperands(lv, s)
        while lives != 0:
            result = decode_result(s, *op)
            if check_answear(s, result, *op):
                opperations -= 1
                # score += 1
                break
            else:
                lives -= 1
        if lives == 0:
            opperations -= 1
            resp = correct_resp(s, *op)
            lost(resp, s, *op)
            time.sleep(DELAY)
            score -= 1
            # break
        if opperations == 0:
            break
    # if lives == 0:
        # lost()

    # else:
        # win(3 - lives)
    print_score(score)


def decode_result(sign, *args):
    """
    This function is used to get the number from the lcd and send it to the rest of the functions.

    param: sign => str -> the opperation symbol
    param: args => int[] -> the array with the 2 operands
    return number => int -> the choosed number
    """
    number = 0
    while True:
        print_equation(sign, args[0], args[1])
        lcd.cursor_pos = (1, 0)
        lcd.write_string("{}".format(number))
        key = next_key()
        if key == "EQUAL_BUTTON":
            break
        elif key == "VOLUME_DOWN":
            number -= 1
        else:
            number = decoder(number, key)
    return number


def print_equation(sign, *args):
    """
    This function is used to pint the equation on the first line of the LCD.

    param: sign => str -> the opperation symbol
    param: args => int[] -> the array with the 2 operands
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    # print(sign)
    lcd.write_string("{} {} {} = ".format(args[0], sign, args[1]))


def equation_choose():
    """
    This function is used to get the opperation symbol.

    return: eq => str -> the symbol of the mathematical opperation
    """
    eq = 0
    while True:
        print_navigations(lcd)
        lcd.cursor_pos = (1, 0)
        lcd.write_string("{}. {}!".format(eq + 1, OPPERATIONS[eq]))
        key = next_key()
        eq = get_eguation_symbol(eq, key)
        if key == "PLAY_BUTTON":
            break
    return eq


def get_eguation_symbol(eq, key):
    """
    This function is used to navigate into the available opperation symbols
    """
    if key == "NEXT_BUTTON":
        if eq == 3:
            eq = 0
        else:
            eq += 1
    elif key == "PREV_BUTTON":
        if eq == 0:
            eq = 3
        else:
            eq -= 1
    return eq


def lost(number, sign, *op):
    """
    This function will display a specific message in case of lose. Also it will
    display the equation where the game was lost with its correct answear
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("You lost 1PT!")
    lcd.cursor_pos = (1, 0)
    time.sleep(DELAY)
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("{}{}{}".format(op[0], sign, op[1]))
    lcd.cursor_pos = (1, 0)
    lcd.write_string("={}".format(number))
    time.sleep(DELAY)


def win(tries):
    """
    This function will display on the LCD a specific message in case of win. Also
    it will print how many tries were used to end the game.
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("You WON!")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Used {} tries".format(tries))
    time.sleep(DELAY)

def print_score(score):
    """
    This function will display on the LCD the gained score.
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("SCORE: {}".format(score))
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
    game_start_calculator(index, lcd)


if __name__ == "__main__":
    main()
