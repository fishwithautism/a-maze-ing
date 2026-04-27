*This project has been created as part of the 42 curriculum by mohael-g, azennani.*

---

# A-Maze-ing 🌀

> *"A labyrinth is not a place to be lost, but a path to be found."*

## Description

**A-Maze-ing** is a Python maze generator and visualizer. It reads a configuration file, generates a randomized maze using **Prim's algorithm**, and renders it directly in the terminal with full color support. The maze always embeds a visible **"42"** pattern made of fully closed cells, and can operate in both *perfect* mode (single unique path between entry and exit) and *non-perfect* mode (multiple routes).

Key features:
- Prim's algorithm with optional seed for reproducibility
- Perfect and non-perfect maze modes
- Terminal ASCII rendering with colored walls, entry, exit, and solution path
- Interactive menu: regenerate, show/hide path, change colors, animated generation
- Hexadecimal output file with BFS-computed shortest path
- Reusable `MazeGenerator` class packaged as a pip-installable library (`mazegen`)

---

## Instructions

### Requirements

- Python 3.10 or later
- Dependencies: `flake8`, `mypy`, `build` (installed via `make install`)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd a-maze-ing

# Install dependencies
make install
```

### Running

```bash
make run
# or directly:
python3 a_maze_ing.py config.txt
```

### Other Makefile targets

| Target | Description |
|---|---|
| `make install` | Install project dependencies (flake8, mypy, build) |
| `make run` | Generate and display the maze |
| `make debug` | Run with Python's built-in debugger (pdb) |
| `make lint` | Run flake8 + mypy with standard flags |
| `make lint-strict` | Run flake8 + mypy with `--strict` |
| `make build` | Build the `mazegen` pip package (.whl and .tar.gz) |
| `make clean` | Remove `__pycache__`, `.mypy_cache`, build artifacts |

### Interactive menu

Once the maze is displayed, you can:

```
[1] Re-generate a new maze
[2] Show / Hide the shortest path from entry to exit
[3] Change maze wall colours  (White / Orange / Pink / Brown)
[4] Animate seeded maze generation
[5] Quit
```

---

## Configuration file format

The program is launched with:

```bash
python3 a_maze_ing.py config.txt
```

The config file uses `KEY=VALUE` pairs (one per line). Lines starting with `#` are comments and are ignored. Keys are **case-insensitive**.

### Mandatory keys

| Key | Type | Description | Example |
|---|---|---|---|
| `WIDTH` | int > 0 | Number of columns | `WIDTH=21` |
| `HEIGHT` | int > 0 | Number of rows | `HEIGHT=21` |
| `ENTRY` | x,y | Entry cell coordinates | `ENTRY=0,0` |
| `EXIT` | x,y | Exit cell coordinates | `EXIT=20,20` |
| `OUTPUT_FILE` | string | Path of the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | bool | Single-path maze? | `PERFECT=True` |

### Optional keys

| Key | Type | Description | Example |
|---|---|---|---|
| `SEED` | any | Random seed for reproducibility | `SEED=42` |

### Example `config.txt`

```
# A-Maze-ing default configuration
WIDTH=21
HEIGHT=21
ENTRY=0,0
EXIT=20,20
PERFECT=True
OUTPUT_FILE=maze.txt
# SEED=42
```

> **Constraints:** WIDTH and HEIGHT must each be at least 14 to fit the "42" pattern. ENTRY and EXIT must be inside the maze bounds and must differ from each other.

---

## Output file format

Each cell is encoded as one hexadecimal digit where each bit flags a closed wall:

| Bit | Direction |
|---|---|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

`1` = wall closed, `0` = wall open.  
Cells are written row by row, one row per line.

After an empty line, three additional lines are appended:

1. Entry coordinates
2. Exit coordinates
3. Shortest path from entry to exit using `N`, `E`, `S`, `W`

---

## Maze generation algorithm

The project uses **Prim's randomized algorithm**:

1. Start from the entry cell; mark it visited.
2. Maintain a list of all visited cells.
3. At each step, pick a random visited cell; look for unvisited neighbours that are not part of the "42" pattern.
4. If found, carve a passage to a random one (remove the shared wall on both sides) and add it to the list.
5. If no unvisited neighbour exists, remove the cell from the list.
6. Repeat until the list is empty (all reachable cells are connected).

For **non-perfect** mazes, an extra pass randomly removes ~30 % of remaining walls to introduce loops.

### Why Prim's algorithm?

- Produces **perfect mazes** (spanning trees) by design — exactly what the `PERFECT=True` requirement demands.
- The random frontier list gives a **wide, open feel** (less biased toward long corridors than recursive backtracking).
- Simple to adapt to **preserve reserved cells** (the "42" pattern) by skipping them during neighbour lookup.
- Straightforward to seed via `random.seed()` for full reproducibility.

---

## Reusable module — `mazegen`

The `MazeGenerator` class lives in `mazegenerator.py` and is distributed as a standalone pip package (`mazegen-1.0.0-py3-none-any.whl`).

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
# or from source:
pip install .
```

### Quick-start example

```python
from mazegenerator import MazeGenerator

# Create a 21×21 perfect maze with a fixed seed
gen = MazeGenerator(
    width=21,
    height=21,
    entry=(0, 0),
    exit=(20, 20),
    perfect=True,
    seed=42
)

gen.generate()          # Build the maze

# Access the raw grid (list[list[int]], hex-encoded walls)
grid = gen.maze         # gen.maze[row][col]

# Solve the maze — returns list of (x, y) coordinates
path_coords = gen.solve_maze()

# Convert coordinates to directional moves (N/E/S/W)
directions = gen.get_path(path_coords)
print("".join(directions))   # e.g. "EESSSSEENE..."
```

### Custom parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `width` | int | — | Number of columns |
| `height` | int | — | Number of rows |
| `entry` | tuple[int,int] | — | Entry cell `(x, y)` |
| `exit` | tuple[int,int] | — | Exit cell `(x, y)` |
| `perfect` | bool | — | Perfect maze (single path) |
| `algo` | str | `"Prim"` | Algorithm name (informational) |
| `seed` | any | `None` | Random seed for reproducibility |

### Accessing the generated structure

```python
# Raw 2-D grid
gen.maze                # list[list[int]]

# Solve and get coordinate path
coords = gen.solve_maze()         # list[tuple[int,int]]

# Convert to cardinal directions
moves  = gen.get_path(coords)     # list[str]  e.g. ['E','E','S',...]
```

> The internal grid format uses the same bit encoding as the output file (bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West). A set bit means the wall is **closed**.

### Building the package from source

```bash
python3 -m venv venv && source venv/bin/activate
pip install build
python3 -m build          # produces dist/mazegen-*.whl and dist/mazegen-*.tar.gz
```

---

## Resources

### References

- [Prim's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Think Labyrinth — Maze algorithms overview](https://www.astrolog.org/labyrnth/algrithm.htm)
- [Python `random` module docs](https://docs.python.org/3/library/random.html)
- [Python packaging guide (setuptools)](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [flake8 docs](https://flake8.pycqa.org/) / [mypy docs](https://mypy.readthedocs.io/)

### AI usage

Claude (Anthropic) was used for the following tasks during this project:

- **README structure & wording** — drafting and refining this document.
- **Makefile** — generating the standard targets (`install`, `run`, `debug`, `lint`, `clean`, `build`) in line with the subject requirements.
- **Docstrings review** — suggesting PEP 257 / Google-style improvements.

All AI-generated content was reviewed, understood, tested, and adjusted by the team before inclusion. No code was blindly copy-pasted.

---

## Team & project management

### Team members and roles

| Member | Role |
|---|---|
| mohael-g | Configuration parser (`config_parser.py`), main entry script (`a_maze_ing.py`) |
| azennani | Maze generation algorithm, renderer, BFS solver, output file format, package build, debugging |

### Planning

| Phase | Planned | Actual |
|---|---|---|
| Config parser | Day 1 | Day 1 |
| Maze generator (Prim's) + "42" pattern | Day 2–3 | Day 2–4 |
| BFS solver + output file | Day 3 | Day 4 |
| Terminal renderer + interactive menu | Day 4 | Day 5 |
| Package build + README + Makefile | Day 5 | Day 5 |

### What worked well

- Prim's algorithm was a natural fit — clean implementation and easy to extend.
- The bitwise wall encoding kept the grid compact and the renderer straightforward.
- Seeded random made debugging reproducible.

### What could be improved

- The "42" shape coordinates are hard-coded relative to the center — a more flexible pattern system would be nicer.
- The terminal renderer has no scrolling; very large mazes overflow the screen.
- Adding Kruskal's or recursive backtracker as alternative algorithms (bonus) would be a good next step.

### Tools used

- **VS Code** with the Python and Pylance extensions
- **Git** for version control
- **Claude (Anthropic)** for documentation drafting and code review assistance
- **mypy** and **flake8** for static analysis
