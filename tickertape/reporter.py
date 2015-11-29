class Reporter:
    """
    Receives FeedEvents from FeedHandlers and decides upon
    the order in which to publish FeedEvents.
    """

    def __init__(self):
        self.events = []
        self.feed_handlers = []

    def register(self, feed_handler):
        self.feed_handlers.append(feed_handler)

    def refresh(self):
        self.events = []
        for fh in self.feed_handlers:
            self.events.extend(fh.report())

    def publish(self):
        # TODO
        for e in self.events:
            print(e.content)
