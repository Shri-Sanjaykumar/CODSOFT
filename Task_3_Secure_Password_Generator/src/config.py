import sys
from pathlib import Path
from colorama import Fore, Style

# Application Metadata
APP_NAME = "Enterprise Password Generator"
VERSION = "1.0.0"
AUTHOR = "Shri Sanjay Kumar"
INTERNSHIP = "CODSOFT Python Programming Internship"

# Directory & File Paths
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "application.log"

# Create directories if they do not exist
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Theme Colors (Colorama mapped)
COLOR_HEADER = Fore.CYAN + Style.BRIGHT
COLOR_SUCCESS = Fore.GREEN + Style.BRIGHT
COLOR_WARNING = Fore.YELLOW + Style.BRIGHT
COLOR_ERROR = Fore.RED + Style.BRIGHT
COLOR_MUTED = Fore.WHITE + Style.DIM
COLOR_RESET = Style.RESET_ALL

# Password Character Pools
UPPERCASE_CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWERCASE_CHARACTERS = "abcdefghijklmnopqrstuvwxyz"
DIGIT_CHARACTERS = "0123456789"
SYMBOL_CHARACTERS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

# Limits
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
DEFAULT_PASSWORD_LENGTH = 16
