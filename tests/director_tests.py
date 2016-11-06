from mock import Mock
import time

from tickertape.director import Director


def test_action():
    # Given
    reporter = Mock()
    feed_handler = Mock()
    runtime = 1
    refresh = 0.5

    director = Director(reporter, [feed_handler], runtime, refresh)

    # When
    director.action()

    # Then
    time.sleep(1)

    feed_handler.handle.assert_called()
    reporter.report.assert_called()


def test_cut():
    # Given
    reporter = Mock()
    feed_handler = Mock()
    runtime = 10
    refresh = 0.5

    director = Director(reporter, [feed_handler], runtime, refresh)
    director.action()

    # When
    director.cut()

    # Then
    feed_handler.handle.reset_mock()
    reporter.report.reset_mock()

    time.sleep(1)

    feed_handler.handle.assert_not_called()
    reporter.report.assert_not_called()

