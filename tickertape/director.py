from threading import Thread

from feedhandler import *
from reporter import Reporter
from tape import *


class Director:
    """
    Coordinates the FeedHandlers and the Reporter
    """

    def __init__(self):
        self._reporter = Reporter(self, Tape())
        self._feed_handlers = [
            BbcNewsFeedHandler(self._reporter, 'http://feeds.bbci.co.uk/news/rss.xml')
        ]

    def action(self):
        self.start_reporter_thread()
        self.start_handler_threads()

    def start_reporter_thread(self):
        t = Thread(target=self._reporter.report)
        t.start()

    def start_handler_threads(self):
        for fh in self._feed_handlers:
            t = Thread(target=fh.listen)
            t.start()

    def rolling(self):
        """
        Run indefinitely.
        """
        return True


if __name__ == '__main__':
    director = Director()
    director.action()
