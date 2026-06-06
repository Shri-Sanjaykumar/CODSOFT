import sys
import logging
from tabulate import tabulate

from src.config import (
    APP_NAME, VERSION, AUTHOR, INTERNSHIP,
    MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, DEFAULT_PASSWORD_LENGTH,
    COLOR_HEADER, COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR, COLOR_MUTED, COLOR_RESET
)
from src.generator import PasswordGenerator, PasswordGeneratorError, logger
from src.analyzer import PasswordAnalyzer

# Try importing pyperclip safely for clipboard management
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


def print_banner() -> None:
    """Displays the password generator ASCII banner and metadata in a compact box."""
    banner = fr"""
{COLOR_HEADER}┌──────────────────────────────────────────────────┐
│   ____   _     ____  _   _    ____  _____ _   _  │
│  |  _ \ / \   / ___|| | | |  / ___|| ____| \ | | │
│  | |_) / _ \  \___ \| |_| | | |  _ |  _| |  \| | │
│  |  __/ ___ \  ___) |  _  | | |_| || |___| |\  | │
│  |_| /_/   \_\|____/|_| |_|  \____||_____|_| \_| │
│                                                  │
│  {APP_NAME:<48}│
│  Version: {VERSION:<39}│
│  Author: {AUTHOR:<40}│
│  Internship: {INTERNSHIP:<36}│
└──────────────────────────────────────────────────┘{COLOR_RESET}"""
    print(banner)

def print_help() -> None:
    """Displays help information and best practices in a clean, structured frame."""
    print(f"\n{COLOR_HEADER}┌──────────────── GENERATOR MENU ──────────────────┐{COLOR_RESET}")
    print(f"│  [1] Generate Single Password                    │")
    print(f"│  [2] Generate Batch Passwords                    │")
    print(f"│  [A] About Project                               │")
    print(f"│  [H] Help & Security Best Practices              │")
    print(f"│  [V] Version Info                                │")
    print(f"│  [Q] Quit Generator                              │")
    print(f"{COLOR_HEADER}└──────────────────────────────────────────────────┘{COLOR_RESET}")

def print_about() -> None:
    """Displays development notes and metadata."""
    print(f"\n{COLOR_HEADER}--- ABOUT THIS PROJECT ---{COLOR_RESET}")
    print(f"Application:   {APP_NAME}")
    print(f"Version:       {VERSION}")
    print(f"Developer:     {AUTHOR}")
    print(f"Internship:    {INTERNSHIP}")
    print("Organization:  CODSOFT")
    print("\nTechnical details:")
    print(" - Uses the cryptographically secure 'secrets' module instead of 'random'.")
    print(" - Calculates Shannon Information Entropy to rank strength.")
    print(" - Clipboard sync via pyperclip with manual fallback.")
    print(" - Action logs stored securely in logs/application.log.")

def print_version() -> None:
    """Displays version info."""
    print(f"\n{COLOR_SUCCESS}{APP_NAME} - Version {VERSION}{COLOR_RESET}")


class PasswordGeneratorCLI:
    """Main execution loop for the secure password generator CLI."""

    def run(self) -> None:
        """Starts the interactive password configuration shell."""
        logger.info("Application started session.")
        print_banner()
        print_help()

        while True:
            try:
                print(f"\n{COLOR_HEADER}====================================={COLOR_RESET}")
                choice = input(f"{COLOR_HEADER}Select option [1-2, A, H, V, Q]: {COLOR_RESET}").strip().upper()

                if choice == "1":
                    self.generate_single_menu()
                elif choice == "2":
                    self.generate_batch_menu()
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
                    print(f"{COLOR_ERROR}Invalid selection. Press 'H' to view options.{COLOR_RESET}")
            except KeyboardInterrupt:
                print(f"\n\n{COLOR_WARNING}KeyboardInterrupt detected. Shutting down generator...{COLOR_RESET}")
                self.quit_app()
                break
            except Exception as e:
                print(f"{COLOR_ERROR}System Error: {e}{COLOR_RESET}")
                logger.error(f"Global CLI Error: {e}", exc_info=True)

    def get_boolean_input(self, prompt: str) -> bool:
        """Helper to prompt for yes/no confirmation (default: Yes)."""
        val = input(prompt).strip().lower()
        return val != 'n'

    def get_length_input(self) -> int:
        """Prompts for and validates password length bounds."""
        while True:
            len_str = input(f"Enter password length ({MIN_PASSWORD_LENGTH}-{MAX_PASSWORD_LENGTH}) [Default: {DEFAULT_PASSWORD_LENGTH}]: ").strip()
            if not len_str:
                return DEFAULT_PASSWORD_LENGTH
            try:
                length = int(len_str)
                if MIN_PASSWORD_LENGTH <= length <= MAX_PASSWORD_LENGTH:
                    return length
                print(f"{COLOR_ERROR}Validation Error: Length must be between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH}.{COLOR_RESET}")
            except ValueError:
                print(f"{COLOR_ERROR}Validation Error: Length must be a valid integer.{COLOR_RESET}")

    def show_strength_report(self, password: str, u: bool, l: bool, d: bool, s: bool) -> None:
        """Calculates and renders a structured strength metrics table."""
        analysis = PasswordAnalyzer.analyze(password, u, l, d, s)
        
        strength = analysis["strength"]
        entropy = analysis["entropy"]
        
        # Color rating based on classification
        rating_color = COLOR_MUTED
        if strength == "Weak":
            rating_color = COLOR_ERROR
        elif strength == "Medium":
            rating_color = COLOR_WARNING
        elif strength == "Strong":
            rating_color = COLOR_SUCCESS
        else:
            rating_color = COLOR_SUCCESS  # Very Strong
            
        report_data = [
            ["Length", f"{analysis['length']} characters"],
            ["Entropy Rating", f"{entropy} bits"],
            ["Strength Level", f"{rating_color}{strength}{COLOR_RESET}"],
            ["Pool Size", f"{analysis['pool_size']} character types"]
        ]
        print(f"\n{COLOR_HEADER}--- PASSWORD SECURITY METRIC REPORT ---{COLOR_RESET}")
        print(tabulate(report_data, headers=["Security Criterion", "Metric"], tablefmt="fancy_grid"))

    def generate_single_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- CONFIGURE PASSWORD CONSTRAINTS ---{COLOR_RESET}")
        
        length = self.get_length_input()
        use_upper = self.get_boolean_input("Include Uppercase characters (A-Z)? (Y/n): ")
        use_lower = self.get_boolean_input("Include Lowercase characters (a-z)? (Y/n): ")
        use_digits = self.get_boolean_input("Include Numbers (0-9)? (Y/n): ")
        use_symbols = self.get_boolean_input("Include Symbols (!@#$...)? (Y/n): ")

        try:
            password = PasswordGenerator.generate(length, use_upper, use_lower, use_digits, use_symbols)
            print(f"\n{COLOR_SUCCESS}Generated Secure Password:{COLOR_RESET}")
            print(f"{Fore.WHITE + Style.BRIGHT}{password}{COLOR_RESET}\n")
            
            # Show the entropy analysis
            self.show_strength_report(password, use_upper, use_lower, use_digits, use_symbols)
            
            # Offer clipboard copying
            self.clipboard_copy_menu(password)
        except PasswordGeneratorError as e:
            print(f"{COLOR_ERROR}Configuration Error: {e}{COLOR_RESET}")

    def generate_batch_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- BATCH GENERATION ---{COLOR_RESET}")
        while True:
            batch_str = input("How many passwords would you like to generate? (1-10): ").strip()
            try:
                count = int(batch_str)
                if 1 <= count <= 10:
                    break
                print(f"{COLOR_ERROR}Validation Error: Limit is 10 passwords per batch.{COLOR_RESET}")
            except ValueError:
                print(f"{COLOR_ERROR}Validation Error: Please enter a valid number.{COLOR_RESET}")

        length = self.get_length_input()
        use_upper = self.get_boolean_input("Include Uppercase? (Y/n): ")
        use_lower = self.get_boolean_input("Include Lowercase? (Y/n): ")
        use_digits = self.get_boolean_input("Include Numbers? (Y/n): ")
        use_symbols = self.get_boolean_input("Include Symbols? (Y/n): ")

        try:
            print(f"\n{COLOR_SUCCESS}Generated Password List:{COLOR_RESET}")
            passwords = []
            for i in range(count):
                pwd = PasswordGenerator.generate(length, use_upper, use_lower, use_digits, use_symbols)
                passwords.append(pwd)
                print(f"  {i+1}. {Fore.WHITE + Style.BRIGHT}{pwd}{COLOR_RESET}")
            
            # Log batch generation
            logger.info(f"Generated batch of {count} passwords.")
            
            print("\nOptions:")
            print("  [1-10] Enter number of password to copy to clipboard")
            print("  [Press Enter] Skip and return to main menu")
            copy_choice = input("Your choice: ").strip()
            
            if copy_choice:
                try:
                    idx = int(copy_choice) - 1
                    if 0 <= idx < count:
                        self.clipboard_copy_menu(passwords[idx])
                    else:
                        print(f"{COLOR_ERROR}Validation Error: Index out of range.{COLOR_RESET}")
                except ValueError:
                    print(f"{COLOR_ERROR}Validation Error: Invalid number choice.{COLOR_RESET}")
        except PasswordGeneratorError as e:
            print(f"{COLOR_ERROR}Configuration Error: {e}{COLOR_RESET}")

    def clipboard_copy_menu(self, password: str) -> None:
        """Copies password using pyperclip, providing user instructions on failure."""
        copy_confirm = input("\nCopy this password to clipboard? (Y/n): ").strip().lower()
        if copy_confirm == 'n':
            return

        if not CLIPBOARD_AVAILABLE:
            print(f"{COLOR_WARNING}pyperclip is not installed. Please copy the password manually.{COLOR_RESET}")
            return

        try:
            pyperclip.copy(password)
            print(f"{COLOR_SUCCESS}Success: Password copied to clipboard successfully!{COLOR_RESET}")
            logger.info("Password copied to clipboard.")
        except Exception as e:
            print(f"{COLOR_ERROR}Failed to copy to clipboard automatically: {e}{COLOR_RESET}")
            print(f"{COLOR_WARNING}Please copy it manually from the terminal output.{COLOR_RESET}")
            logger.error(f"Clipboard Copy Error: {e}")

    def quit_app(self) -> None:
        print(f"\n{COLOR_SUCCESS}Exiting Password Generator. Stay secure!{COLOR_RESET}")
        logger.info("Application session shutdown successfully.")
        sys.exit(0)
