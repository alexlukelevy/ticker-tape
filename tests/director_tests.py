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
    reporter_call = call(refresh, reporter.report)
    feed_handler_call = call(refresh, feed_handler.handle)
    timer.assert_has_calls([reporter_call, feed_handler_call], any_order=False)

    reporter_timer.start.assert_called()
    feed_handler_timer.start.assert_called()
