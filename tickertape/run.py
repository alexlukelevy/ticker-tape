from rgbmatrix import graphics
from rgbmatrix import RGBMatrix

from feedhandler import *
from reporter import Reporter
from director import Director
from tape import *


"""
Configure DI and start tickertape
"""
if __name__ == '__main__':

    matrix = RGBMatrix(16, 1, 1)
    color = graphics.Color(255, 255, 0)
    font = graphics.Font()
    font.LoadFont('../fonts/7x13.bdf')
    draw = graphics.DrawText
    tape = Tape(matrix, color, font, draw)

    reporter = Reporter(tape)

    feed_handlers = [
        BbcNewsFeedHandler(reporter, 'http://feeds.bbci.co.uk/news/rss.xml')
    ]

    director = Director(reporter, feed_handlers, 60*10)
    director.action()

    raw_input('Press ENTER to shutdown\n')
