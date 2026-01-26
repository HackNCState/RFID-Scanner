from machine import Pin,PWM
from mfrc522 import MFRC522
import time
from utime import sleep


# -------- Format UUID (bytes → string) --------
def format_uuid(b):
    return (
        f"{b[0]:02x}{b[1]:02x}{b[2]:02x}{b[3]:02x}-"
        f"{b[4]:02x}{b[5]:02x}-"
        f"{b[6]:02x}{b[7]:02x}-"
        f"{b[8]:02x}{b[9]:02x}-"
        f"{b[10]:02x}{b[11]:02x}{b[12]:02x}{b[13]:02x}{b[14]:02x}{b[15]:02x}"
    )
    

            
DEFAULT_KEY = [255, 255, 255, 255, 255, 255]

print("Place card on reader...")

reader = MFRC522(spi_id=0, sck=2, mosi=3, miso=4, cs=1, rst=0)
DEFAULT_KEY = [255, 255, 255, 255, 255, 255]

buzz = Pin(21, Pin.OUT)

past_uid = None  # store the last scanned card UID


while True:
    reader.init()
    (stat, _) = reader.request(reader.REQIDL)
    if stat != reader.OK:
        sleep(0.1)
        continue

    (stat, uid) = reader.SelectTagSN()
    if stat != reader.OK:
        continue

    uid_val = int.from_bytes(bytes(uid), "little", False)

    # Only process if this is a new card
    if uid_val != past_uid:
        past_uid = uid_val  # store this UID as the “past” one

        # Beep once
        buzz.value(1)
        sleep(0.05)
        buzz.value(0)


        # Read UUID from sector 1 block 0
        (stat, data) = reader.readSectorBlock(uid, sector=1, block=0, keyB=DEFAULT_KEY)
        if stat == reader.OK:
            uuid_bytes = bytes(data)
            print(format_uuid(uuid_bytes))
        else:
            print("UUID read failed")
            buzz.value(1)
            sleep(1)
            buzz.value(0)

    sleep(0.2)  
