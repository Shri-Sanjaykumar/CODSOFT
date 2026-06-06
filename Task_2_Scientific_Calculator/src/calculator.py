import math
from typing import Optional

class CalculatorError(ArithmeticError):
    """Base exception class for mathematical errors in the calculator."""
    pass


class Calculator:
    """Core mathematical engine supporting scientific functions and memory registers."""

    def __init__(self) -> None:
        self.memory: float = 0.0
        self.angle_mode: str = "DEGREES"  # Can be "DEGREES" or "RADIANS"

    # Memory Operations
    def memory_store(self, value: float) -> None:
        """Stores the given value in the memory register (overwrites)."""
        self.memory = value

    def memory_add(self, value: float) -> None:
        """Adds the given value to the memory register."""
        self.memory += value

    def memory_subtract(self, value: float) -> None:
        """Subtracts the given value from the memory register."""
        self.memory -= value

    def memory_recall(self) -> float:
        """Returns the current value stored in the memory register."""
        return self.memory

    def memory_clear(self) -> None:
        """Resets the memory register to zero."""
        self.memory = 0.0

    # Angle Mode Management
    def set_angle_mode(self, mode: str) -> None:
        """Sets angle calculations mode to DEGREES or RADIANS."""
        if mode.upper() in ["DEGREES", "RADIANS"]:
            self.angle_mode = mode.upper()

    # Basic Operations
    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise CalculatorError("Division by zero is mathematically undefined.")
        return a / b

    def modulus(self, a: float, b: float) -> float:
        if b == 0:
            raise CalculatorError("Modulus by zero is mathematically undefined.")
        return math.fmod(a, b)

    def power(self, base: float, exponent: float) -> float:
        try:
            # Handle fractional exponents of negative numbers
            return math.pow(base, exponent)
        except ValueError:
            raise CalculatorError("Fractional power of a negative base results in a complex number.")
        except OverflowError:
            raise CalculatorError("Result overflow: Exponent power is too large to compute.")

    # Advanced Scientific Operations
    def square_root(self, value: float) -> float:
        if value < 0:
            raise CalculatorError("Square root of a negative number is undefined in real numbers.")
        return math.sqrt(value)

    def factorial(self, value: float) -> int:
        if value < 0:
            raise CalculatorError("Factorial of a negative number is undefined.")
        if not value.is_integer():
            raise CalculatorError("Factorial is only defined for integer values.")
        
        # Guard against huge numbers causing performance hangs or overflows
        if value > 1000:
            raise CalculatorError("Value too large. Factorial limit is 1000 to prevent overflow.")
        return math.factorial(int(value))

    def percentage(self, value: float, pct: float) -> float:
        """Calculates percent representation (e.g. 50% of 200 = 100)."""
        return (value * pct) / 100.0

    def log_natural(self, value: float) -> float:
        """Calculates natural log (base e)."""
        if value <= 0:
            raise CalculatorError("Logarithm domain error: Input must be greater than zero.")
        return math.log(value)

    def log_base10(self, value: float) -> float:
        """Calculates base-10 log."""
        if value <= 0:
            raise CalculatorError("Logarithm domain error: Input must be greater than zero.")
        return math.log10(value)

    # Trigonometric Operations
    def _to_radians(self, value: float) -> float:
        """Helper to convert input if angle mode is degrees."""
        if self.angle_mode == "DEGREES":
            return math.radians(value)
        return value

    def sin(self, angle: float) -> float:
        rad = self._to_radians(angle)
        # Avoid minor floating point imprecision for exact values (like sin(180) -> 0.0)
        res = math.sin(rad)
        return 0.0 if math.isclose(res, 0.0, abs_tol=1e-15) else res

    def cos(self, angle: float) -> float:
        rad = self._to_radians(angle)
        res = math.cos(rad)
        return 0.0 if math.isclose(res, 0.0, abs_tol=1e-15) else res

    def tan(self, angle: float) -> float:
        rad = self._to_radians(angle)
        # Tan is undefined for 90 degrees (or pi/2 radians)
        cos_val = math.cos(rad)
        if math.isclose(cos_val, 0.0, abs_tol=1e-15):
            raise CalculatorError(f"Tangent is undefined for {angle} {self.angle_mode}.")
        res = math.tan(rad)
        return 0.0 if math.isclose(res, 0.0, abs_tol=1e-15) else res
