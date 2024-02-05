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


def main():
    window = Window(600, 800)
    window.start()


main()
