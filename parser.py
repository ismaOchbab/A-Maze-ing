from typing import Dict, Optional
import sys


class ConfigError(Exception):
    "Custom exception for configuration errors"
    pass


class Parsing:
    """Parser class for maze config file"""

    def __init__(self, config_file: str) -> None:
        """Initialize the parser with the config file path"""
        self.config_file: str = config_file
        self.width: int = 0
        self.height: int = 0
        self.entry: Dict[str, int] = {}
        self.exit: Dict[str, int] = {}
        self.output_file: str = ""
        self.perfect: bool = False
        self.seed: Optional[int] = None
        self.extra: Dict[str, str] = {}

    def parse(self) -> None:
        """
        Parses the config file and set the attributes
        Raises COnfigError i f any error occurs
        """
        try:
            with open(self.config_file, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise ConfigError(
                f"File not found: {self.config_file}"
            )
        except PermissionError:
            raise ConfigError(
                f"No permission to read: {self.config_file}"
            )
        
        #first pass: collect raw key-value pairs
        raw_config: Dict[str, str] = {}
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if '=' not in stripped:
                raise ConfigError(
                    f"Line {line_num}: missing '=' separator"
                )
            key, value = stripped.split('=', 1)
            key = key.strip().lower()
            value = value.strip()
            if not key:
                raise ConfigError(
                    f"Line {line_num}: empty line"
                )
            raw_config[key] = value

        #required keys
        required = ['width',
                    'height',
                    'entry',
                    'exit',
                    'output_file',
                    'perfect']
        missing = [r for r in required if r not in raw_config]
        if missing:
            raise ConfigError(
                f"Missing required keys: {', '.join(missing)}"
            )
        
        try:
            self.width = int(raw_config['width'])
            if self.width < 0:
                raise ValueError
        except ValueError:
            raise ConfigError("WIDTH must be positive int")
        
        try:
            self.height = int(raw_config['height'])
            if self.height < 0:
                raise ValueError
        except ValueError:
            raise ConfigError(
                    f"HEIGHT must be positive integer"
                )

        try:
            entry_parts = raw_config['entry'].split(',')
            if len(entry_parts) != 2:
                raise ValueError
            ex, ey = int(entry_parts[0]), int(entry_parts[1])
            if not (0 <= ex < self.width and 0 <= ey < self.height):
                raise ValueError("Out of bounds")
            self.entry = {'x': ex, 'y': ey}
        except ValueError:
            raise ConfigError(
                f"ENTRY must be 'x,y' with integers inside maze bounds"
                f"(0..{self.width - 1}, 0..{self.height - 1})"
            )
        
        try:
            exit_parts = raw_config['exit'].split(',')
            if len(exit_parts) != 2:
                raise ValueError
            xx, xy = int(exit_parts[0]), int(exit_parts[1])
            if not (0 < xx < self.width and 0 < xy < self.height):
                raise ValueError("Out of bounds")
            self.exit = {'x': xx, 'y': xy}
        except ValueError:
            raise ConfigError(
                f"EXIT must be 'x,y' with integers inside maze bounds"
                f"(0..{self.width - 1}, 0..{self.height - 1})"
            )
        
        if self.entry == self.exit:
            raise ConfigError("ENTRY and EXIT must be different")
        
        self.output_file = raw_config['output_file']

        perfect_flag = raw_config['perfect'].lower()
        if perfect_flag in ('true', '1', 'yes'):
            self.perfect = True
        elif perfect_flag in ('false', '0', 'no'):
            self.perfect = False
        else:
            raise ConfigError("PERFECT must be True or False")

        if 'seed' in raw_config:
            try:
                self.seed = int(raw_config['seed'])
            except ValueError:
                raise ConfigError("SEED must be an integer")
            
        #extra keys
        standard_keys = {'width', 'height', 'entry', 'exit',
                         'output_file', 'perfect', 'seed'}
        self.extra = {k: v for k, v in raw_config.items()
                      if k not in standard_keys}


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    parser = Parsing(sys.argv[1])
    try:
        parser.parse()
    except ConfigError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    print("Configuration loaded successfully")
    print(f"Size: {parser.width}x{parser.height}")
    print(f"Entry: {parser.entry}, Exit: {parser.exit}")
    print(f"Perfect: {parser.perfect}")
    print(f"Output file: {parser.output_file}")
    if parser.seed is not None:
        print(f"Seed: {parser.seed}")
    if parser.extra:
        print(f"Extra: {parser.extra}")

if __name__ == '__main__':
    config = Parsing("config.txt")
    config.parse()
    print(config.entry)