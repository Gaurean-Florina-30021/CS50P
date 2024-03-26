from basic_functions import str_to_int
import csv
from random import randint
import sys

MIN_LEVEL = 1
MAX_LEVEL = 7
LEVELS = ["1.csv", "2.csv", "3.csv", "4.csv", "5.csv", "6.csv", "7.csv"]


def replace_letter(word, guessed, g_letter):
    """
    This function is used to replace blank spaces in the word with the correct letters

    param: word => str -> the word without any blank spaces
    param: guessed => str -> the word containing blank spaces
    param: g_letter => char -> the letter guessed by the usser

    return: guessed => str -> the word containing the guessed word
    """
    index = 0
    for letter in word:
        if letter == g_letter:
            guessed[index] = g_letter
            index += 1
        else:
            index += 1
    return guessed


def wd_to_guess(lv):
    """
    This function is used to get frin the file the word that needs to be guessed

    param: lv => int -> the level that the player choosed to play

    return: to_guess => str -> the word to guess
    return: last_index => int -> the last index from the wordlist in the file
    """
    file_name = str(lv) + ".csv"
    before = verify_file(file_name, "r")
    if before == -1:
        return None, 0
    # store needed data from the file
    students = []
    students = read_data(before)
    last_index = len(students)
    before.close()
    word = randint(0, last_index - 1)
    to_guess = (students[word])["word"]
    return to_guess, last_index


def remove(level):
    """
    This function is used to read all words from the file and the word the user wants to delete
    and remove it from the file rewriting the hole file without the specified file.

    param: level => int -> the level from where the file shall be removed
    """
    name = str(level) + ".csv"
    file = verify_file(name, "r")
    if file == -1:
        print("Not enough words")
        return
    words = read_data(file)
    if len(words) <= 10:
        print("Not enough words")
        return
    new_dict = []
    word_list = [d["word"] for d in words]
    for wd in word_list:
        print(wd)
    rm_word = input("What word you want to earase? ")
    if not (rm_word in word_list):
        print("Word not in the list")
        return
    first = 0
    for d in words:
        # print(d, d['word'])
        if d["word"] != rm_word:
            new_dict.append({"index": d["index"], "word": d["word"]})
    with open(name, "w") as file1:
        writer = csv.DictWriter(file1, fieldnames=["index", "word"])
        writer.writeheader()
        for d in new_dict:
            writer.writerow({"index": d["index"], "word": d["word"]})


def verify_letter(letter, word):
    """
    This function will verify if a specified letter is in the word.

    param: letter => char -> the letter specified by the user
    param: word => str -> the word that needs to be guessed by the user
    """
    if len(letter) > 1 or len(letter) < 1:
        raise ValueError("Not a letter!")
    if letter in word:
        return True
    return False


def get_level():
    """
    This function is only used if the user plays on the software(WITHOUT ANY HARDWARE) and
    it gets the level the player wants to start.
    If the level is not an apropriate one the game will end and the programm will raise an error

    retur: lv => int -> the choosed level
    """
    lv = input("What level do you want to play[1-7]? ")
    lv = str_to_int(lv)
    if lv > 7 or lv < 1:
        raise ValueError("Not a valid number")
    return lv


def read_data(file):
    """
    This function is used to read all the words from a specified file.

    param: file => str -> the name of the file from where to read
    return: words => str[] -> an array with all words from the file
    """
    words = []
    reader = csv.DictReader(file)
    # print(reader)
    for row in reader:
        words.append({"index": int(row["index"]), "word": row["word"]})
    # print(words)
    return words


def verify_file(name, how):
    """
    This file will verify if the mentioned file can be opened or not. If the file
    cannot be opened the function will return -1

    param: name => str -> the name of the file
    param: how => str -> the way to open the file
    return: file => str -> the name of the file.
    """
    try:
        file = open(name, how)
    except:
        return -1
        # raise FileNotFoundError("Could not read the mentioned file")
        # sys.exit("Could not read ", name)
    return file


def get_wd():
    """
    This function is only used if the user plays on the software(WITHOUT ANY HARDWARE) and
    it gets the word that user wants to add in the dictionary.
    """
    word = input("What word you want to add? ").lower()
    # print(f"Are you sure you want to add {word} in dictionary?")
    response = input(
        'Are you sure you want to add "{}" in dictionary[Yes/No]?'.format(word)
    ).capitalize()
    save_word(word, response)


def save_word(word, response):
    """
    This function will try to save the word in the dictionary. If the word has less or more letters
    than it should have the returned value will be -3. If the word is already in list than the
    repsonse of the function will be -1.
    The function has a safety memory measure and it do not allow adding more than 100 words to the
    dictionary so if the user tries to add more the function will return -2.

    param: word => str -> the word the user wants to add
    param: response => str -> if the user is sure about adding the word or not
    return: int -> 0 in case of succes and negative numbers if not.
    """
    if response == "Yes":
        lv = len(word)
        if lv > 10 or lv < 3:
            return -3
            # raise ValueError("Word to long!")
        lv -= 2
        file_name = str(lv) + ".csv"
        # print(file_name)
        last_index, words = get_index(file_name)
        last_index = int(last_index)
        word_list = [d["word"] for d in words]
        if word in word_list:
            print("Already in list!")
            return -1
        if last_index == 100:
            print("Can't add! To many words in the file")
            return -2
        # store needed data from the file
        with open(file_name, "a") as file:
            writer = csv.DictWriter(file, fieldnames=["index", "word"])
            writer.writerow({"index": last_index + 1, "word": word})
        return 0


def get_index(file_name):
    """
    This function get the  last index present into the file.

    param: file_name => str -> the name of the file
    return: last_index => int -> the index of the last element from the dictionary
    return: words => str[] -> the words inside the dictionary
    """
    words = []
    # get index
    last_index = 0
    try:
        file = open(file_name, "r")
        words = read_data(file)
        # print(words)
        last_index = len(words)
        file.close()
    except:
        with open(file_name, "a") as file:
            writer = csv.DictWriter(file, fieldnames=["index", "word"])
            writer.writeheader()
    return last_index, words



def not_play_yet():
  while True:
        print("Enter a key to continue:\n1.Play\n2.Add\n3.Delete\n4.Back")
        what1 = input()
        what1 = str_to_int(what1)
        if what1 == 2:
            get_wd()
        elif what1 == 3:
            lv = input("From What level? ")
            lv = str_to_int(lv)
            remove(lv)
        else:
            return what1

def play_hangmane_sw():
    what1 = not_play_yet()
    if what1 == 1:
        # read the needed file
        lv = get_level()
        lv = verify_level(lv, MIN_LEVEL, MAX_LEVEL)
        while lv == False:
            lv = input("Level range [{}, {}]:".format(MIN_NUMBER, MAX_LEVEL))
            lv = verify_level(lv, MIN_NUMBER, MAX_LEVEL)
        to_guess, last_index = wd_to_guess(lv)
        if not can_play(to_guess):
            return
        guessed = []
        for letter in to_guess:
            guessed.append("_")
        print("Guess the word")
        tries = 5
        while tries != 0:
            for letter in guessed:
                # print(letter, end="")
                sys.stdout.write(letter)
            g_letter = input("What is your letter? ")

            # print(guessed)
            if not verify_letter(g_letter, to_guess):
                tries -= 1
            else:
                guessed = replace_letter(to_guess, guessed, g_letter)
            if not ("_" in guessed):
                break
        end_game(tries, to_guess)

def can_play(word):
    if word == None:
        print("File not found! Please add words!")
    else:
        return True

def end_game(tries, word):
    if tries == 0:
        print("You lost! The word was: {}".format(word))
    else:
        print("You Won!")
    print("Thanks for playing! Have a nice day!")


def main():
    if len(sys.argv) >= 2:
        print("Yey")
    play_hangmane_sw()


if __name__ == "__main__":
    main()
