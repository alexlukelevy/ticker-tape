from mock import Mock, patch
from tickertape.feedhandler import FeedEvent

from tickertape.reporter import Reporter


@patch('__builtin__.print')
def test_report(_print):
    # Given
    tape = Mock()
    lock = Mock()
    reporter = Reporter(tape, lock)

    reporter.receive(FeedEvent('Item 1'))

    # When
    reporter.report()

    # Then
    lock.acquire.assert_called()
    tape.display.assert_called_with('Item 1')
    _print.assert_called_with('1 new events received')
    lock.release.assert_called()


@patch('__builtin__.print')
def test_receive_event(_print):
    # Given
    tape = Mock()
    lock = Mock()
    reporter = Reporter(tape, lock)
    event = FeedEvent('Item 1')

    # When
    reporter.receive(event)

    # Then
    # TODO: better assertion?
    lock.acquire.assert_called()
    assert reporter._events[0] == event
    _print.assert_called_with('Reporter receiving event: Item 1')
    lock.release.assert_called()


@patch('__builtin__.print')
def test_print_status_non_empty(_print):
    # Given
    tape = Mock()
    reporter = Reporter(tape)

    event = FeedEvent('Item 1')
    reporter.receive(event)

    # When
    reporter.print_status()

    # Then
    _print.assert_called_with('1 new events received')


@patch('__builtin__.print')
def test_print_status_empty(_print):
    # Given
    tape = Mock()
    reporter = Reporter(tape)

    # When
    reporter.print_status()

    # Then
    _print.assert_called_with('No new events received')
