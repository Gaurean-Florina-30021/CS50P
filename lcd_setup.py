from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO


def init_lcd():
    GPIO.setwarnings(False)
    lcd_rs = 37
    # enable
    lcd_en = 35
    # data pins:
    D4 = 33
    D5 = 31
    D6 = 29
    D7 = 26
    # lcd setup
    # some lcd setups may include rows an cols parameters which are rows and coloumns
    lcd = CharLCD(
        pin_rs=lcd_rs,
        pin_e=lcd_en,
        pins_data=[D4, D5, D6, D7],
        numbering_mode=GPIO.BOARD,
    )
    # clear the display
    lcd.clear()
    return lcd


def main():
    lcd = init_lcd()
    lcd.clear()
    # set cursor position (if not set automatically starts from the first char on the LCD)
    lcd.cursor_pos = (0, 2)  # line 1 coloumn 3
    # Write text
    lcd.write_string("Hello world!")
    lcd.cursor_pos = (1, 5)  # line 2 coloumn 6
    lcd.write_string("CS50P!")


if __name__ == "__main__":
    main()
