import sys
from config_parser import parse_config, ConfigParseError


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
    except (ConfigParseError, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Now use config['WIDTH'], config['HEIGHT'], etc.
    print("Configuration loaded successfully:")
    for k, v in config.items():
        print(f"  {k} = {v}")


if __name__ == "__main__":
    main()
