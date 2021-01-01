# Metro Matrix Clock
# Metro Matrix Clock
# Metro Matrix Clock
# Runs on Airlift Metro M4 with 64x32 RGB Matrix display & shield
import _pixelbuf
import time
import board
import displayio
import terminalio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix
import vectorio
from new_year import NEW_YEAR

BIT_DEPTH = 6
BLINK = True
DEBUG = False
global year
year = 2020

from secrets import secrets
print("Time will be set for {}".format(secrets["timezone"]))

# --- Display setup ---
matrix = Matrix(bit_depth=BIT_DEPTH)
display = matrix.display
display.brightness = 0.8
network = Network(debug=DEBUG)
BITMAP = displayio.OnDiskBitmap(open('balldrop.bmp', 'rb'))

TILE_GRID = displayio.TileGrid(BITMAP,pixel_shader=displayio.ColorConverter(),)

class RowCountdown:
    def __init__(self, display, displayio):
        # --- Drawing setup ---
        self.group = displayio.Group(max_size=10)  # Create a Group
        self.bitmap = displayio.Bitmap(64, 32, 5)  # Create a bitmap object,width, height, bit depth
        self.color = displayio.Palette(256)  # Create a color palette
        for idx in range(1,255):
            self.color[idx] = _pixelbuf.colorwheel(idx)

        # Create a TileGrid using the Bitmap and Palette
        self.tile_grid = displayio.TileGrid(BITMAP,
                            pixel_shader=displayio.ColorConverter(),
                            width=1,
                            height=1,
                            tile_width=16,
                            tile_height=16)
        self.tile_grid.x = 64-16
        self.tile_grid.y = 1
        #pole = vectorio.Rectangle(width=1,height=14)
        #self.pole = vectorio.VectorShape(shape=pole, pixel_shader=self.color,x=64-16,y=1)
        #self.group.append(self.pole)
        self.group.append(self.tile_grid)  # Add the TileGrid to the Group
        display.show(self.group)

        #### NDAYS[1] "DAYS"[2]  12 pixel font
        #### NHOUR[3] "HOURS"[4]  8 pixel font
        #### NMIN[5] "MINUTES"[6] 8 pixel font
        #### NSEC[7] "SECONDS"[8] 8 pixel font
        if not DEBUG:
            self.font = bitmap_font.load_font("/fonts/IBMPlexMono-Medium-12.bdf")
            self.sfont = bitmap_font.load_font("/fonts/IBMPlexMono-Medium-8.bdf")
        else:
            self.font = terminalio.FONT

        self.create_clock()



    def create_clock(self):
        offset = 6 #
        self.group.append(Label(self.font,text="000",x=0,y=5))
        self.group.append(Label(self.font,text="DAYS",x=20,y=5,color=0x1010FF))
        for idx,val in enumerate(("HOURS","MIN","SEC"),start=1):
            self.group.append(Label(self.sfont,text="00",y=offset+7*idx,x=0))
            self.group.append(Label(self.sfont,text=val,y=offset+7*idx,x=12, color=0x30FF00))


    def timediff(self, t1=None):
        global year
        if t1 == None:
            t1 = time.mktime(time.struct_time((year,12,25,0,0,0,4,-1,-1)))
        secs = t1 - time.time()
        diff = t1 - time.time()
        days = int(diff//86400)
        #if days < 0:
        #    year += 1
        #    print("Adding a year!")
        #    return
        #elif days > 365:
        #    year -= 1
        #    print("Subtracting a year!")
        #    return
        diff = diff - days*86400
        hours = int(diff // 3600)
        diff = diff - hours*3600
        min = int(diff // 60)
        sec = int(diff - min*60)
        self.group[1].text = "%2d" % days
        self.group[3].text = "%2d" % hours
        self.group[5].text = "%2d" % min
        self.group[7].text = "%2d" % sec
        return secs
        #return "{:3d}Days\n{:02d}:{:02d}:{:02d}".format(days,hours,min,sec)


last_check = None
q = RowCountdown(display, displayio)
idx = 0

while True:
    one_second_start = time.monotonic()
    if last_check is None or time.monotonic() > last_check + 864000:
        try:
            network.get_local_time()
            last_check = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
    secs = q.timediff(t1=time.mktime(time.struct_time((2021,1,1,0,0,0,4,-1,-1))))
    #print("Days Left = ",dleft)
    if secs < 7200:
        print("HOW DID WE GET HERE")
        n = NEW_YEAR()
        display.show(n.group)
        while True:
            n.one_cycle()
    ball_pos = 16 - (secs // 5400 )
    if ball_pos < 0:
        ball_pos = 0
    elif ball_pos > 16:
        ball_pos = 16

    q.tile_grid.y = ball_pos
    while time.monotonic() < one_second_start + 1:
        for gidx in (1,3,5,7):
            q.group[gidx].color = q.color[idx]
        idx += 1
        idx %= 255
        if idx == 0:
            idx = 1
        q.tile_grid[0] = (idx//2)%14
        time.sleep(10/255)
    #time.sleep(1)