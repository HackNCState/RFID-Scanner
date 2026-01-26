from machine import Pin
from mfrc522 import MFRC522
import utime
import urandom

# ---------------- Buzzer ----------------
buzz = Pin(21, Pin.OUT)

def short_beep():
    buzz.value(1)
    utime.sleep_ms(50)
    buzz.value(0)
def longbeep():
    buzz.value(1)
    utime.sleep_ms(1000)
    buzz.value(0)
    utime.sleep_ms(100)
    buzz.value(1)
    utime.sleep_ms(1000)
    buzz.value(0)


# ---------------- UUID v4 ----------------
def uuid4_bytes():
    b = bytearray(16)
    for i in range(16):
        b[i] = urandom.getrandbits(8)

    # RFC 4122 compliance
    b[6] = (b[6] & 0x0F) | 0x40  # version 4
    b[8] = (b[8] & 0x3F) | 0x80  # variant
    return b

def format_uuid(b):
    return (
        f"{b[0]:02x}{b[1]:02x}{b[2]:02x}{b[3]:02x}-"
        f"{b[4]:02x}{b[5]:02x}-"
        f"{b[6]:02x}{b[7]:02x}-"
        f"{b[8]:02x}{b[9]:02x}-"
        f"{b[10]:02x}{b[11]:02x}{b[12]:02x}{b[13]:02x}{b[14]:02x}{b[15]:02x}"
    )

# ---------------- RFID setup ----------------
reader = MFRC522(
    spi_id=0,
    sck=2,
    miso=4,
    mosi=3,
    cs=1,
    rst=0
)

DEFAULT_KEY = [255, 255, 255, 255, 255, 255]
past_uid = None

print("Ready — scan cards")

while True:
    reader.init()
    (stat, _) = reader.request(reader.REQIDL)
    if stat != reader.OK:
        utime.sleep_ms(100)
        continue

    (stat, uid) = reader.SelectTagSN()
    if stat != reader.OK:
        continue

    uid_val = bytes(uid)

    # Only act if this is a new card
    if uid_val != past_uid:
        past_uid = uid_val

        short_beep()  # beep on new card


        # Generate UUID v4
        uuid_bytes = uuid4_bytes()
        print(format_uuid(uuid_bytes))

        # Write UUID to sector 1, block 0
        if reader.writeSectorBlock(uid, sector=1, block=0, data=list(uuid_bytes), keyB=DEFAULT_KEY) == reader.OK:
            (stat, data) = reader.readSectorBlock(uid, 1, 0, keyB=DEFAULT_KEY)
        else:
            print("Write failed")
            longbeep()

    utime.sleep_ms(200)