#!/usr/bin/python3
# -*- coding:utf-8 -*-

# lib pour le lecteur nfc
import subprocess
import nxppy
# lib pour les gpio du rasp
import RPi.GPIO as GPIO
# pour le sleep
import time
# pour le traitement du JSON
import json
# pour la communication avec volumio
from socketIO_client import SocketIO, LoggingNamespace
# passage en UTF-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# connection vers volumio
socketIO = SocketIO('localhost', 3000)
# init du nfc
mifare = nxppy.Mifare()
# com avec les GPIO en mode num des broches
GPIO.setmode(GPIO.BCM)

# variables
# bouton pour l'enregistrement
rec_button = 21
# bouton pour la lecture
play_button = 16
# led pendant l'enregistrement
rec_led = 26
# pour le courant
courant = 20
# onOff
on_off_button = 19
# volumePlus
plus_vol_button = 13
# volumeMoins
minus_vol_buuton = 6


# init de l'id du tag NFC
uid = ''

# inti des broche GPIO
# onOff
GPIO.setup(on_off_button, GPIO.IN)
# rec
GPIO.setup(rec_button, GPIO.IN)
# play
GPIO.setup(play_button, GPIO.IN)
# courant
GPIO.setup(courant, GPIO.OUT, initial=GPIO.HIGH)
# led
GPIO.setup(rec_led, GPIO.OUT, initial=GPIO.LOW)
# volume
GPIO.setup(plus_vol_button, GPIO.IN)
GPIO.setup(minus_vol_buuton, GPIO.IN)

# callback pour la creation de la playlist

def on_getQueue_response(*args):
    GPIO.output(rec_led, GPIO.HIGH)  # allumage de la led
    # suppression de la playlist
    socketIO.emit('deletePlaylist', {'name': uid})
    time.sleep(0.5)
    # iteration sur le contenu de la liste de lecture
    for row in args[0]:
        # recuperation de l'emplacement de la piste
        uri = row['uri'].decode().encode('utf-8')
        print(uri)
        # ajout a la playlist
        socketIO.emit('addToPlaylist', {
                      'name': uid, 'service': row['service'], 'uri': uri})
        socketIO.wait_for_callbacks(seconds=1)
        # pause avant de passer a la suivante
        time.sleep(0.7)
    # a la fin de la boucle on eteint la led
    GPIO.output(rec_led, GPIO.LOW)

# fonction de lecture
# uid : identifiant de la playlist


def play(buttonPlay):
    print('play')
    # effacer la liste de lecture
    # ajout de la playlist a la liste de lecture
    socketIO.emit('playPlaylist', {'name': uid})


def rec(buttonRec):
    print('rec')
    socketIO.emit('createPlayist', {'name': uid})
    socketIO.on('pushQueue', on_getQueue_response)
    socketIO.emit('getQueue', '', on_getQueue_response)
    socketIO.wait_for_callbacks(seconds=1)


def on_off(buttonOnOff):
    print('off')
    subprocess.call(['shutdown', '-h', 'now'], shell=False)


def volumeControl(button):
    print(button)


GPIO.add_event_detect(on_off, GPIO.RISING, callback=on_off, bouncetime=200)
GPIO.add_event_detect(rec, GPIO.RISING, callback=rec, bouncetime=600)
GPIO.add_event_detect(play, GPIO.RISING, callback=play, bouncetime=200)
GPIO.add_event_detect(minus_vol_buuton, GPIO.RISING,
                      callback=volumeControl, bouncetime=200)
GPIO.add_event_detect(plus_vol_button, GPIO.RISING,
                      callback=volumeControl, bouncetime=200)


# Print card UIDs as they are detected
while True:
    try:
        time.sleep(1)
        uid = mifare.select()
        print(uid)
    except nxppy.SelectError:
        pass
    except KeyboardInterrupt:
        GPIO.cleanup()
        pass
