from mock import Mock, call

from tickertape.director import Director


def test_action():
    # Given
    reporter = Mock()
    feed_handler = Mock()
    refresh = 30

    reporter_timer = Mock()
    feed_handler_timer = Mock()

    timer = Mock(side_effect=[reporter_timer, feed_handler_timer])

    director = Director(reporter, [feed_handler], refresh, timer)

    # When
    director.action()

    # Then
    # scheduled call
    reporter_call = call(refresh, director._start_timer, [reporter.report])
    feed_handler_call = call(refresh, director._start_timer, [feed_handler.handle])
    timer.assert_has_calls([feed_handler_call, reporter_call], any_order=False)
    # start schedule
    reporter_timer.start.assert_called()
    feed_handler_timer.start.assert_called()
    # initial synchronous call
    reporter.report.assert_called()
    feed_handler.handle.assert_called()
