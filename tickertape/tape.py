import time
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix


class Tape:

    def __init__(self):
        self.matrix = RGBMatrix(16, 1, 1)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.colour = graphics.Color(255, 255, 0)
        self.font = graphics.Font()
        self.font.LoadFont("../fonts/7x13.bdf")

    def display(self, text):
        print('Tape displaying: ' + text)
        canvas = self.offscreen_canvas
        pos = self.offscreen_canvas.width
        len = self.draw_text(pos, 10, text)

        while pos + len > 0:
            canvas.Clear()
            len = self.draw_text(pos, 10, text)
            pos -= 1
            time.sleep(0.05)
            self.offscreen_canvas = self.matrix.SwapOnVSync(canvas)

    def draw_text(self, x, y, text):
        return graphics.DrawText(self.offscreen_canvas, self.font, x, y, self.colour, text)