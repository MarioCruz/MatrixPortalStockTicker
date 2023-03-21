#MatrixPortal Stock Ticker
#by Mario the Maker
#https://github.com/MarioCruz/MatrixPortalStockTicker/
#Marxh 21, 2023
import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal
from adafruit_display_text import label
import supervisor

#Prepare Stock Api
#Change the Stock1 to be the Stock Symbol you want
STOCK1 = "WSO"
# Set up where we'll be fetching data from
# Go here https://finnhub.io/ get a free ApiKey
DATA_SOURCE = (
    "https://finnhub.io/api/v1/quote?symbol=" + STOCK1 + "&token=ddddd"
)
#Parse the Json data
DATA1_LOCATION = ["c"]  #  Current price
DATA2_LOCATION = ["h"]  #  High price of the day
DATA3_LOCATION = ["l"]  #  Low price of the day
DATA4_LOCATION = ["pc"]  #  Prevoius Close
DATA5_LOCATION = ["d"]  #  Prevoius Close


# the current working directory (where this file is)
cwd = ("/" + __file__).rsplit("/", 1)[0]

FONT = "/fonts/IBMPlexMono-Medium-24_jep.bdf"
FONT2 = "/fonts/helvB12.bdf"
FONT3 = "/fonts/helvR10.bdf"
FONT4 = "/fonts/6x10.bdf"


#Get the JSON data
matrixportal = MatrixPortal(
    url=DATA_SOURCE, json_path=(DATA1_LOCATION, DATA2_LOCATION, DATA3_LOCATION, DATA4_LOCATION,DATA5_LOCATION), status_neopixel=board.NEOPIXEL,debug=True
)


#Add info to the JSON Data
def text_Current(val):
    return STOCK1+"  $%g" % val

def text_High(val):
    return "$%g High" % val

def text_Low(val):
    return "$%g Low" % val

def text_Prevoius(val):
    return "$%g Prevoius" % val

def text_Change(val):
    return "%"+"%g Change" % val


#Price
matrixportal.add_text(
    text_transform=text_Current,
    text_font=FONT,
    text_position=(6, 12),
    text_color=(0xC0C0C0),
    text_scale=1.4,
    scrolling=True,
)

#High
matrixportal.add_text(
    text_transform=text_High,
    text_font=FONT2,
    #text_font=terminalio.FONT,
    text_position=(1, 14),
    text_color=(0x0000AA),
    scrolling=True,
)

#Low
matrixportal.add_text(
    text_transform=text_Low,
    text_font=FONT2,
    #text_font=terminalio.FONT,
    text_position=(1, 23),
    text_color=(0x00FFFF),
    scrolling=True,
)

#Prevoius
matrixportal.add_text(
    text_transform=text_Prevoius,
    text_font=FONT3,
    text_position=(1, 16),
    text_color=(0xFF6600),
    text_scale=1.4,
    scrolling=True,
)

#Change
matrixportal.add_text(
    text_transform=text_Change,
    text_font=FONT4,
    text_position=(1, 15),
    text_color=(0x8533FF),
    text_scale=1.4,
    scrolling=True,
)

last_check = None

while True:
    if last_check is None or time.monotonic() > last_check + 280:  # How long to wait to get new data in seconds
        try:
            value = matrixportal.fetch()
            print("Response is", value)
            print(time.monotonic())
            last_check = time.monotonic()
        except (ValueError, RuntimeError) as e:
            print("Some error occurred, retrying! -", e)
            supervisor.reload()
    matrixportal.scroll()
    time.sleep(.0205)  # How Fast to Scroll

    
