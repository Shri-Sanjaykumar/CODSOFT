# Task 2: Professional Scientific Calculator

This is a comprehensive scientific command-line calculator written in Python. It supports basic arithmetic, advanced operations (power, modulus, factorial, logarithms, square root), trigonometric functions, memory storage registers, and calculation session exports.

---

## Technical Architecture

The architecture separating concerns consists of:
```
+-------------------------------------------------------+
|                       main.py                         |
|                 (Application Entry)                   |
+---------------------------+---------------------------+
                            |
                            v
+-------------------------------------------------------+
|                    src/cli.py                         |
|            (User Interface & Input Prompts)           |
+---------------------------+---------------------------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
+-------------------------+   +-------------------------+
|   src/calculator.py     |   |     src/history.py      |
|  (Core Math Functions)  |   | (Calculation log sync)  |
+-------------------------+   +------------+------------+
                                           |
                                           v
                              +-------------------------+
                              |    data/history.txt     |
                              |   (Persistent Log)      |
                              +-------------------------+
```

1. **`calculator.py`:** Holds the core mathematical operations, keeping track of memory registers (`M+`, `M-`, `MR`, `MC`) and validating domains (checking for division by zero or negative factorials).
2. **`history.py`:** Logs calculations in the current session and appends them to `data/history.txt` on export.
3. **`cli.py`:** Displays terminal prompt colors using `colorama`, formats outputs, and catches interrupts.
4. **`config.py`:** Contains default settings, metadata, and relative directory routes.

---

## Supported Operations

### 1. Basic Arithmetic
- **Addition:** `a + b`
- **Subtraction:** `a - b`
- **Multiplication:** `a * b`
- **Division:** `a / b` (guarded against division by zero)

### 2. Powers & Modulus
- **Power:** `x^y`
- **Modulus:** `a % b` (finds division remainder)

### 3. Advanced Scientific
- **Square Root:** `√x` (guarded against negative inputs)
- **Factorial:** `x!` (restricted to integers in the range `[0, 1000]`)
- **Percentage:** `Rate% of Base`
- **Logarithms:** Natural Logarithm (`ln(x)`) and Base-10 Logarithm (`log10(x)`) (guarded against non-positive numbers)

### 4. Trigonometry
- **Trig functions:** `sin(x)`, `cos(x)`, `tan(x)` (supports switching between DEGREES and RADIANS)

### 5. Memory Storage Registers
- **MS:** Store value in memory
- **MR:** Recall value from memory
- **MC:** Clear memory register
- **M+:** Add value to memory
- **M-:** Subtract value from memory

---

## Example Output & File Export
When you run a calculation, it is displayed as:
```text
Result: 5 + 3 = 8
Result: sin(90) = 1.0
```

On export, these calculations are appended to `data/history.txt` in the following format:
```text
[5 + 3 = 8]
[sin(90) = 1.0]
```

---

## Running the Application
To run the calculator:

```bash
python Task_2_Scientific_Calculator/main.py
```
