import board
import time
from digitalio import DigitalInOut, Direction, Pull


# variables
#-- digital
# bouton pour l'enregistrement
rec_button = DigitalInOut(board.D1)
rec_button.direction = Direction.INPUT
rec_button.pull = Pull.UP
# bouton pour la lecture
play_button = DigitalInOut(board.D2)
play_button.direction = Direction.INPUT
play_button.pull = Pull.UP
# bouton pour stop
stop_button = DigitalInOut(board.D3)
stop_button.direction = Direction.INPUT
stop_button.pull = Pull.UP
# bouton suivant
next_button = DigitalInOut(board.D4)
next_button.direction = Direction.INPUT
next_button.pull = Pull.UP
# bouton precedent
prev_button = DigitalInOut(board.D5)
prev_button.direction = Direction.INPUT
prev_button.pull = Pull.UP
#led rec
rec_led = DigitalInOut(board.D10)
rec_led.direction = Direction.OUTPUT

def play():
    print('Play')

def rec():
    print('Rec')
    rec_led.value = True

def stop():
    print('Stop')

def next_song():
    print('Next')

def previous_song():
    print('Prev')

while True:
    if play_button.value:
        play()
    if rec_button.value:
        rec()
    if stop_button.value:
        stop()
    if next_button.value:
        next_song()
    if prev_button.value:
        previous_song()
    time.sleep(0.01)