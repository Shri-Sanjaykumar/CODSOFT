import json
import logging
import shutil
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class JsonDatabase:
    """Manages secure reading, writing, and backup recovery of JSON task data."""

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load_data(self) -> List[Dict[str, Any]]:
        """Loads data from the JSON file. Reconstructs if corrupted or missing."""
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                logger.warning("JSON database structure was not a list. Resetting database.")
                return []
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.error(f"Database file corrupted or unreadable: {e}. Attempting recovery.")
            self._handle_corruption()
            return []
        except Exception as e:
            logger.error(f"Unexpected error loading database: {e}")
            return []

    def save_data(self, data: List[Dict[str, Any]]) -> bool:
        """Saves data to JSON file atomically by writing to a temporary file first."""
        temp_file = self.file_path.with_suffix(".tmp")
        try:
            # Write to temporary file first
            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            
            # Replace the original file atomically
            if temp_file.exists():
                shutil.move(str(temp_file), str(self.file_path))
            return True
        except Exception as e:
            logger.error(f"Failed to write data atomically: {e}")
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass
            return False

    def _handle_corruption(self) -> None:
        """Backs up corrupted file and creates a new empty file to recover gracefully."""
        backup_path = self.file_path.with_suffix(".corrupted.bak")
        try:
            if self.file_path.exists():
                shutil.move(str(self.file_path), str(backup_path))
                logger.info(f"Corrupted file backed up to {backup_path}")
            # Create a fresh empty database
            self.save_data([])
        except Exception as e:
            logger.critical(f"Failed to recover database during corruption handle: {e}")
