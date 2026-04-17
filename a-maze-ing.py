import sys
from config_parser import parse_config, ConfigParseError
from mazegenerator import MazeGenerator


def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python3 a_maze_ing.py config.txt")
            sys.exit(1)

        try:
            config = parse_config(sys.argv[1])
        except (ConfigParseError, OSError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        maze = MazeGenerator(
            width=config["WIDTH"],
            height=config["HEIGHT"],
            entry=config["ENTRY"],
            exit=config["EXIT"],
            perfect=config["PERFECT"]
        )
        maze.generate()
    except (KeyboardInterrupt, OSError, Exception):
        print(" bad trip")
        return


if __name__ == "__main__":
    main()
