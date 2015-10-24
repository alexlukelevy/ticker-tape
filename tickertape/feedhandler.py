import feedparser


class FeedEvent:

    def __init__(self, content):
        self.content = content


class BbcNewsFeedHandler:

    def __init__(self, rss_url):
        self.rss_url = rss_url

    def events(self):
        rss = feedparser.parse(self.rss_url)
        return self.create_events(rss.entries)

    def create_events(self, rss_entries):
        return [FeedEvent(r.title) for r in rss_entries if self.is_valid_entry(r)]

    def is_valid_entry(self, entry):
        return not entry.title.startswith('VIDEO: ')