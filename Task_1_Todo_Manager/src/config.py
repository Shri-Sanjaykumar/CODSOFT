import sys
from pathlib import Path
from colorama import Fore, Style

# Application Metadata
APP_NAME = "Advanced To-Do List Manager"
VERSION = "1.0.0"
AUTHOR = "Shri Sanjay Kumar"
INTERNSHIP = "CODSOFT Python Programming Internship"

# Directory & File Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

DATA_FILE = DATA_DIR / "tasks.json"
LOG_FILE = LOG_DIR / "application.log"

# Create directories if they do not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Theme Colors (Colorama mapped)
COLOR_HEADER = Fore.CYAN + Style.BRIGHT
COLOR_SUCCESS = Fore.GREEN + Style.BRIGHT
COLOR_WARNING = Fore.YELLOW + Style.BRIGHT
COLOR_ERROR = Fore.RED + Style.BRIGHT
COLOR_MUTED = Fore.WHITE + Style.DIM
COLOR_RESET = Style.RESET_ALL

# Task Priority Constants
PRIORITY_LOW = "LOW"
PRIORITY_MEDIUM = "MEDIUM"
PRIORITY_HIGH = "HIGH"

# Task Status Constants
STATUS_PENDING = "PENDING"
STATUS_COMPLETED = "COMPLETED"
