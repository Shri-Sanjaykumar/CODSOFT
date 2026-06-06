import sys
from typing import Optional
from src.config import (
    APP_NAME, VERSION, AUTHOR, INTERNSHIP,
    HISTORY_FILE, COLOR_HEADER, COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR, COLOR_MUTED, COLOR_RESET
)
from src.calculator import Calculator, CalculatorError
from src.history import HistoryManager

def print_banner() -> None:
    """Displays the calculator ASCII startup banner and metadata in a compact box."""
    banner = fr"""
{COLOR_HEADER}┌──────────────────────────────────────────────────┐
│   ____   ____ ___    ____   _    _     ____      │
│  / ___| / ___|_ _|  / ___| / \  | |   / ___|     │
│  \___ \| |    | |  | |    / _ \ | |  | |         │
│   ___) | |___ | |  | |___/ ___ \| |__| |___      │
│  |____/ \____|___|  \____/_/   \_\_____\____|    │
│                                                  │
│  {APP_NAME:<48}│
│  Version: {VERSION:<39}│
│  Author: {AUTHOR:<40}│
│  Internship: {INTERNSHIP:<36}│
└──────────────────────────────────────────────────┘{COLOR_RESET}"""
    print(banner)

def print_help() -> None:
    """Displays the menu options description in a compact grid."""
    print(f"\n{COLOR_HEADER}┌─────────────── CALCULATOR MENU ──────────────────┐{COLOR_RESET}")
    print(f"│  [1] Basic Arithmetic    [5] Trigonometry        │")
    print(f"│  [2] Modulus & Powers    [6] Angle Mode Toggle   │")
    print(f"│  [3] Advanced Functions  [7] Memory Register     │")
    print(f"│  [4] Logarithms          [8] Session History     │")
    print(f"│  [A] About Project       [H] Help & Usage        │")
    print(f"│  [V] Version Info        [Q] Quit Calculator     │")
    print(f"{COLOR_HEADER}└──────────────────────────────────────────────────┘{COLOR_RESET}")

def print_about() -> None:
    """Displays metadata and architecture notes."""
    print(f"\n{COLOR_HEADER}--- ABOUT THIS PROJECT ---{COLOR_RESET}")
    print(f"Application:   {APP_NAME}")
    print(f"Version:       {VERSION}")
    print(f"Developer:     {AUTHOR}")
    print(f"Internship:    {INTERNSHIP}")
    print("Organization:  CODSOFT")
    print("\nTechnical Features:")
    print(" - Modular object-oriented architecture.")
    print(" - Precision decimal float parsing with extensive domain checks.")
    print(" - Integrated Session History logs that export to file.")
    print(" - Handles Ctrl+C (KeyboardInterrupt) gracefully to avoid crashes.")

def print_version() -> None:
    """Displays version information."""
    print(f"\n{COLOR_SUCCESS}{APP_NAME} - Version {VERSION}{COLOR_RESET}")


class CalculatorCLI:
    """Main terminal loop runner for the Scientific Calculator application."""

    def __init__(self) -> None:
        self.calc = Calculator()
        self.history = HistoryManager(HISTORY_FILE)

    def run(self) -> None:
        """Starts the interactive math console loop."""
        print_banner()
        print_help()

        while True:
            try:
                print(f"\n{COLOR_HEADER}====================================={COLOR_RESET}")
                # Print status bar
                print(f"{COLOR_MUTED}[Mode: {self.calc.angle_mode}] [Memory: {self.calc.memory_recall():.4f}]{COLOR_RESET}")
                
                choice = input(f"{COLOR_HEADER}Select option [1-8, A, H, V, Q]: {COLOR_RESET}").strip().upper()
                
                if choice == "1":
                    self.basic_arithmetic_menu()
                elif choice == "2":
                    self.mod_power_menu()
                elif choice == "3":
                    self.advanced_menu()
                elif choice == "4":
                    self.logarithm_menu()
                elif choice == "5":
                    self.trig_menu()
                elif choice == "6":
                    self.toggle_angle_mode()
                elif choice == "7":
                    self.memory_menu()
                elif choice == "8":
                    self.history_menu()
                elif choice == "A":
                    print_about()
                elif choice == "H":
                    print_help()
                elif choice == "V":
                    print_version()
                elif choice == "Q":
                    self.quit_app()
                    break
                else:
                    print(f"{COLOR_ERROR}Invalid selection. Press 'H' to view help.{COLOR_RESET}")
            except KeyboardInterrupt:
                print(f"\n\n{COLOR_WARNING}KeyboardInterrupt detected. Shutting down calculator...{COLOR_RESET}")
                self.quit_app()
                break
            except Exception as e:
                print(f"{COLOR_ERROR}System Error: {e}{COLOR_RESET}")

    def get_float_input(self, prompt: str) -> float:
        """Prompts user for float input and validates it."""
        while True:
            val_str = input(prompt).strip()
            if not val_str:
                print(f"{COLOR_ERROR}Validation Error: Input cannot be empty.{COLOR_RESET}")
                continue
            try:
                return float(val_str)
            except ValueError:
                print(f"{COLOR_ERROR}Validation Error: Input must be a valid number.{COLOR_RESET}")

    def basic_arithmetic_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- BASIC ARITHMETIC ---{COLOR_RESET}")
        print("  [+] Addition")
        print("  [-] Subtraction")
        print("  [*] Multiplication")
        print("  [/] Division")
        op = input("Enter operator (+, -, *, /): ").strip()
        if op not in ["+", "-", "*", "/"]:
            print(f"{COLOR_ERROR}Validation Error: Invalid operator.{COLOR_RESET}")
            return

        a = self.get_float_input("Enter first number: ")
        b = self.get_float_input("Enter second number: ")

        try:
            if op == "+":
                res = self.calc.add(a, b)
            elif op == "-":
                res = self.calc.subtract(a, b)
            elif op == "*":
                res = self.calc.multiply(a, b)
            else:
                res = self.calc.divide(a, b)
            
            res_str = f"{res:.6f}".rstrip('0').rstrip('.')
            print(f"\n{COLOR_SUCCESS}Result: {a} {op} {b} = {res_str}{COLOR_RESET}")
            self.history.record_entry(f"{a} {op} {b}", res_str)
        except CalculatorError as e:
            print(f"{COLOR_ERROR}Math Error: {e}{COLOR_RESET}")

    def mod_power_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- MODULUS & POWERS ---{COLOR_RESET}")
        print("  [%] Modulus (Remainder)")
        print("  [^] Power (x^y)")
        op = input("Enter operator (%, ^): ").strip()
        if op not in ["%", "^"]:
            print(f"{COLOR_ERROR}Validation Error: Invalid operator.{COLOR_RESET}")
            return

        a = self.get_float_input("Enter base/first number: ")
        b = self.get_float_input("Enter exponent/second number: ")

        try:
            if op == "%":
                res = self.calc.modulus(a, b)
                op_char = "%"
            else:
                res = self.calc.power(a, b)
                op_char = "^"
            
            res_str = f"{res:.6f}".rstrip('0').rstrip('.')
            print(f"\n{COLOR_SUCCESS}Result: {a} {op_char} {b} = {res_str}{COLOR_RESET}")
            self.history.record_entry(f"{a} {op_char} {b}", res_str)
        except CalculatorError as e:
            print(f"{COLOR_ERROR}Math Error: {e}{COLOR_RESET}")

    def advanced_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- ADVANCED SCIENTIFIC FUNCTIONS ---{COLOR_RESET}")
        print("  [1] Square Root (√x)")
        print("  [2] Factorial (x!)")
        print("  [3] Percentage Calculation")
        opt = input("Select sub-option (1-3): ").strip()
        
        if opt == "1":
            x = self.get_float_input("Enter number: ")
            try:
                res = self.calc.square_root(x)
                res_str = f"{res:.6f}".rstrip('0').rstrip('.')
                print(f"\n{COLOR_SUCCESS}Result: √{x} = {res_str}{COLOR_RESET}")
                self.history.record_entry(f"√{x}", res_str)
            except CalculatorError as e:
                print(f"{COLOR_ERROR}Math Error: {e}{COLOR_RESET}")
        elif opt == "2":
            x = self.get_float_input("Enter integer: ")
            try:
                res = self.calc.factorial(x)
                print(f"\n{COLOR_SUCCESS}Result: {int(x)}! = {res}{COLOR_RESET}")
                self.history.record_entry(f"{int(x)}!", str(res))
            except CalculatorError as e:
                print(f"{COLOR_ERROR}Math Error: {e}{COLOR_RESET}")
        elif opt == "3":
            val = self.get_float_input("Enter base value: ")
            pct = self.get_float_input("Enter percentage rate (%): ")
            res = self.calc.percentage(val, pct)
            res_str = f"{res:.6f}".rstrip('0').rstrip('.')
            print(f"\n{COLOR_SUCCESS}Result: {pct}% of {val} = {res_str}{COLOR_RESET}")
            self.history.record_entry(f"{pct}% of {val}", res_str)
        else:
            print(f"{COLOR_ERROR}Validation Error: Invalid selection.{COLOR_RESET}")

    def logarithm_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- LOGARITHMS ---{COLOR_RESET}")
        print("  [1] Natural Logarithm (ln x)")
        print("  [2] Base-10 Logarithm (log10 x)")
        opt = input("Select log sub-option (1-2): ").strip()
        
        if opt not in ["1", "2"]:
            print(f"{COLOR_ERROR}Validation Error: Invalid selection.{COLOR_RESET}")
            return
            
        x = self.get_float_input("Enter number: ")
        try:
            if opt == "1":
                res = self.calc.log_natural(x)
                label = f"ln({x})"
            else:
                res = self.calc.log_base10(x)
                label = f"log10({x})"
                
            res_str = f"{res:.6f}".rstrip('0').rstrip('.')
            print(f"\n{COLOR_SUCCESS}Result: {label} = {res_str}{COLOR_RESET}")
            self.history.record_entry(label, res_str)
        except CalculatorError as e:
            print(f"{COLOR_ERROR}Math Error: {e}{COLOR_RESET}")

    def trig_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- TRIGONOMETRY ---{COLOR_RESET}")
        print("  [1] Sine (sin)")
        print("  [2] Cosine (cos)")
        print("  [3] Tangent (tan)")
        opt = input("Select trig sub-option (1-3): ").strip()
        
        if opt not in ["1", "2", "3"]:
            print(f"{COLOR_ERROR}Validation Error: Invalid selection.{COLOR_RESET}")
            return
            
        angle = self.get_float_input(f"Enter angle value in {self.calc.angle_mode}: ")
        try:
            if opt == "1":
                res = self.calc.sin(angle)
                label = f"sin({angle})"
            elif opt == "2":
                res = self.calc.cos(angle)
                label = f"cos({angle})"
            else:
                res = self.calc.tan(angle)
                label = f"tan({angle})"
                
            res_str = f"{res:.6f}".rstrip('0').rstrip('.')
            print(f"\n{COLOR_SUCCESS}Result: {label} = {res_str}{COLOR_RESET}")
            self.history.record_entry(label, res_str)
        except CalculatorError as e:
            print(f"{COLOR_ERROR}Math Error: {e}{COLOR_RESET}")

    def toggle_angle_mode(self) -> None:
        new_mode = "DEGREES" if self.calc.angle_mode == "RADIANS" else "RADIANS"
        self.calc.set_angle_mode(new_mode)
        print(f"{COLOR_SUCCESS}Success: Angle mode changed to {new_mode}.{COLOR_RESET}")

    def memory_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- MEMORY REGISTER FUNCTIONS ---{COLOR_RESET}")
        print("  [MS] Store (Save current display)")
        print("  [MR] Recall (Get memory register)")
        print("  [MC] Clear (Reset memory to 0)")
        print("  [M+] Add (Add input to memory)")
        print("  [M-] Subtract (Subtract input from memory)")
        opt = input("Select operation (MS, MR, MC, M+, M-): ").strip().upper()
        
        if opt == "MS":
            val = self.get_float_input("Enter value to store: ")
            self.calc.memory_store(val)
            print(f"{COLOR_SUCCESS}Stored: {val}{COLOR_RESET}")
        elif opt == "MR":
            print(f"{COLOR_SUCCESS}Recall value: {self.calc.memory_recall()}{COLOR_RESET}")
        elif opt == "MC":
            self.calc.memory_clear()
            print(f"{COLOR_SUCCESS}Memory register cleared.{COLOR_RESET}")
        elif opt == "M+":
            val = self.get_float_input("Enter value to add to memory: ")
            self.calc.memory_add(val)
            print(f"{COLOR_SUCCESS}Success: Added to memory.{COLOR_RESET}")
        elif opt == "M-":
            val = self.get_float_input("Enter value to subtract from memory: ")
            self.calc.memory_subtract(val)
            print(f"{COLOR_SUCCESS}Success: Subtracted from memory.{COLOR_RESET}")
        else:
            print(f"{COLOR_ERROR}Validation Error: Invalid memory command.{COLOR_RESET}")

    def history_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- SESSION HISTORY ---{COLOR_RESET}")
        hist_list = self.history.get_session_history()
        
        if not hist_list:
            print(f"{COLOR_WARNING}No history entries recorded in this session.{COLOR_RESET}")
        else:
            for idx, entry in enumerate(hist_list, 1):
                print(f"  {idx}. {entry}")
                
        print("\nOptions:")
        print("  [1] Export session history to file")
        print("  [2] Clear current session lists")
        sub_opt = input("Enter option (or press Enter to return): ").strip()
        
        if sub_opt == "1":
            if self.history.export_to_file():
                print(f"{COLOR_SUCCESS}Success: History appended to {HISTORY_FILE}{COLOR_RESET}")
            else:
                print(f"{COLOR_WARNING}No new history entries to export.{COLOR_RESET}")
        elif sub_opt == "2":
            self.history.clear_session_history()
            print(f"{COLOR_SUCCESS}Session history cleared.{COLOR_RESET}")

    def quit_app(self) -> None:
        """Saves current state and exits."""
        # Auto export history if user wishes
        hist_list = self.history.get_session_history()
        if hist_list:
            confirm = input(f"{COLOR_WARNING}Would you like to export session history before exiting? (Y/n): {COLOR_RESET}").strip().lower()
            if confirm != 'n':
                self.history.export_to_file()
                print(f"{COLOR_SUCCESS}History exported.{COLOR_RESET}")
                
        print(f"\n{COLOR_SUCCESS}Exiting Scientific Calculator. Goodbye!{COLOR_RESET}")
        sys.exit(0)
