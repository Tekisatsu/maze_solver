import sys
from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.width = width
        self.height = height
        self.root.title('Maze')
        self.canvas = Canvas(self.root, height=height, width=width)
        self.canvas.pack()
        self.running = False
        self.root.protocol('WM_DELETE_WINDOW', self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def start(self):
        self.root.geometry(f'{self.width}x{self.height}')
        self.wait_for_close()
        self.root.mainloop()

    def close(self):
        self.running = False
        self.root.destroy()
        sys.exit(0)


class Point:
    def __init__(self, x_1=0, y_1=0):
        self.x = x_1
        self.y = y_1


class Line:
    def __init__(self, x_1, x_2, y_1, y_2, canvas, colour='black'):
        self.coordinates = (x_1, x_2, y_1, y_2)
        self.colour = colour
        self.canvas = canvas

    def draw(self):
        self.canvas.create_line(*self.coordinates, fill=self.colour)


class Cell:
    def __init__(self, i, j, size, canvas):
        self.has_right_wall = True
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = i*size
        self._x2 = self._x1+size
        self._y1 = j*size
        self._y2 = self._y1+size
        self._canvas = canvas

    def draw(self):
        if self.has_left_wall:
            Line(self._x1, self._y1, self._x1, self._y2, self._canvas).draw()
        if self.has_right_wall:
            Line(self._x2, self._y1, self._x2, self._y2, self._canvas).draw()
        if self.has_top_wall:
            Line(self._x1, self._y1, self._x2, self._y1, self._canvas).draw()
        if self.has_bottom_wall:
            Line(self._x1, self._y2, self._x2, self._y2, self._canvas).draw()


def main():
    window = Window(600, 800)
    cell = Cell(3, 2, 50, window.canvas)
    cell.draw()
    window.start()
    window.wait_for_close()


main()
