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
        for fh in self._feed_handlers:
            self._start_timer(fh.handle)

        self._start_timer(self._reporter.report)

    def _start_timer(self, func):
        # reschedule every self._refresh seconds
        self._timer(self._refresh, self._start_timer, [func]).start()
        func()
