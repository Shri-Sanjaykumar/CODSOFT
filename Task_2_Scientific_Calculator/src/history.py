import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

class HistoryManager:
    """Manages recording and exporting calculator session history logs."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.session_history: List[str] = []

    def record_entry(self, operation: str, result: str) -> None:
        """Saves a calculation entry to the temporary session history list."""
        entry = f"{operation} = {result}"
        self.session_history.append(entry)
        logger.info(f"Recorded history entry: {entry}")

    def get_session_history(self) -> List[str]:
        """Returns calculations recorded in the current session."""
        return self.session_history

    def clear_session_history(self) -> None:
        """Clears calculations recorded in the current session."""
        self.session_history.clear()

    def export_to_file(self) -> bool:
        """Appends current session history to the persistent file on disk."""
        if not self.session_history:
            return False

        try:
            # Append history entries in UTF-8 format
            with open(self.file_path, "a", encoding="utf-8") as file:
                for entry in self.session_history:
                    file.write(f"[{entry}]\n")
            logger.info(f"Exported {len(self.session_history)} entries to {self.file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export history: {e}")
            return False
