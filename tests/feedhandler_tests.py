from tickertape.feedhandler import *


def setup():
    print "SETUP!"


def teardown():
    print "TEAR DOWN!"


def test_bbc_news_events():
    # Given
    fh = BbcNewsFeedHandler('tests\\bbc_rss.xml')

    # When
    events = fh.events()

    # Then
    # VIDEO: entries stripped out and content populated with RSS title
    assert len(events) == 2
    assert events[0].content == 'Flood threat from storm Patricia'
    assert events[1].content == 'Win-win on Britain\'s China gamble?'

