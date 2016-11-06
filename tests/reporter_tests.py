from mock import Mock, patch, call
from tickertape.feedhandler import FeedEvent

from tickertape.reporter import Reporter


@patch('__builtin__.print')
def test_report(_print):
    # Given
    tape = Mock()
    lock = Mock()
    reporter = Reporter(tape, lock)

    reporter.receive(FeedEvent('Item 1', 'bbc', 2))

    # When
    reporter.report()

    # Then
    lock.acquire.assert_called()
    tape.display.assert_called_with('Item 1')
    assert tape.display.call_count == 2
    _print.assert_called_with('Reporting for bbc')
    lock.release.assert_called()


@patch('__builtin__.print')
def test_receive_event(_print):
    # Given
    tape = Mock()
    lock = Mock()
    reporter = Reporter(tape, lock)
    event = FeedEvent('Item 1', 'bbc')

    # When
    reporter.receive(event)

    # Then
    lock.acquire.assert_called()
    _print.assert_called_with('Reporter receiving event: Item 1')
    lock.release.assert_called()


def test_receive_event_and_report():
    # Given
    tape = Mock()
    reporter = Reporter(tape)

    reporter.receive(FeedEvent('Item 1', 'bbc'))
    reporter.receive(FeedEvent('Item 2', 'bbc'))
    reporter.receive(FeedEvent('Item 3', 'bbc'))
    reporter.receive(FeedEvent('Item 4', 'bbc'))
    reporter.receive(FeedEvent('Item 5', 'bbc'))
    reporter.receive(FeedEvent('Item 6', 'bbc'))

    # When
    reporter.report()

    # Then
    assert tape.display.call_count == 5
    tape.display.assert_has_calls([
        call('Item 2'),
        call('Item 3'),
        call('Item 4'),
        call('Item 5'),
        call('Item 6')
    ])
