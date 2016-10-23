import threading
import time


class Director:
    """
    Coordinates the FeedHandlers and the Reporter

    Feedhandlers are set up to be invoked every
    [refresh] seconds, whilst the Reporter is invoked
    continuously.
    """

    def __init__(self, reporter, feed_handlers, refresh):
        self._reporter = reporter
        self._feed_handlers = feed_handlers
        self._refresh = refresh
        self._airing = False
        self._threads = []

    def action(self):
        self._airing = True

        for fh in self._feed_handlers:
            fh_thread = threading.Thread(target=self._repeat, args=(fh.handle, self._refresh))
            self._threads.append(fh_thread)

        reporter_thread = threading.Thread(target=self._repeat, args=(self._reporter.report,))
        self._threads.append(reporter_thread)

        for thread in self._threads:
            thread.start()

    def cut(self):
        self._airing = False
        for thread in self._threads:
            thread.join()
        self._threads = []

    def _repeat(self, func, interval=0):
        while self._airing:
            func()
            time.sleep(interval)
