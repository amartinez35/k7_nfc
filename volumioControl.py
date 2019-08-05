#!/usr/bin/python3
# -*- coding:utf-8 -*-
import serial
from Volumio import Volumio
ser = serial.Serial('/dev/ttyACM0', 9600)
vol = Volumio()

while True:
  commande = ser.readline().decode().strip()
  if commande == 'Play':
      vol.play_song()
  print(commande) 