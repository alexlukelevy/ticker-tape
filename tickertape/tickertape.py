from __future__ import print_function
import argparse
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix

from feedhandler import *
from reporter import Reporter
from director import Director
from tape import Tape

"""
Configure DI and start tickertape
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TickerTape')
    parser.add_argument(
        '-m',
        '--runtime',
        dest='runtime',
        default=0,
        help='minutes to run (default: 0 - infinite)'
    )
    parser.add_argument(
        '-r',
        '--refresh',
        dest='refresh',
        default=5,
        help='minutes between FeedHandler refreshes (default: 5 )'
    )
    args = parser.parse_args()

    print('TickerTape configured to run for {} minutes, refreshing FeedHandlers'
          'every {} minutes', args.runtime, args.refresh)

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

    director = Director(reporter, feed_handlers, args.runtime * 60, args.refresh * 60)
    director.action()

    raw_input('Press ENTER to shutdown\n')
