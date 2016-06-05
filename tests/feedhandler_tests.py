from mock import Mock, patch, call
from tickertape.feedhandler import *


@patch('__builtin__.print')
def test_handler_publish(_print):
    # Given
    reporter = Mock()
    handler = FeedHandler(reporter)
    event = FeedEvent('Item 1')

    # When
    handler.publish(event)

    # Then
    reporter.receive.assert_called_with(event)
    _print.assert_called_with('FeedHandler raising event: Item 1')


def test_bbc_news_handler():
    # Given
    reporter = Mock()
    handler = BbcNewsFeedHandler(reporter, 'tests\\bbc_rss.xml')

    # When
    handler.handle()

    # Then
    # VIDEO: entries stripped out and content populated with RSS title
    assert reporter.receive.call_count == 2
    call1 = call(FeedEvent('Flood threat from storm Patricia'))
    call2 = call(FeedEvent('Win-win on Britain\'s China gamble?'))
    reporter.receive.assert_has_calls([call1, call2], any_order=False)

