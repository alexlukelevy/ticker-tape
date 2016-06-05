import threading


class Director:
    """
    Coordinates the FeedHandlers and the Reporter
    """

    def __init__(self, reporter, feed_handlers, refresh, timer=threading.Timer):
        self._reporter = reporter
        self._feed_handlers = feed_handlers
        self._refresh = refresh
        self._timer = timer

    def action(self):
        self._start_timer(self._reporter.report)

        for fh in self._feed_handlers:
            self._start_timer(fh.handle)

    def _start_timer(self, func):
        t = self._timer(self._refresh, func)
        t.start()
