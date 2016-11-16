from __future__ import print_function
import threading
import time


class Director:
    """
    Coordinates the FeedHandlers and the Reporter

    Feedhandlers are set up to be invoked every
    [refresh] minutes, whilst the Reporter will
    run until [runtime] minutes have passed.
    """

    def __init__(self, reporter, feed_handlers, runtime, refresh):
        self._reporter = reporter
        self._feed_handlers = feed_handlers
        self._runtime = runtime
        self._refresh = refresh
        self._airing = False
        self._timer = None
        self._threads = []

    def action(self):
        print('TickerTape starting up')
        self._airing = True
        self._start_timer()
        self._start_reporter()
        self._start_feed_handlers()
        print('TickerTape started')

    def cut(self):
        print('TickerTape shutting down')
        self._airing = False
        self._timer.cancel()
        self._timer = None
        for thread in self._threads:
            thread.join()
        self._threads = []
        print('TickerTape stopped')

    def _start_timer(self):
        self._timer = threading.Timer(self._runtime, self.cut)
        self._timer.start()

    def _start_reporter(self):
        reporter_thread = threading.Thread(target=self._repeat, args=(self._reporter.report,))
        self._threads.append(reporter_thread)
        reporter_thread.start()

    def _start_feed_handlers(self):
        for fh in self._feed_handlers:
            fh_thread = threading.Thread(target=self._repeat, args=(fh.handle, self._refresh))
            self._threads.append(fh_thread)
            fh_thread.start()

    def _repeat(self, func, interval=0):
        while self._airing:
            func()
            time.sleep(interval)
