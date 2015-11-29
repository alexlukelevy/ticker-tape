from tickertape.reporter import Reporter
from tickertape.feedhandler import *

from unittest.mock import MagicMock


def test_bbc_news_init():
    # Given
    r = Reporter()
    r.register = MagicMock()

    # When
    fh = BbcNewsFeedHandler(r, '')

    # Then
    r.register.assert_called_with(fh)


def test_bbc_news_report():
    # Given
    r = Reporter()
    fh = BbcNewsFeedHandler(r, 'tests\\bbc_rss.xml')

    # When
    events = fh.report()

    # Then
    # VIDEO: entries stripped out and content populated with RSS title
    assert len(events) == 2
    assert events[0].content == 'Flood threat from storm Patricia'
    assert events[1].content == 'Win-win on Britain\'s China gamble?'

