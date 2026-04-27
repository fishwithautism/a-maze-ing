""" Renders the maze in the terminal using ASCII characters.
The maze is represented as a 2D list of integers, where each
integer encodes the presence of walls in the four cardinal
directions (N, E, S, W) using bitwise flags. The function
iterates through each cell in the maze and prints the appropriate
characters to represent walls and paths. The entry and exit points
are highlighted with different colors, and the path from entry to exit
is also highlighted if provided. The maze is enclosed within a border
for better visualization."""


def render_maze(
        maze: list[list[int]], start: tuple[int, int],
        end: tuple[int, int],
        wall_color: str, path: list[tuple[int, int]] = []) -> None:

    RESET = '\033[0m'
    WALL = f"{wall_color}  {RESET}"

    for row in range(len(maze)):
        print(f"\n{WALL}", end="")
        for cell in maze[row]:
            binary = format(cell, '04b')
            if binary[3] == "1":
                print(WALL * 2, end="")
            else:
                print(f"  {WALL}", end="")
        print(f"\n{WALL}", end="")
        for cell in range(len(maze[row])):
            if maze[row][cell] == 15:
                print("\033[41m  \033[0m", end="")
            elif (cell, row) == start:
                print("\033[43m  \033[0m", end="")
            elif (cell, row) == end:
                print("\033[44m  \033[0m", end="")
            elif (cell, row) in path:
                print("\033[42m  \033[0m", end="")
            else:
                print("  ", end="")
            binary = format(maze[row][cell], '04b')
            if binary[2] == "1":
                print(f"{WALL}", end="")
            else:
                print("  ", end="")
    print(f"\n{WALL}", end="")
    for _ in range(len(maze[0])):
        print(WALL * 2, end="")
    print()


def display_menu() -> None:

    CYAN = '\033[36m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    print(f"\n{CYAN}{BOLD}╭─── A-Maze-ing ──────────────────────╮{RESET}")
    print(f"{CYAN}│{RESET} {GREEN}[1]{RESET} Re-generate a new "
          f"maze         {CYAN} │{RESET}")
    print(f"{CYAN}│{RESET} {GREEN}[2]{RESET} Show/Hide path from "
          f"entry/exit {CYAN} │{RESET}")
    print(f"{CYAN}│{RESET} {GREEN}[3]{RESET} Change maze wall "
          f"colours       {CYAN} │{RESET}")
    print(f"{CYAN}│{RESET} {GREEN}[4]{RESET} Animate seeded "
          f"maze generation {CYAN} │{RESET}")
    print(f"{CYAN}│{RESET} {GREEN}[5]{RESET} Quit    "
          f"                       {CYAN} │{RESET}")
    print(f"{CYAN}╰─────────────────────────────────────╯{RESET}")
