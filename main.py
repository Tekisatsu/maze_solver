import sys
from tkinter import Tk, BOTH, Canvas
import time
import random


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

    def start(self):
        self.root.geometry(f'{self.width}x{self.height}')
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
        self._canvas = canvas

    def draw(self):
        self._canvas.create_line(*self.coordinates, fill=self.colour)


class Cell:
    def __init__(self, i, j, size, canvas=None):
        self.has_right_wall = True
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = i*size
        self._x2 = self._x1+size
        self._y1 = j*size
        self._y2 = self._y1+size
        self._canvas = canvas
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        if self.has_left_wall:
            Line(x1, y1, x1, y2, self._canvas).draw()
        else:
            Line(x1, y1, x1, y2, self._canvas, colour='white').draw()
        if self.has_right_wall:
            Line(x2, y1, x2, y2, self._canvas).draw()
        else:
            Line(x2, y1, x2, y2, self._canvas, colour='white').draw()
        if self.has_top_wall:
            Line(x1, y1, x2, y1, self._canvas).draw()
        else:
            Line(x1, y1, x2, y1, self._canvas, colour='white').draw()
        if self.has_bottom_wall:
            Line(x1, y2, x2, y2, self._canvas).draw()
        else:
            Line(x1, y2, x2, y2, self._canvas, colour='white').draw()

    def draw_move(self, to_cell, undo=False):
        center_x = (self._x1 + self._x2)//2
        center_y = (self._y1 + self._y2)//2
        to_cell_center_x = (to_cell._x1 + to_cell._x2)//2
        to_cell_center_y = (to_cell._y1 + to_cell._y2)//2
        if undo is True:
            Line(center_x, center_y, to_cell_center_x, to_cell_center_y, self._canvas, 'grey').draw()
        Line(center_x, center_y, to_cell_center_x, to_cell_center_y, self._canvas, 'red').draw()


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size,
        win=None,
        seed=None
    ):

        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size = cell_size
        self.win = win
        self.cells_to_redraw = []
        if seed:
            random.seed(seed)
        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for col in range(self.num_cols):
            column_list = []
            for row in range(self.num_rows):
                cell = Cell(col, row, self.cell_size, self.win.canvas)
                column_list.append(cell)
            self._cells.append(column_list)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self.win is None:
            return
        x1 = self.x1 + i * self.cell_size
        y1 = self.y1 + j * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.02)

    def _break_enter_exit(self):
        self._cells[0][0].has_left_wall = False
        self._cells[self.num_cols-1][self.num_rows-1].has_right_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)
        self._draw_cell(0, 0)

    def _break_walls_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True
        cords = []
        if i > 0 and not self._cells[i-1][j].visited:
            cords.append((i-1, j))
        if i < self.num_cols - 1 and not self._cells[i+1][j].visited:
            cords.append((i+1, j))
        if j > 0 and not self._cells[i][j-1].visited:
            cords.append((i, j-1))
        if j < self.num_rows - 1 and not self._cells[i][j+1].visited:
            cords.append((i, j+1))
        elif not cords:
            self._draw_cell(i, j)
            return
        chosen = random.choice(cords)
        if chosen[0] == i+1:
            current.has_top_wall = False
            self._cells[chosen[0]][chosen[1]].has_bottom_wall = False
        if chosen[0] == i-1:
            current.has_bottom_wall = False
            self._cells[chosen[0]][chosen[1]].has_top_wall = False
        if chosen[1] == j+1:
            current.has_left_wall = False
            self._cells[chosen[0]][chosen[1]].has_right_wall = False
        if chosen[1] > j-1:
            current.has_right_wall = False
            self._cells[chosen[0]][chosen[1]].has_left_wall = False
        self._draw_cell(i, j)
        self._break_walls_r(chosen[0], chosen[1])
        self._draw_cell(chosen[0], chosen[1])

    def _reset_visited(self):
        for i in self._cells:
            for k in i:
                k.visited = False


def main():
    window = Window(1200, 1200)
    num_cols = 10
    num_rows = 12
    cell_size = 50
    maze = Maze(50, 50, num_rows, num_cols, cell_size, window, 10)
    maze._reset_visited()
    maze._break_walls_r(0, 0)
    maze._break_enter_exit()
    window.redraw()
    window.start()


main()
