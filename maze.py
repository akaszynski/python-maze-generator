#!/usr/bin/python

import random
import argparse

from PIL import Image, ImageDraw


class Cell:
    def __init__(self):
        self.north = True
        self.south = True
        self.east = True
        self.west = True
        self.visited = False


class Maze:
    def __init__(self, width=20, height=20, cell_width=20):
        self.width = width
        self.height = height
        self.cw = cell_width
        self.cells = [[Cell() for _ in range(height)] for _ in range(width)]

    def generate(self):
        x, y = random.choice(range(self.width)), random.choice(range(self.height))
        self.cells[x][y].visited = True
        path = [(x, y)]

        while not all(all(c.visited for c in cell) for cell in self.cells):
            x, y = path[len(path) - 1][0], path[len(path) - 1][1]

            good_adj_cells = []
            if self.exists(x, y - 1) and not self.cells[x][y - 1].visited:
                good_adj_cells.append('north')
            if self.exists(x, y + 1) and not self.cells[x][y + 1].visited:
                good_adj_cells.append('south')
            if self.exists(x + 1, y) and not self.cells[x + 1][y].visited:
                good_adj_cells.append('east')
            if self.exists(x - 1, y) and not self.cells[x - 1][y].visited:
                good_adj_cells.append('west')

            if good_adj_cells:
                go = random.choice(good_adj_cells)
                if go == 'north':
                    self.cells[x][y].north = False
                    self.cells[x][y - 1].south = False
                    self.cells[x][y - 1].visited = True
                    path.append((x, y - 1))
                if go == 'south':
                    self.cells[x][y].south = False
                    self.cells[x][y + 1].north = False
                    self.cells[x][y + 1].visited = True
                    path.append((x, y + 1))
                if go == 'east':
                    self.cells[x][y].east = False
                    self.cells[x + 1][y].west = False
                    self.cells[x + 1][y].visited = True
                    path.append((x + 1, y))
                if go == 'west':
                    self.cells[x][y].west = False
                    self.cells[x - 1][y].east = False
                    self.cells[x - 1][y].visited = True
                    path.append((x - 1, y))
            else:
                path.pop()

    def exists(self, x, y):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return False
        return True

    def get_direction(self, direction, x, y):
        if direction == 'north':
            return x, y - 1
        if direction == 'south':
            return x, y + 1
        if direction == 'east':
            return x + 1, y
        if direction == 'west':
            return x - 1, y

    def draw(self, background_color='white', line_color='black'):
        canvas_width, canvas_height = self.cw * self.width, self.cw * self.height
        im = Image.new('RGB', (canvas_width, canvas_height), color=background_color)
        draw = ImageDraw.Draw(im)

        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y].north:
                    draw.line(
                        (x * self.cw, y * self.cw, (x + 1) * self.cw, y * self.cw), line_color)
                if self.cells[x][y].south:
                    draw.line((x * self.cw, (y + 1) * self.cw, (x + 1) * self.cw,
                               (y + 1) * self.cw), line_color)
                if self.cells[x][y].east:
                    draw.line(((x + 1) * self.cw, y * self.cw, (x + 1) * self.cw,
                               (y + 1) * self.cw), line_color)
                if self.cells[x][y].west:
                    draw.line(
                        (x * self.cw, y * self.cw, x * self.cw, (y + 1) * self.cw), line_color)

        im.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='maze')

    parser.add_argument('width', type=int,
                        default=20,
                        help='Maze width')

    parser.add_argument('height', type=int,
                        default=20,
                        help='Maze height')

    parser.add_argument('--background-color', type=str,
                        required=False, default='white',
                        help='Background color')

    parser.add_argument('--line-color', type=str,
                        required=False, default='black',
                        help='Line color')

    args = parser.parse_args()
    maze = Maze(width=args.width, height=args.height)
    maze.generate()
    maze.draw(args.background_color, args.line_color)
