import sys
from pathlib import Path

# Add src folder to module search path so relative imports work
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.cli import CalculatorCLI

if __name__ == "__main__":
    try:
        app = CalculatorCLI()
        app.run()
    except KeyboardInterrupt:
        print("\n\nSession terminated by user (Ctrl+C). Goodbye!")
        sys.exit(0)
