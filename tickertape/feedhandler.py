import feedparser


class FeedEvent:

    def __init__(self, content):
        self.content = content


class BbcNewsFeedHandler:

    def __init__(self, reporter, rss_url):
        self.__reporter = reporter
        self.__rss_url = rss_url
        self.__reporter.register(self)

    def report(self):
        rss = feedparser.parse(self.__rss_url)
        return self.create_events(rss.entries)

    def create_events(self, rss_entries):
        return [FeedEvent(r.title) for r in rss_entries if self.is_valid_entry(r)]

    @staticmethod
    def is_valid_entry(entry):
        return not entry.title.startswith('VIDEO: ')