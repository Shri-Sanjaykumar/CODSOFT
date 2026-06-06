import sys
from pathlib import Path
from colorama import Fore, Style

# Application Metadata
APP_NAME = "Professional Scientific Calculator"
VERSION = "1.0.0"
AUTHOR = "Shri Sanjay Kumar"
INTERNSHIP = "CODSOFT Python Programming Internship"

# Directory & File Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
HISTORY_FILE = DATA_DIR / "history.txt"

# Create data directory if it does not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Theme Colors (Colorama mapped)
COLOR_HEADER = Fore.CYAN + Style.BRIGHT
COLOR_SUCCESS = Fore.GREEN + Style.BRIGHT
COLOR_WARNING = Fore.YELLOW + Style.BRIGHT
COLOR_ERROR = Fore.RED + Style.BRIGHT
COLOR_MUTED = Fore.WHITE + Style.DIM
COLOR_RESET = Style.RESET_ALL

# Calculator Preferences
DEFAULT_PRECISION = 6
ANGLE_MODE_DEGREES = "DEGREES"
ANGLE_MODE_RADIANS = "RADIANS"
