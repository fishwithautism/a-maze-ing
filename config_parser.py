"""
Config parser for the maze generator (a_maze_ing.py).

Reads a configuration file in the format:
    KEY = VALUE

Lines starting with '#'(comments) are ignored. Empty lines are ignored.
Keys are case insensitive but stored as uppercase.
Mandatory keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT.
"""

from pathlib import Path
from typing import Dict, Any, Union


class ConfigParseError(Exception):
    """Custom exception for configuration parsing errors."""
    pass


def parse_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Parse the maze configuration file.

    Args:
        config_path: Path to the configuration file.

    Returns:
        Dictionary with keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT,
        plus any additional keys present in the file.

    Raises:
        ConfigParseError: If the file is missing, malformed, contains invalid
        values, or misses mandatory keys.
        OSError: If the file cannot be read (permissions, etc.).
    """
    path = Path(config_path)
    if not path.exists():
        raise ConfigParseError(f"Configuration file not found: {config_path}")
    if not path.is_file():
        raise ConfigParseError(f"Not a regular file: {config_path}")

    # Store parsed values (keys in uppercase)
    config: Dict[str, Any] = {}
    mandatory_keys = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}

    with open(path, "r", encoding="utf-8") as f:
        for line_num, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Check for KEY=VALUE format
            if "=" not in line:
                raise ConfigParseError(
                    f"Line {line_num}: missing '=' separator -> '{
                        raw_line.rstrip()}'"
                )

            # Split on first '=' only (values may contain '=')
            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()

            # Validate and convert values based on key type
            if key == "WIDTH":
                try:
                    width = int(value)
                except ValueError:
                    raise ConfigParseError(
                        f"Line {line_num}: WIDTH"
                        f" must be an integer, got '{value}'"
                    )
                if width <= 0:
                    raise ConfigParseError(
                        f"Line {line_num}: WIDTH must be positive, got {width}"
                    )
                config[key] = width

            elif key == "HEIGHT":
                try:
                    height = int(value)
                except ValueError:
                    raise ConfigParseError(
                        f"Line {line_num}: HEIGHT must be an "
                        f"integer, got '{value}'"
                    )
                if height <= 0:
                    raise ConfigParseError(
                        f"Line {line_num}: HEIGHT must be "
                        f"positive, got {height}"
                    )
                config[key] = height

            elif key == "ENTRY" or key == "EXIT":
                # Expected format: "x,y" (e.g., "0,0")
                parts = value.split(",")
                if len(parts) != 2:
                    raise ConfigParseError(
                        f"Line {line_num}: {key} must be 'x,y' "
                        f"(two integers), got '{value}'"
                    )
                try:
                    x = int(parts[0].strip())
                    y = int(parts[1].strip())
                except ValueError:
                    raise ConfigParseError(
                        f"Line {line_num}: {key} coordinates must be "
                        f"integers, got '{value}'"
                    )
                config[key] = (x, y)

            elif key == "PERFECT":
                # Accept true/false, True/False, 1/0, yes/no (case‑insensitive)
                normalized = value.lower()
                if normalized in ("true", "1", "yes"):
                    config[key] = True
                elif normalized in ("false", "0", "no"):
                    config[key] = False
                else:
                    raise ConfigParseError(
                        f"Line {line_num}: PERFECT must be a boolean "
                        f"(True/False), got '{value}'"
                    )

            elif key == "OUTPUT_FILE":
                # Simple string, but must not be empty
                if not value:
                    raise ConfigParseError(
                        f"Line {line_num}: OUTPUT_FILE cannot be empty"
                    )
                config[key] = value

            else:
                # Any additional key (e.g., SEED) is stored as it is
                config[key] = value

    # After reading all lines, ensure all mandatory keys are present
    missing = mandatory_keys - set(config.keys())
    if missing:
        raise ConfigParseError(
            f"Missing mandatory configuration key(s): {', '.join(missing)}")

    # Optional: basic sanity checks for ENTRY/EXIT range (WIDTH/HEIGHT known)
    width = config["WIDTH"]
    height = config["HEIGHT"]
    for coord_name in ("ENTRY", "EXIT"):
        x, y = config[coord_name]
        if not (0 <= x < width):
            raise ConfigParseError(
                f"{coord_name} x coordinate {x} out of range (0..{width-1})"
            )
        if not (0 <= y < height):
            raise ConfigParseError(
                f"{coord_name} y coordinate {y} out of range (0..{height-1})"
            )
    if config["ENTRY"] == config["EXIT"]:
        raise ConfigParseError("ENTRY and EXIT must be different cells")

    return config
