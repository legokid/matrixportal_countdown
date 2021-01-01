import _pixelbuf
import time
import board
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_text.label import Label
from secrets import secrets
from random import randint, choice

class NEW_YEAR:
    #RBITMAP = displayio.Bitmap(64,32,256)

    #group.append(background)
    #group.append(txt)
    #display.show(group)
    #global scroll_count
    scroll_count = 0

    #global ye

    def __init__(self):
        self.SHADER = displayio.Palette(256)
        self.RBITMAP = displayio.Bitmap(64,32,256)
        self.background = displayio.TileGrid(self.RBITMAP,pixel_shader=self.SHADER,)
        self.group = displayio.Group()

        self.font = bitmap_font.load_font("/fonts/IBMPlexMono-Medium-24.bdf")

        text = "HAPPY 2021!!!      HAPPY NEW YEAR!!!"
        self.txt = Label(self.font, text=text)
        for idx in range(1,255):
            self.SHADER[idx] = _pixelbuf.colorwheel(idx)
        self.group.append(self.background)
        self.group.append(self.txt)
        (self.xs,self.ys,self.xe,self.ye) = self.txt.bounding_box

        self.txt.y = 16

    def scrolltext(self):
        #global scroll_count,xe
        self.txt.x -=2
        if self.txt.x < -self.xe:
            self.txt.x = 0
        self.txt.color=_pixelbuf.colorwheel(self.scroll_count)
        self.scroll_count = (self.scroll_count +1)% 255

    def randomize(self,num=96):
        for idx in range(num):
            self.RBITMAP[randint(0,63), randint(0,31)] = randint(0,255) * choice([0,1,1,1,1])

    def one_cycle(self):
        self.randomize()
        self.scrolltext()

#n = NEW_YEAR()
#display.show(n.group)
#while True:
#    n.one_cycle()
#    time.sleep(0.1)
    #time.sleep(0.01)