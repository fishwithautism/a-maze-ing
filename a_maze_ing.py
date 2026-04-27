import sys
from config_parser import parse_config, ConfigParseError
from mazegenerator import MazeGenerator
from render import render_maze, display_menu


def main() -> None:
    #  COLORS
    WHITE = '\033[48;2;230;230;230m'
    YELLOW = '\033[33m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    ORANGE = '\033[48;5;208m'
    PINK = '\033[48;5;206m'
    BROWN = '\033[48;5;94m'

    try:
        if len(sys.argv) < 2:
            print("\nUsage: \n\t \033[32mpython3 a_maze_ing.py "
                  "config.txt\033[0m\n")
            sys.exit(1)
        try:
            config = parse_config(sys.argv[1])
        except (ConfigParseError, OSError) as e:
            print(f"\033[31mError:\033[0m \033[33m{e}\033[0m")
            sys.exit(1)
        if config["HEIGHT"] < 14 or config[
             "WIDTH"] < 14:
            raise ValueError(
                "Maze dimensions must be at least 14x14 to "
                "accommodate the 4 and 2 shapes.")
        seed = None
        if "SEED" in config:
            seed = config["SEED"]
        maze = MazeGenerator(
         width=config["WIDTH"],
         height=config["HEIGHT"],
         entry=config["ENTRY"],
         exit=config["EXIT"],
         perfect=config["PERFECT"],
         seed=seed)
        maze.generate()
        path = maze.solve_maze()
        result = "\n".join(
            "".join(format(num, "X") for num in row)
            for row in maze.maze
        )
        try:
            with open(config["OUTPUT_FILE"], "w") as output:
                output.write(result)
                output.write("\n\n")
                output.write(f"Entry cell is: \n\t{config["ENTRY"]}")
                output.write("\n\n")
                output.write(f"Exit cell is: \n\t{config["EXIT"]}\n")
                output.write("\n")
                output.write(f"Path is: \n{"".join(maze.get_path(path))}")
        except Exception:
            raise Exception("\033[33moutput file format is wrong\033[0m ")
        wall_color = WHITE
        print("\033[2J\033[H")
        render_maze(maze.maze, config["ENTRY"], config["EXIT"], wall_color)

        # MENU
        path_render = True
        while True:
            display_menu()
            choice = input(
                f"{YELLOW} ❯ Select an option {DIM}(1-5)"
                f"{RESET}{YELLOW}: {RESET}")
            if choice == '1':
                maze = MazeGenerator(
                    width=config["WIDTH"],
                    height=config["HEIGHT"],
                    entry=config["ENTRY"],
                    exit=config["EXIT"],
                    perfect=config["PERFECT"]
                )
                maze.generate()
                print("\033[2J\033[H")
                render_maze(maze.maze,
                            config["ENTRY"], config["EXIT"], wall_color)
            if choice == '2':
                if path_render:
                    print("\033[2J\033[H")
                    path = maze.solve_maze()
                    render_maze(maze.maze, config["ENTRY"],
                                config["EXIT"], wall_color, path=path)
                else:
                    print("\033[2J\033[H")
                    render_maze(maze.maze,
                                config["ENTRY"], config["EXIT"], wall_color)
                path_render = not path_render
            if choice == '3':
                print(f"{YELLOW}Select wall color:{RESET}")
                print(f"{YELLOW}1. White{RESET}")
                print(f"{YELLOW}2. Orange{RESET}")
                print(f"{YELLOW}3. Pink{RESET}")
                print(f"{YELLOW}4. Brown{RESET}")
                color_choice = input(f"{YELLOW} ❯ {RESET}")
                if color_choice == '1':
                    wall_color = WHITE
                elif color_choice == '2':
                    wall_color = ORANGE
                elif color_choice == '3':
                    wall_color = PINK
                elif color_choice == '4':
                    wall_color = BROWN
                else:
                    pass
                print("\033[2J\033[H")
                render_maze(maze.maze, config["ENTRY"],
                            config["EXIT"], wall_color)

            if choice == '4':
                maze = MazeGenerator(
                    width=config["WIDTH"],
                    height=config["HEIGHT"],
                    entry=config["ENTRY"],
                    exit=config["EXIT"],
                    perfect=config["PERFECT"],
                    seed=seed
                )
                maze.generate(animation=True, wall_color=wall_color)
                print("\033[2J\033[H")
                render_maze(maze.maze, config["ENTRY"],
                            config["EXIT"], wall_color)
            if choice == '5':
                print(f"{YELLOW}Goodbye!{RESET}")
                sys.exit(0)
    except (KeyboardInterrupt, Exception) as e:
        print(f"\033[31mError:\033[0m {e}")
        print("bad trip")
        return


if __name__ == "__main__":
    main()
