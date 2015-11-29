import time

from tickertape.feedhandler import *

from tickertape.reporter import Reporter


class Director:
    """
    Coordinates the FeedHandlers and the Reporter
    """

    def __init__(self):
        self.reporter = Reporter()
        self.feed_handlers = [
            BbcNewsFeedHandler(self.reporter, 'http://feeds.bbci.co.uk/news/rss.xml')
        ]

    def action(self):
        while True:
            self.reporter.refresh()
            self.reporter.publish()
            time.sleep(10)


if __name__ == '__main__':
    director = Director()
    director.action()
