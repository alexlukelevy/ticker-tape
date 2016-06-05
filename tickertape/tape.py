import time


class Tape:

    def __init__(self, matrix, color, font, draw, sleep=time.sleep):
        self._matrix = matrix
        self._color = color
        self._font = font
        self._draw = draw
        self._sleep = sleep
        self._offscreen_canvas = self._matrix.CreateFrameCanvas()

    def display(self, text):
        print('Tape displaying: ' + text)
        canvas = self._offscreen_canvas
        pos = self._offscreen_canvas.width
        len = self.draw_text(pos, 10, text)

        while pos + len > 0:
            canvas.Clear()
            len = self.draw_text(pos, 10, text)
            pos -= 1
            self._sleep(0.05)
            self._offscreen_canvas = self._matrix.SwapOnVSync(canvas)

    def draw_text(self, x, y, text):
        return self._draw(self._offscreen_canvas, self._font, x, y, self._color, text)
