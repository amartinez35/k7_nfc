import serial
import time
import nxppy
from Volumio import Volumio

ser = serial.Serial('/dev/ttyACM0', 9600)
vol = Volumio()
mifare = nxppy.Mifare()

def nfc_read_card():
  try:
    time.sleep(1)
    uid = mifare.select()
    return uid
  except nxppy.SelectError:
        # SelectError is raised if no card is in the field.
    pass

while True:
  if ser.inWaiting() > 0:
    commande = ser.readline().decode().strip()
    if commande == 'Rec':
      playlist = nfc_read_card()
      print(commande)
      print(playlist) 
       
