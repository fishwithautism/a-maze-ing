"""This module defines the MazeGenerator class,
which is responsible for generating and solving
mazes using Prim's algorithm.
The maze is represented as a 2D grid where each cell
is an integer that encodes the presence of walls in four
directions (N, E, S, W) using bitwise operations.
The class provides methods to generate the maze, solve it,
and convert the solution path into directional moves."""
from typing import List, Tuple, Any
import random
from time import sleep
from copy import deepcopy


class MazeGenerator:
    """A class to generate and solve mazes using Prim's algorithm.
    The maze is represented as a 2D grid where each cell is an integer
    that encodes the presence of walls in four directions (N, E, S, W)
    using bitwise operations."""
    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int],
                 exit: Tuple[int, int],
                 perfect: bool,
                 algo: str = "Prim",
                 seed: Any = None) -> None:
        """Initialize the maze generator with the specified parameters."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.algorithm = algo
        random.seed(seed)
        self.maze = [[15 for _ in range(width)] for _ in range(height)]

    def get_2_shape(self) -> List[tuple[int, int]]:
        """Returns the coordinates of the "2" shape in the maze,
        which is a specific pattern of walls that must be preserved
        during maze generation."""
        gx, gy = (self.width // 2, self.height // 2)
        _2_shape = [
            (gx + 1, gy), (gx + 2, gy), (gx + 3, gy),
            (gx + 3, gy - 1), (gx + 3, gy - 2), (gx + 2, gy - 2),
            (gx + 1, gy - 2), (gx + 1, gy + 1), (gx + 1, gy + 2),
            (gx + 2, gy + 2), (gx + 3, gy + 2)
            ]
        return _2_shape

    def get_4_shape(self) -> List[tuple[int, int]]:
        """Returns the coordinates of the "4" shape in the maze,"""
        gx, gy = (self.width // 2, self.height // 2)
        _4_shape = [
                (gx - 1, gy), (gx - 2, gy), (gx - 3, gy),
                (gx - 3, gy - 1), (gx - 3, gy - 2), (gx - 1, gy + 1),
                (gx - 1, gy + 2)
            ]
        return _4_shape

    def generate(self, animation: bool = False, wall_color: str = "") -> None:
        """Generates the maze using Prim's algorithm while ensuring that
        the entry and exit points do not conflict with the predefined "2"
        and "4" shapes in the maze. If the maze is not perfect, it will
        introduce additional paths to create loops."""
        if self.entry in self.get_2_shape() or (
             self.entry in self.get_4_shape()):
            raise ValueError("entry or exit are conflicting with 42 shape")
        if self.exit in self.get_2_shape() or (
             self.exit in self.get_4_shape()):
            raise ValueError("entry or exit are conflicting with 42 shape")
        self._generate_prim(animation, wall_color)
        if not self.perfect:
            self._make_nonperfect()

    def solve_maze(self) -> List[Tuple[int, int]]:
        """getter method for the maze solver,
        which returns the path from the entry"""
        return self._maze_solver()

    def get_path(self, path: List[Tuple[int, int]]) -> List[str]:
        """Converts a list of coordinates representing a path through
        the maze into a list of directional moves (N, E, S, W) based on
        the changes in x and y coordinates between consecutive points
        in the path."""
        path_list = []
        for i in range(len(path) - 1):
            x, y = path[i]
            a, b = path[i + 1]
            if x > a:
                path_list.append('W')
            if x < a:
                path_list.append('E')
            if y < b:
                path_list.append('S')
            if y > b:
                path_list.append('N')
        return (path_list)

    def _generate_prim(self, animation: bool, wall_color: str) -> None:
        """Generates the maze using Prim's algorithm, starting
        from the entry point and carving out paths while ensuring
        that the "2" and "4" shapes are preserved. The algorithm maintains
        a list of visited cells and randomly selects a cell from this list
        to explore its neighbors, carving out paths as it goes."""
        visited: List[Tuple[int, int]] = [self.entry]
        while visited:
            cx, cy = random.choice(visited)
            neighbours_list = []
            directions = [(cx + 1, cy),
                          (cx - 1, cy),
                          (cx, cy + 1),
                          (cx, cy - 1)]
            for dx, dy in directions:
                if 0 <= dy < self.height and (
                     0 <= dx < self.width
                     ) and (
                         (dx, dy) not in self.get_2_shape()
                         ) and (
                         (dx, dy) not in self.get_4_shape()
                         ) and self.maze[dy][dx] == 15:
                    neighbours_list.append((dx, dy))
            if not neighbours_list:
                visited.remove((cx, cy))
                continue
            rx, ry = random.choice(neighbours_list)
            if rx > cx:
                self.maze[ry][rx] &= ~8
                self.maze[cy][cx] &= ~2
            if rx < cx:
                self.maze[ry][rx] &= ~2
                self.maze[cy][cx] &= ~8
            if ry > cy:
                self.maze[ry][rx] &= ~1
                self.maze[cy][cx] &= ~4
            if ry < cy:
                self.maze[ry][rx] &= ~4
                self.maze[cy][cx] &= ~1
            visited.append((rx, ry))
            if animation:
                try:
                    from render import render_maze
                    print("\033[2J\033[H")
                    render_maze(self.maze, self.entry, self.exit, wall_color)
                    sleep(0.04)
                except ImportError:
                    pass

    def _make_nonperfect(self) -> None:
        """Introduces additional paths in the maze to create loops, making
        it non-perfect.This is done by randomly removing walls between
        adjacent cells that are not partof the "2" or "4" shapes."""
        for cy in range(self.height):
            for cx in range(self.width):
                rand = random.random()
                if rand < 0.3:
                    neighbours = self._get_neighbours((cx, cy))
                    if neighbours:
                        rx, ry = random.choice(neighbours)
                        if rx > cx:
                            self.maze[ry][rx] &= ~8
                            self.maze[cy][cx] &= ~2
                        elif rx < cx:
                            self.maze[ry][rx] &= ~2
                            self.maze[cy][cx] &= ~8
                        elif ry > cy:
                            self.maze[ry][rx] &= ~1
                            self.maze[cy][cx] &= ~4
                        else:
                            self.maze[ry][rx] &= ~4
                            self.maze[cy][cx] &= ~1

    def _get_neighbours(
            self, coordinates: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Returns a list of neighboring cells that can be connected to
        the current cell without violating the structure of the maze"""
        cx, cy = coordinates
        if (cx, cy) in self.get_2_shape() or (cx, cy) in self.get_4_shape():
            return []
        neighbours_list = []
        directions = [(cx + 1, cy),
                      (cx - 1, cy),
                      (cx, cy + 1),
                      (cx, cy - 1)]
        for dx, dy in directions:
            if 0 <= dy < self.height and (
                    0 <= dx < self.width
                    ) and (
                    (dx, dy) not in self.get_2_shape()
                    ) and (
                    (dx, dy) not in self.get_4_shape()
                    ):
                neighbours_list.append((dx, dy))
        return neighbours_list

    def _maze_solver(self) -> List[Tuple[int, int]]:
        """Solves the maze using a breadth-first search (BFS) algorithm,
        starting from the entry point and exploring all possible paths
        until it reaches the exit."""
        path_grid = [
            [0 for _ in range(self.width)] for _ in range(self.height)]
        paths: List[List[Tuple[int, int]]] = [[self.entry]]
        x, y = self.entry
        path_grid[y][x] = 1
        while True:
            new_paths = []
            for path in paths:
                x, y = path[len(path) - 1]
                binary = format(self.maze[y][x], "04b")
                directions = [
                    (x - 1, y),
                    (x, y + 1),
                    (x + 1, y),
                    (x, y - 1)
                ]
                for i in range(4):
                    x, y = directions[i]
                    if binary[i] == '0' and not path_grid[y][x]:
                        new_path = deepcopy(path)
                        new_path.append((x, y))
                        new_paths.append(new_path)
                        path_grid[y][x] = 1
                        if (x, y) == self.exit:
                            return new_path
            paths = new_paths
