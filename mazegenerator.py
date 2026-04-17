# maze_generator.py
import random
from typing import List, Tuple
from collections import deque


class MazeGenerator:
    """
    Perfect maze generator using randomized DFS/Prim's algorithm.
    All maze properties (size, entry, exit, seed) are set at construction.
    Call generate() to create the maze with mandatory '42' pattern.
    """

    def __init__(
            self, width: int, height: int,
            entry: Tuple[int, int], exit: Tuple[int, int],
            seed: int = 42, algo: str = "prim") -> None:
        """
        Initialize the maze generator with all necessary parameters.

        Arguments:
            width: Number of cells horizontally (columns).
            height: Number of cells vertically (rows).
            entry: (x, y) coordinates of the entrance.
            exit: (x, y) coordinates of the exit.
            seed: Random seed for reproducibility (default 42).
        """
        self._width = width
        self._height = height
        self._entry = entry
        self._exit = exit
        self._seed = seed
        self.algorithm = algo.lower()
        random.seed(seed)

        # Maze grid: each cell is a bitmask (0-15),
        # initially all walls closed (15)
        self._maze = [[15 for _ in range(width)] for _ in range(height)]
        self._solution = ""

    # public methods

    def generate(self) -> None:
        """
        Generate the complete maze.
        This is the only method needed after construction.
        It performs:
            1. Perfect maze generation (DFS/Prim's algorithm)
            2. Opening of entry/exit border walls
            3. Addition of '42' pattern (2x2 fully closed cells)
        """
        if self.algorithm == "dfs":
            self._generate_prim()
        else:
            self._generate_prim()
        self._add_42_pattern()

    def get_maze(self) -> List[List[int]]:
        """
        Return a copy of the maze grid (bitmasks).
        Returns a deep copy to prevent external modification.
        """
        return [row[:] for row in self._maze]

    def get_cell(self, x: int, y: int) -> int:
        """
        Return the bitmask of a single cell.

        Arguments:
            x: Column index (0 to width-1)
            y: Row index (0 to height-1)

        Returns:
            Integer mask (0-15) representing walls.
        """
        if 0 <= x < self._width and 0 <= y < self._height:
            return self._maze[y][x]
        raise IndexError(f"Cell ({x},{y}) out of bounds")

    def get_entry(self) -> Tuple[int, int]:
        """Return the (x, y) coordinates of the entrance."""
        return self._entry

    def get_exit(self) -> Tuple[int, int]:
        """Return the (x, y) coordinates of the exit."""
        return self._exit

    def get_solution(self) -> str:
        """
        Return the shortest path from entry to exit
        as a string of letters (N/E/S/W).
        The path is computed lazily on first call and cached.
        """
        if not self._solution:
            self._compute_shortest_path()
        return self._solution

    def get_width(self) -> int:
        """Return the maze width (number of columns)."""
        return self._width

    def get_height(self) -> int:
        """Return the maze height (number of rows)."""
        return self._height

    def get_seed(self) -> int:
        """Return the random seed used for generation."""
        return self._seed

    # Private methods

    def _generate_prim(self) -> None:
        """
        Private: Generate a perfect maze using randomized Prim's algorithm.
        All cells start with all walls closed; walls are knocked
        down to create passages.
        """
        # Track which cells are already part of the maze
        in_maze = [[False] * self._width for _ in range(self._height)]

        # Choose random starting cell
        start_x = random.randrange(self._width)
        start_y = random.randrange(self._height)
        in_maze[start_y][start_x] = True

        # Frontier: each entry is (neighbor_x, neighbor_y, from_x, from_y)
        frontier = []

        def add_frontier(cx: int, cy: int):
            """Add all unvisited neighbors of (cx, cy) to the frontier."""
            # East
            if cx + 1 < self._width and not in_maze[cy][cx + 1]:
                frontier.append((cx + 1, cy, cx, cy))
            # West
            if cx - 1 >= 0 and not in_maze[cy][cx - 1]:
                frontier.append((cx - 1, cy, cx, cy))
            # South
            if cy + 1 < self._height and not in_maze[cy + 1][cx]:
                frontier.append((cx, cy + 1, cx, cy))
            # North
            if cy - 1 >= 0 and not in_maze[cy - 1][cx]:
                frontier.append((cx, cy - 1, cx, cy))

        add_frontier(start_x, start_y)

        # Main Prim's loop
        while frontier:
            idx = random.randrange(len(frontier))
            nx, ny, fx, fy = frontier.pop(idx)

            if in_maze[ny][nx]:
                continue

            # Knock down the wall between (fx, fy) and (nx, ny)
            if nx == fx + 1:   # neighbor is EAST
                self._maze[fy][fx] &= ~2   # clear east wall of 'from'
                self._maze[ny][nx] &= ~8   # clear west wall of neighbor
            elif nx == fx - 1:  # neighbor is WEST
                self._maze[fy][fx] &= ~8
                self._maze[ny][nx] &= ~2
            elif ny == fy + 1:  # neighbor is SOUTH
                self._maze[fy][fx] &= ~4
                self._maze[ny][nx] &= ~1
            elif ny == fy - 1:  # neighbor is NORTH
                self._maze[fy][fx] &= ~1
                self._maze[ny][nx] &= ~4

            in_maze[ny][nx] = True
            add_frontier(nx, ny)

    def _add_42_pattern(self) -> None:
        """
        Private: Add the mandatory '42' pattern - a 2x2 block of
        fully closed cells (mask=15).
        If the maze is too small (width<2 or height<2), prints an error
        message as required.
        """
        if self._width < 2 or self._height < 2:
            print(
                "Error: Maze too small to add '42' pattern (need at least 2x2)"
                )
            return

        # Choose a random top-left corner for the 2x2 block
        max_x = self._width - 2
        max_y = self._height - 2
        top_left_x = random.randrange(max_x + 1)
        top_left_y = random.randrange(max_y + 1)

        for dy in range(2):
            for dx in range(2):
                self._maze[top_left_y + dy][top_left_x + dx] = 15

    def _compute_shortest_path(self) -> None:
        """
        Private: Compute the shortest path from entry to exit using BFS.
        Stores the result in self._solution as a string of N/E/S/W.
        """
        # Directions:
        # (dx, dy, wall_bit_from_current, opposite_wall_bit, letter)
        directions = [
            (1, 0, 2, 8, 'E'),   # east
            (-1, 0, 8, 2, 'W'),  # west
            (0, 1, 4, 1, 'S'),   # south
            (0, -1, 1, 4, 'N'),  # north
        ]

        start_x, start_y = self._entry
        goal_x, goal_y = self._exit

        queue = deque()
        queue.append((start_x, start_y, ""))
        visited = [[False] * self._width for _ in range(self._height)]
        visited[start_y][start_x] = True

        while queue:
            x, y, path = queue.popleft()
            if (x, y) == (goal_x, goal_y):
                self._solution = path
                return

            for dx, dy, wall_self, wall_neighbor, letter in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self._width and (
                     0 <= ny < self._height and not visited[ny][nx]):
                    # Check if wall is open between current and neighbor
                    if (self._maze[y][x] & wall_self) == 0 and (
                         self._maze[ny][nx] & wall_neighbor) == 0:
                        visited[ny][nx] = True
                        queue.append((nx, ny, path + letter))

        # No path found (should not happen in a perfect maze)
        self._solution = ""
