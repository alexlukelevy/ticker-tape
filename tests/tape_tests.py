from mock import Mock, call

from tickertape.tape import Tape


def test_display():
    # Given

    matrix = Mock()
    color = Mock()
    font = Mock()
    draw = Mock()
    sleep = Mock()

    canvas = Mock()
    canvas.width = 2
    matrix.CreateFrameCanvas.return_value = canvas
    matrix.SwapOnVSync.return_value = canvas
    draw.side_effect = [1, 0, 0]
    text = 'Hi'

    tape = Tape(matrix, color, font, draw, sleep)

    # When
    tape.display(text)

    # Then
    draw1 = call(canvas, font, 2, 10, color, text)
    draw2 = call(canvas, font, 2, 10, color, text)
    draw3 = call(canvas, font, 1, 10, color, text)
    draw.assert_has_calls([draw1, draw2, draw3], any_order=False)
    sleep.assert_has_calls([call(0.05), call(0.05)])
    assert canvas.Clear.call_count == 2

