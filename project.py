from remote_control import init_irw, next_key
from lcd_setup import init_lcd
import time
import RPi.GPIO as GPIO
from gpiozero import MCP3008
from temperature_sensor import read_temp
from guess_hw import game_start_guess
from calculator_hw import game_start_calculator
from hangman_hw import game_start_hangman
from common_hw_functions import print_navigations
from basic_functions import str_to_int
from hangman import play_hangmane_sw
from guess import play_guess_sw
from calculator import play_calculator_sw
import sys

b = 16
exit_button = 18
pomp = 8
delay = 2
games = ["Guess ME", "Smart Calculator", "Hangman"]
lcd = init_lcd()


def setup_hardware():
    """
    This funtion will set up the butons and the pomp as output/input.
    Also this function will enable the remote control of the project.
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(exit_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(pomp, GPIO.OUT)
    init_irw()


def read_data():
    """
    This function will read the humidity sensor value and connvert it in percentage.
    Also the function will read the tempeature.
    Those values will be printed on the LCD.

    return: temp => float -> temperature in Celsius degree
            h => float -> humidity in percentage
    """
    global lcd
    humidity = MCP3008(channel=0)
    h = 100 - (humidity.value * 100)
    temp = read_temp()
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Humidity: {}%".format(round(h, 1)))
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Temp: {}C".format(temp))
    return h, temp


def watter_plant():
    """
    This function will open the pomp afor a second and than stop it
    """
    GPIO.output(pomp, GPIO.HIGH)
    time.sleep(delay / delay)
    GPIO.output(pomp, GPIO.LOW)


def shut_down():
    """
    This function will display the Goodbye message at the end of the program
    also it will clean the lcd.
    """
    global lcd
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("See you soon!")
    time.sleep(delay)
    lcd.clear()


def start_games(lcd):
    """
    This function will start the selected game

    param: lcd -> the lcd used to print on the screen during te selection process
    return: -1 -> in case of error or in case that the player chose to go back
    """
    print_navigations(lcd)
    index = 0
    game = game_selection(index)
    if game == 0:
        game_start_guess(index, lcd)
    elif game == 1:
        game_start_calculator(index, lcd)
    elif game == 2:
        game_start_hangman(index, lcd)
    else:
        return -1


def game_selection(index):
    """
    This function will stop only when one game will be selected and will return the
    game index.
    """
    global lcd
    game_index = None
    while True:
        print_menu(index)
        key = next_key()
        game_index, index = browse_games(key, index)
        if index == None:
            return None
        if game_index != None:
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            if game_index < 0:
                lcd.write_string("Wrong button!")
                lcd.cursor_pos = (1, 0)
                lcd.write_string("GOODBYE!")
            elif game_index < 3 and game_index >= 0:
                lcd.write_string(games[index])
            else:
                print_end(lcd)
            break
    time.sleep(delay)
    return game_index


def browse_games(key, index):
    """
    This function will verify if the key is a key that helps to navigate in the
    available games or to select the games.
    If the input key will be one that helps during the game navigation it will return None
    on the first position and next/previous game index, from the list, according to pressed key.
    If the input key is a key with selection purpose than the both possition will be the index of
    the current game in the list.
    If another key is pressed than both return values will be None

    param: key -> The key pressed on the remote control
    param: index => int -> the index of the current game
    return: index => index. First index is used to indicate the index of selected
    game. The second index is the index of the next game in the list.

    """
    if key == "NEXT_BUTTON":
        if index == 3:
            index = 0
        else:
            index += 1
    elif key == "PREV_BUTTON":
        if index == 0:
            index = 3
        else:
            index -= 1
    elif key == "PLAY_BUTTON" or key == "EQUAL_BUTTON":
        return index, index
    else:
        return None, None
    return None, index


def print_end(lcd):
    """
    This function will print a message at the end of the game
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Thanks for")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("attention!")
    time.sleep(delay)


def print_menu(index):
    """
    This function will display on the lcd the instructionto navigate trough the games.
    The game that will be selected is always displayed on the LCD

    param: index => int -> the index of the current displayed game
    """
    global lcd
    print_navigations(lcd)
    lcd.cursor_pos = (1, 0)  # line 2
    if index == 3:
        txt = "{}. Back!".format(index + 1)
    else:
        txt = "{}. {}!".format(index + 1, games[index])
    lcd.write_string(txt)

def play_again_sw():
    print("Play again?\n1.Yes\n2.No\n")
    what1 = input()
    what1 = str_to_int(what1)
    if what1 == 1:
        return True
    return False


def software_play():
    for g in enumerate(games):
            print("{}. {}".format(g[0] + 1, g[1]))
    game = input("What game you want to play?")
    game = str_to_int(game)
    if 1<= game and game <= 3:
        while True:
            print("{}. {}".format(game, games[game - 1]))
            if game == 1:
                play_guess_sw()
            elif game == 2:
                play_calculator_sw()
            else:
                play_hangmane_sw()
            if play_again_sw() == 1:
                continue
            else:
                break

def hw_part():
    global lcd
    setup_hardware()
    while True:
        humidity, temp = read_data()
        if humidity < 10:
            watter_plant()
        time.sleep(delay)
        if GPIO.input(exit_button) == GPIO.HIGH:
            break
        if GPIO.input(b) == GPIO.HIGH:
            while True:
                if start_games(lcd) == -1:
                    break
    shut_down()

def main():
    if len(sys.argv) >= 2:
        software_play()
    else:
        hw_part()



if __name__ == "__main__":
    main()
