from machine import Pin,PWM
from mfrc522 import MFRC522
import time
from utime import sleep

reader = MFRC522(spi_id=0, sck=2, mosi=3, miso=4, cs=1, rst=0)

print("Place your card near the reader...")
buzz = machine.Pin(16, machine.Pin.OUT)
past_uid=0

while True:
    (status, tag_type) = reader.request(reader.REQIDL)
    if status == reader.OK:
        (status, uid) = reader.SelectTagSN()
        uid_val = int.from_bytes(bytes(uid), "little", False) #ints are easier to input
        if uid_val!=past_uid:
                buzz.value(1)
                sleep(.3)
                buzz.value(0)
                print("Card detected! UID:", uid_val)
                past_uid=uid_val
            
            
            
