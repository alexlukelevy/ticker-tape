from threading import Thread

from feedhandler import *
from reporter import Reporter
from tape import *


class Director:
    """
    Coordinates the FeedHandlers and the Reporter
    """

    def __init__(self):
        self.__reporter = Reporter(Tape())
        #self.__reporter = Reporter(FakeTape())
        self.__feed_handlers = [
            BbcNewsFeedHandler(self.__reporter, 'http://feeds.bbci.co.uk/news/rss.xml')
        ]

    def action(self):
        self.start_reporter_thread()
        self.start_handler_threads()

    def start_reporter_thread(self):
        t = Thread(target=self.__reporter.report)
        t.start()

    def start_handler_threads(self):
        for fh in self.__feed_handlers:
            t = Thread(target=fh.listen)
            t.start()


if __name__ == '__main__':
    director = Director()
    director.action()
