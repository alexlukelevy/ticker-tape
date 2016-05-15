from __future__ import print_function
import feedparser
import time


class FeedEvent:

    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.content == other.content

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.content


class FeedHandler(object):

    def __init__(self, director, reporter):
        self._director = director
        self._reporter = reporter

    def publish(self, event):
        self.print_publish(event)
        self._reporter.receive(event)

    def print_publish(self, event):
        handler = self.__class__.__name__
        print('{0} raising event: {1}'.format(handler, event))


class BbcNewsFeedHandler(FeedHandler):

    def __init__(self, director, reporter, rss_url):
        super(BbcNewsFeedHandler, self).__init__(director, reporter)
        self._rss_url = rss_url
        self._event_log = []

    def listen(self):
        # indefinitely look for new headlines
        while self._director.rolling():
            rss = feedparser.parse(self._rss_url)
            events = self.create_events(rss.entries[:10])

            for e in events:
                if e not in self._event_log:
                    self.publish(e)

            time.sleep(600)

    def publish(self, event):
        super(BbcNewsFeedHandler, self).publish(event)
        self._event_log.append(event)

    def create_events(self, rss_entries):
        return [FeedEvent(r.title) for r in rss_entries if self.is_valid_entry(r)]

    @staticmethod
    def is_valid_entry(entry):
        return not entry.title.startswith('VIDEO: ')
