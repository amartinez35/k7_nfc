import serial
import time
import nxppy
from Volumio import Volumio

ser = serial.Serial('/dev/ttyACM0', 9600)
volumio = Volumio()
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
    print(commande)
    if commande == 'Rec':
      playlist = nfc_read_card()
      print(playlist)
      if playlist is not None:
        volumio.set_playlist(playlist)
        volumio.create_playlist()
        volumio.record_playlist()
    if commande == 'Play':
      playlist = nfc_read_card()
      print(playlist)
      if playlist is not None:
        volumio.set_playlist(playlist)
        volumio.play_playlist()
    if commande == 'Prev':
      volumio.previous_song()
    if commande == 'Next':
      volumio.next_song()
    if commande == 'Stop':
      volumio.stop_song()
       
