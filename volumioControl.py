import serial
import time
import nxppy
from Volumio import Volumio

ser = serial.Serial('/dev/ttyACM0', 9600)
vol = Volumio()
mifare = nxppy.Mifare()

while True:
  commande = ser.readline().decode().strip()
  if commande == 'Play':
      vol.play_song()
  print(commande) 
  try:
    uid = mifare.select()
    print(uid)
  except nxppy.SelectError:
        # SelectError is raised if no card is in the field.
    pass

  time.sleep(1)