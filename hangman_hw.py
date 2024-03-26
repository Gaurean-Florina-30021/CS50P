import csv
import time
from remote_control import init_irw, next_key
from lcd_setup import init_lcd
from common_hw_functions import (
    level_nr,
    level_choose,
    play_again,
    print_navigations,
)
from hangman import (
    verify_file,
    read_data,
    save_word,
    verify_letter,
    replace_letter,
    wd_to_guess,
)

g_word = []
lcd = ""

MIN_LEVEL = 1
MAX_LEVEL = 8

actions = ["Play!", "Add!", "Delete!", "Back!"]


def game_start_hangman(index, lcd1):
    """
    This function will run as long as the game is in progress. This function is used
    to choose if the player really wants to play this game or would rather go back.
    In addition the player can append additional words or remove words from the dictionaries

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
        if key == "PLAY_BUTTON":
             game_index = index

        index = level_nr(index, key, 0, len(actions) - 1)
        if game_index == 0 or game_index == 3:
            break
        if game_index == 1:

            add_word()
        if game_index == 2:

            lv = level_choose(lcd, MIN_LEVEL, MAX_LEVEL)
            remove_word(lv)
        game_index = None
    if game_index == 0:
        lv = level_choose(lcd, MIN_LEVEL, MAX_LEVEL)
        play_game(lv)

def game_menu(index, lcd):
    """
    This function is used to print the action menu in a game.

    param: index => int -> the index of the current action
    param: lcd -> the LCD used to print the values
    """
    print_navigations(lcd)
    lcd.cursor_pos = (1, 0)
    txt = "{}. {}!".format(index + 1, actions[index])
    lcd.write_string(txt)


def add_word():
    """
    This function will add a word in a dictionary depending on the lenght
    """
    # word =[]
    word = read_word()
    sure_add(word)
    word = word.lower()
    sure = play_again(lcd)
    if sure == 0:
        response = "Yes"
    else:
        response = "No"
    status = save_word(word, response)
    print_status(status)


def read_word():
    """
    This function will read, using the remote controll the word the user want to add
    in the dictionary.

    retrun: word -> str => the word the user want to add
    """
    word = ""
    index = ord("A")
    letter = None
    while True:
        print_navigations(lcd)
        lcd.cursor_pos = (1, 0)
        lcd.write_string("{}|{}".format(word, chr(index)))
        key = next_key()
        letter, index = choose_letter(key, index)
        if letter != None:
            word += letter
        if key == "PLAY_BUTTON":
            break
    return word


def choose_letter(key, index):
    """
    This function helps to choose the letters even if it is about the adding process
    or during the guessing process.

    param: key => str => the presssed key on the remote control
    param: index => int -> the index of the current letter

    return: If the letter was selected than it returns the selected character index and
    the index of the "A" letter. If not it will return None and the index of the current
    character.
    """
    first_nr = ord("A")
    last_nr = ord("Z")
    if key == "NEXT_BUTTON":
        if last_nr == index:
            index = first_nr
        else:
            index += 1
    elif key == "PREV_BUTTON":
        if first_nr == index:
            index = last_nr
        else:
            index -= 1
    elif key == "EQUAL_BUTTON":
        return chr(index), first_nr
    return None, index


def sure_add(word):
    """
    This function will display a message to verify if the user is sure about adding
    the specified word. In case of mistakes.

    param: word => str -> the word that the user wants to add
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('"{}" will'.format(word.upper()))
    lcd.cursor_pos = (1, 0)
    lcd.write_string("be added!")
    time.sleep(2)
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Are you")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("sure?")
    time.sleep(1)


def print_status(status):
    """
    This function will print a message on the LCD depending on the returned value from the
    adding function
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    if status == -3:
        lcd.write_string("Too big or too")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("small word!")
    elif status == -2:
        lcd.write_string("Dictionary is")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("full!")
    elif status == -1:
        lcd.write_string("Already in")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("list!")
    else:
        lcd.write_string("Success!")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(":)")
    time.sleep(1)


def remove_word(lv):
    """
    This function is used to remove a specific word from a specific level.

    param: lv => int -> the levek from where the user wants to remove a word
    """
    name = str(lv) + ".csv"
    file = verify_file(name, "r")
    if file == -1:
        print_no_file()
        return -1
    words = read_data(file)
    word_list = [d["word"] for d in words]
    rm_word = choose_word(word_list)
    sure = None
    if rm_word != None:
        sure_rm(rm_word)
        lcd.cursor_pos = (0, 0)
        sure = play_again(lcd)
    if sure == 0:
        word_list = erase(rm_word, words)
        with open(name, "w") as file1:
            writer = csv.DictWriter(file1, fieldnames=["index", "word"])
            writer.writeheader()
            for d in word_list:
                writer.writerow({"index": d["index"], "word": d["word"]})


def print_no_file():
    """
    This function display a message in case the user tries to open a file that do
    not exist during the earasing process. Eg.: The level 7 file was not yet created.
    Also it prints a solution for this problem
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Not such file")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Add words!")


def erase(rm_word, words):
    """
    This function will remove the word specified from the word list.

    param: rm_word => str -> the word user wantsto remove
    param: words => str[] -> the list of words present in dictionary
    return: new_dict[] => str[] -> the new list of words without the rm_word in it
    """
    new_dict = []
    for d in words:
        # print(d, d['word'])
        if d["word"] != rm_word:
            new_dict.append({"index": d["index"], "word": d["word"]})
    return new_dict


def choose_word(word_list):
    """
    This function is used to choose the word during the earasing procees

    param: word_list => str[] -> the list of words in this level
    return: str -> the word choosed by the user
    """
    index = 0
    last_index = len(word_list)
    if last_index < 10:
        not_enough()
        return None
    while True:
        print_navigations(lcd)
        lcd.cursor_pos = (1, 0)
        lcd.write_string("{}. {}".format(index + 1, word_list[index]))
        key = next_key()
        index = navigate_words(index, last_index, key)
        if key == "PLAY_BUTTON":
            break
    return word_list[index]


def not_enough():
    """
    This function is used to print a message in case the user wants to remove words from list
    but the list contains less than 10 words(Safety measure to prevent leaving a list completely empty)
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Not enough")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("words!")


def sure_rm(word):
    """
    This function will display a message to verify if the user is sure about remiving
    the specified word. In case of mistakes.

    param: word => str -> the word that the user wants to remove
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('"{}" will'.format(word.upper()))
    lcd.cursor_pos = (1, 0)
    lcd.write_string("be removed")
    time.sleep(2)
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Are you")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("sure?")
    time.sleep(1)


def navigate_words(index, last, key):
    """
    This function helps to navigate into the words list so this way the list will not be
    exedeed.

    param: index => int -> the index of the current word in the list
    param: last => int -> the index of the last word
    param: key => str -> the key pressed on the remote control
    return: index => int -> the index of the next element in the list. If the current
    element is the last one than the function will return the first index.
    """
    if key == "NEXT_BUTTON":
        if index == last - 1:
            index = 0
        else:
            index += 1
    elif key == "PREV_BUTTON":
        if index == 0:
            index = last - 1
        else:
            index -= 1
    return index


def play_game(lv):
    """
    This function is represented by the game itself. The lifespam of this function is
    equal with the game lifespam so until the user decide to not play again.
    """
    guessed = []
    tries = 5
    index = ord("A")
    while True:
        word, last_i = wd_to_guess(lv)
        if last_i == 0 and word == None:
            # if last_i == 0:
            not_enough()
            time.sleep(0.5)
            break
        for letter in word:
            guessed.append("_")
        while tries != 0:
            print_enigma("".join(guessed), tries)
            lcd.cursor_pos = (1, len(word))
            lcd.write_string("|{}".format(chr(index)))
            key = next_key()
            letter, index = choose_letter(key, index)
            if letter != None:
                letter = letter.lower()
                if not verify_letter(letter, word):
                    tries -= 1
                else:

                    guessed = replace_letter(word, guessed, letter)
            if not ("_" in guessed):
                break
        if tries == 0:
            lost(word)
        else:
            win(tries)
        if play_again(lcd) == 1:
            break
        else:
            guessed = []
            tries = 5
            index = ord("A")


def print_enigma(word, tries):
    """
    This function is used to display on the LCD the numbers of tries remaining
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("{} tries left!".format(tries))
    lcd.cursor_pos = (1, 0)
    lcd.write_string("{}".format("".join(word)))


def lost(word):
    """
    This function is used to print on the LCD a specific message in case of lose.
    Also this function will reveal the word that needed to be guessed.

    param: word => str -> the word that the user did not guessed
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("You lost!")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Ans:{}".format(word))
    time.sleep(2)


def win(tries):
    """
    This functio will print a message in case the user wins the game. Also the
    number of the remaining tries will be printed so the user will know how many
    times he/she guessed worng.

    param: tries => int -> the number of remaining tries
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("You WON!")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("{} tries left".format(tries))
    time.sleep(2)


def main():
    global lcd
    lcd = init_lcd()
    init_irw()
    index = 0
    lcd.clear()
    game_start_hangman(index, lcd)


if __name__ == "__main__":
    main()
