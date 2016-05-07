from __future__ import print_function
import RPi.GPIO as GPIO
import time
import string
import Queue
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np

# rsync scratch.py pi@raspberrypi:/home/pi/display16x32/python/scratch.py

delay = 0.00001

GPIO.setmode(GPIO.BCM)
red1_pin = 17
green1_pin = 18
blue1_pin = 22
red2_pin = 23
green2_pin = 24
blue2_pin = 25
clock_pin = 3
a_pin = 7
b_pin = 8
c_pin = 9
latch_pin = 4
oe_pin = 2

GPIO.setup(red1_pin, GPIO.OUT)
GPIO.setup(green1_pin, GPIO.OUT)
GPIO.setup(blue1_pin, GPIO.OUT)
GPIO.setup(red2_pin, GPIO.OUT)
GPIO.setup(green2_pin, GPIO.OUT)
GPIO.setup(blue2_pin, GPIO.OUT)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(a_pin, GPIO.OUT)
GPIO.setup(b_pin, GPIO.OUT)
GPIO.setup(c_pin, GPIO.OUT)
GPIO.setup(latch_pin, GPIO.OUT)
GPIO.setup(oe_pin, GPIO.OUT)

GPIO.setwarnings(False)

screen = np.zeros([16, 32], int)

def clock():
    GPIO.output(clock_pin, 1)
    GPIO.output(clock_pin, 0)

def latch():
    GPIO.output(latch_pin, 1)
    GPIO.output(latch_pin, 0)

def bits_from_int(x):
    if type(x) is np.int32:
        x = x.item()

    a_bit = x & 1
    b_bit = x & 2
    c_bit = x & 4
    return (a_bit, b_bit, c_bit)

def set_row(row):
    a_bit, b_bit, c_bit = bits_from_int(row)
    GPIO.output(a_pin, a_bit)
    GPIO.output(b_pin, b_bit)
    GPIO.output(c_pin, c_bit)

def set_color_top(color):
    red, green, blue = bits_from_int(color)
    GPIO.output(red1_pin, red)
    GPIO.output(green1_pin, green)
    GPIO.output(blue1_pin, blue)

def set_color_bottom(color):
    red, green, blue = bits_from_int(color)
    GPIO.output(red2_pin, red)
    GPIO.output(green2_pin, green)
    GPIO.output(blue2_pin, blue)

def refresh():
    for row in range(8):
        GPIO.output(oe_pin, 1)
        set_color_top(0)
        set_color_bottom(0)
        set_row(row)

        for col in range(32):
            set_color_top(screen[row][col])
            set_color_bottom(screen[row+8][col])
            clock()

        latch()
        GPIO.output(oe_pin, 0)
        time.sleep(delay)


def set_pixel(x, y, color):
    screen[y][x] = color


def clear():
    for x in range(32):
        for y in range(16):
            set_pixel(x, y, 0)


def char_to_pixels(text, path='arialbd.ttf', fontsize=14):
    """
    Based on http://stackoverflow.com/a/27753869/190597 (jsheperd)
    """
    font = ImageFont.truetype(path, fontsize)
    w, h = font.getsize(text)
    h *= 2
    image = Image.new('L', (w, h), 1)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    arr = arr[(arr != 0).any(axis=1)]
    return arr

_buffer = Queue.Queue()

for c in 'HELLO JELLYBEAN!':
    arr = char_to_pixels(
        c,
        path='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf',
        fontsize=9)

    _buffer.put(arr)


def roll_screen():
    global screen
    screen = np.roll(screen, -1)
    screen[:, 31] = 0

while not _buffer.empty():
    c = _buffer.get()

    # roll array and add whitespace
    roll_screen()
    refresh()

    # iterate columns in character
    for col in c.T:
        roll_screen()
        for y, val in enumerate(col):
            screen[y+4][31] = val

        refresh()

# finish the current scrolling text
while np.count_nonzero(screen):
    roll_screen()
    refresh()


clear()
refresh()