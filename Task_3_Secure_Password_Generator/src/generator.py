import secrets
import logging
from typing import List, Optional

from src.config import (
    LOG_FILE, UPPERCASE_CHARACTERS, LOWERCASE_CHARACTERS, DIGIT_CHARACTERS, SYMBOL_CHARACTERS
)

# Setup Logging in UTF-8
logger = logging.getLogger("Task_3_Secure_Password_Generator")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


class PasswordGeneratorError(ValueError):
    """Custom exception raised for invalid password generation parameters."""
    pass


class PasswordGenerator:
    """Handles generating cryptographically secure passwords using secrets module."""

    @staticmethod
    def generate(length: int, use_upper: bool, use_lower: bool, use_digits: bool, use_symbols: bool) -> str:
        """Generates a secure password satisfying the specified pool requirements."""
        if not (use_upper or use_lower or use_digits or use_symbols):
            raise PasswordGeneratorError("At least one character pool must be selected.")

        pools: List[str] = []
        required_chars: List[str] = []

        if use_upper:
            pools.append(UPPERCASE_CHARACTERS)
            required_chars.append(secrets.choice(UPPERCASE_CHARACTERS))
        if use_lower:
            pools.append(LOWERCASE_CHARACTERS)
            required_chars.append(secrets.choice(LOWERCASE_CHARACTERS))
        if use_digits:
            pools.append(DIGIT_CHARACTERS)
            required_chars.append(secrets.choice(DIGIT_CHARACTERS))
        if use_symbols:
            pools.append(SYMBOL_CHARACTERS)
            required_chars.append(secrets.choice(SYMBOL_CHARACTERS))

        if length < len(required_chars):
            raise PasswordGeneratorError(
                f"Password length ({length}) is too short for selected constraints. "
                f"Must be at least {len(required_chars)}."
            )

        # Merge selected character pools
        full_pool = "".join(pools)
        
        # Fill the remaining length with random characters from the combined pool
        remaining_length = length - len(required_chars)
        random_chars = [secrets.choice(full_pool) for _ in range(remaining_length)]
        
        # Combine required and random characters, then shuffle them securely
        password_list = required_chars + random_chars
        secrets.SystemRandom().shuffle(password_list)
        
        password = "".join(password_list)
        logger.info(f"Password Generated - Length: {length}, Pools: "
                    f"U:{use_upper} L:{use_lower} D:{use_digits} S:{use_symbols}")
        return password
