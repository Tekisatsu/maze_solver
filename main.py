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


def main():
    window = Window(600, 800)
    line = Line(30, 30, 300, 300, window.canvas, 'blue')
    line.draw()
    window.start()
    window.wait_for_close()


main()
