import math
from typing import Dict, Any

class PasswordAnalyzer:
    """Evaluates password security metrics, entropy, and strength classifications."""

    @staticmethod
    def calculate_entropy(length: int, pool_size: int) -> float:
        """Calculates Shannon Information Entropy of the password in bits."""
        if pool_size <= 0 or length <= 0:
            return 0.0
        return length * math.log2(pool_size)

    @staticmethod
    def get_strength_rating(entropy: float) -> str:
        """Categorizes strength according to entropy (bits) thresholds."""
        if entropy < 40:
            return "Weak"
        elif entropy < 60:
            return "Medium"
        elif entropy < 80:
            return "Strong"
        else:
            return "Very Strong"

    @classmethod
    def analyze(cls, password: str, use_upper: bool, use_lower: bool, use_digits: bool, use_symbols: bool) -> Dict[str, Any]:
        """Runs a complete security scan on the password and returns metrics."""
        # Calculate active pool size
        pool_size = 0
        if use_upper:
            pool_size += 26
        if use_lower:
            pool_size += 26
        if use_digits:
            pool_size += 10
        if use_symbols:
            pool_size += 26  # Based on character set length in config

        length = len(password)
        entropy = cls.calculate_entropy(length, pool_size)
        strength = cls.get_strength_rating(entropy)

        return {
            "length": length,
            "pool_size": pool_size,
            "entropy": round(entropy, 2),
            "strength": strength
        }
