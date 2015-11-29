from unittest.mock import Mock
from feedhandler import FeedEvent

from tickertape.reporter import Reporter


def test_register():
    # Given
    r = Reporter()
    fh = Mock()

    # When
    r.register(fh)

    # Then
    assert r.feed_handlers[0] == fh


def test_refresh():
    # Given
    r = Reporter()
    fh = Mock()

    events = [FeedEvent('Item 1'), FeedEvent('Item 2')]
    fh.report = Mock(return_value=events)

    r.register(fh)

    # When
    r.refresh()

    # Then
    assert r.events == events
