from remote_control import next_key

MIN_LEVEL = 1
MAX_LEVEL = 5

action = ["Play", "Back"]
resp = ["Yes", "No"]


# play or back
def action_choose(index, key):
    """
    This function is used to select between to play the game or to go back in
    the case of the Smart Calculator and Guess game.

    param: index => int -> the index of the current action
    param: key -> the key pressed on the remote
    return: index1 => int -> the index of the chosen action
    return: index2 => int -> the index of the next/prev action
    """
    if key == "NEXT_BUTTON":
        if index == 1:
            index = 0
        else:
            index += 1
    elif key == "PREV_BUTTON":
        if index == 0:
            index = 1
        else:
            index -= 1
    elif key == "PLAY_BUTTON":
        return index, index
    return None, index


def game_menu(index, lcd):
    """
    This function is used to print the action menu in a game.

    param: index => int -> the index of the current action
    param: lcd -> the LCD used to print the values
    """
    print_navigations(lcd)
    lcd.cursor_pos = (1, 0)
    txt = "{}. {}!".format(index + 1, action[index])
    lcd.write_string(txt)


def level_choose(lcd, min, max):
    """
    This function will sellect the level that will be played in the case of
    Smart Calculator and Guess game.

    param: lcd -> the LCD where the information will be printed
    return: lv => int -> the level choosed to play
    """
    lv = 1
    while True:
        print_navigations(lcd)
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Level {}!".format(lv))
        key = next_key()
        lv = level_nr(lv, key, min, max)
        if key == "PLAY_BUTTON":
            break
    return lv


def print_navigations(lcd):
    """
    This function is used to display the instruction on how to navigate trough the menus.
    """
    # always clear the LCD
    lcd.clear()
    # set cursor position (if not set automatically starts from the first char on the LCD)
    lcd.cursor_pos = (0, 0)  # line 1 coloumn 3
    # Write text
    lcd.write_string("Use : >>| or |<<")


def level_nr(lv, key, min, max):
    """
    This function will increse, decrese or select the lv depending on the pressed key on the remote.

    param: lv => int -> the current level
    param: key -> the key pressed on the remote
    return: lv -> the prevous/next level
    """
    if key == "NEXT_BUTTON":
        if lv == max:
            lv = min
        else:
            lv += 1
    elif key == "PREV_BUTTON":
        if lv == min:
            lv = max
        else:
            lv -= 1
    return lv


def play_again(lcd):
    """
    This function will help to see if the player wants to play agein or not.

    return: index => int -> the index of the response
    """
    index = 0
    while True:
        print_navigations(lcd)
        lcd.cursor_pos = (1, 0)
        lcd.write_string("{}. {}!".format(index + 1, resp[index]))
        key = next_key()
        if key == "NEXT_BUTTON":
            if index == 1:
                index = 0
            else:
                index += 1
        if key == "PREV_BUTTON":
            if index == 0:
                index = 1
            else:
                index -= 1
        if key == "PLAY_BUTTON":
            return index


def decoder(number, key):
    """
    This function will decode the numbers pressed on the keys.
    """
    aux = -1
    if key == "ZERO_BUTTON":
        aux = 0
    elif key == "ONE_BUTTON":
        aux = 1
    elif key == "TWO_BUTTON":
        aux = 2
    elif key == "THREE_BUTTON":
        aux = 3
    elif key == "FOUR_BUTTON":
        aux = 4
    elif key == "FIVE_BUTTON":
        aux = 5
    elif key == "SIX_BUTTON":
        aux = 6
    elif key == "SEVEN_BUTTON":
        aux = 7
    elif key == "EIGHT_BUTTON":
        aux = 8
    elif key == "NINE_BUTTON":
        aux = 9
    elif key == "HUNDRED_BUTTON":
        number += 100
    elif key == "2HUNDRED_BUTTON":
        number += 200
    elif key == "VOLUME_UP":
        number += 1
    elif key == "VOLUME_DOWN":
        # if number != 0:
            number -= 1
    if aux != -1:
        number = number * 10 + aux
    return number
