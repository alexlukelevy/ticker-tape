from mock import Mock, patch
from tickertape.feedhandler import FeedEvent

from tickertape.reporter import Reporter


@patch('time.sleep')
@patch('__builtin__.print')
def test_report(_print, sleep):
    # Given
    director = Mock()
    tape = Mock()
    reporter = Reporter(director, tape)

    # iterate once
    director.rolling = Mock(side_effect=[True, False])
    reporter.receive(FeedEvent('Item 1'))

    # When
    reporter.report()

    # Then
    tape.display('Item 1')
    _print.assert_called_with('1 new events received')
    sleep.assert_called_with(60*5)


@patch('__builtin__.print')
def test_receive_event(_print):
    # Given
    director = Mock()
    tape = Mock()
    reporter = Reporter(director, tape)
    event = FeedEvent('Item 1')

    # When
    reporter.receive(event)

    # Then
    # TODO: better assertion?
    assert reporter._events[0] == event
    _print.assert_called_with('Reporter receiving event: Item 1')


@patch('__builtin__.print')
def test_print_status_non_empty(_print):
    # Given
    director = Mock()
    tape = Mock()
    reporter = Reporter(director, tape)

    event = FeedEvent('Item 1')
    reporter.receive(event)

    # When
    reporter.print_status()

    # Then
    _print.assert_called_with('1 new events received')


@patch('__builtin__.print')
def test_print_status_empty(_print):
    # Given
    director = Mock()
    tape = Mock()
    reporter = Reporter(director, tape)

    # When
    reporter.print_status()

    # Then
    _print.assert_called_with('No new events received')
