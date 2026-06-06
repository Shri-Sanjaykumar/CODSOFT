# CODSOFT Python Programming Internship Portfolio

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-CLI-orange.svg)]()
[![Internship](https://img.shields.io/badge/internship-CODSOFT-blueviolet.svg)](https://www.codsoft.in)

Welcome to my Python programming internship repository for **CODSOFT** (May-June 2026 cohort). This repository hosts a collection of professional, production-ready command-line applications designed to demonstrate core software engineering principles, clean modular design, and robust exception handling.

---

## Internship Details
- **Intern:** Shri Sanjaykumar V
- **Domain:** Python Programming
- **Batch:** May 2026 Batch B99
- **Duration:** 10 May 2026 - 10 June 2026

---

## Internship Overview

During this internship with **CODSOFT**, I worked on designing and building interactive systems that solve everyday user tasks. Through these projects, I aimed to write code that adheres to standard industrial guidelines, ensuring maintainability, code readability, and scalability.

### Project Objectives
- **Clean Architecture & Separation of Concerns:** Segregate business logic, user interface menus, and database access.
- **Robustness:** Cover all mathematical, user input, and file system edge cases gracefully.
- **User Centric Design:** Create engaging, well-formatted terminal interfaces with intuitive navigation, descriptive headers, and ANSI color codes.
- **Traceability:** Maintain historical records and execution logs using Python's native logging module.

---

## Technologies Used
- **Core Language:** Python 3.11+ (leveraging Dataclasses, Type Hinting, Pathlib, and Secrets)
- **Formatting & Layout:** `tabulate` (for tabular output alignment) and `colorama` (for colorful terminal output)
- **Clipboard Management:** `pyperclip` (for secure cross-platform clipboard copy interactions)
- **Version Control:** Git & GitHub

---

## Skills Demonstrated
1. **Object-Oriented Programming (OOP):** Dataclasses, inheritance, enums, encapsulation.
2. **Defensive Programming:** Active input validation, range checks, custom error definitions, and handling `KeyboardInterrupt` (Ctrl+C).
3. **Data Serialization:** Safe atomic file system writes and JSON/Text persistence.
4. **Information Security:** Understanding and applying cryptographic entropy calculations (Shannon Entropy) for password strength checks.
5. **Config Management:** Centralized configuration (`config.py`) for easy maintenance of settings, colors, and directory paths.

---

## Folder Structure

```
CODSOFT_MAY_INTERN/
├── .gitignore
├── requirements.txt
├── LICENSE
├── README.md                          # Root Portfolio Document
├── DEMO_GUIDE.md                      # Presentation & Testing Checklist
│
├── Task_1_Todo_Manager/               # Command-line Task Planner
│   ├── src/
│   │   ├── config.py                  # Theme colors, file paths, metadata
│   │   ├── models.py                  # Dataclasses & enums
│   │   ├── database.py                # Atomic JSON handling
│   │   ├── manager.py                 # Core planner logic & statistics
│   │   └── cli.py                     # User interactive menus
│   ├── data/
│   │   └── tasks.json                 # Persistent task store
│   ├── logs/
│   │   └── application.log            # Execution logging file
│   ├── screenshots/                   # Demonstration visuals
│   ├── README.md                      # Technical documentation
│   └── main.py                        # Entry point
│
├── Task_2_Scientific_Calculator/      # Advanced Math Utility
│   ├── src/
│   │   ├── config.py                  # Configurations
│   │   ├── calculator.py              # Math engine & memory registers
│   │   ├── history.py                 # History manager (history.txt writer)
│   │   └── cli.py                     # Math prompt loop
│   ├── data/
│   │   └── history.txt                # Calculation logs
│   ├── screenshots/                   # Demonstration visuals
│   ├── README.md                      # Technical documentation
│   └── main.py                        # Entry point
│
└── Task_3_Secure_Password_Generator/  # Security Token Tool
    ├── src/
    │   ├── config.py                  # Configuration & pool constants
    │   ├── generator.py               # Cryptographically secure gen
    │   ├── analyzer.py                # Shannon entropy & rating ranker
    │   └── cli.py                     # User customization interface
    ├── logs/
    │   └── application.log            # System event log
    ├── screenshots/                   # Demonstration visuals
    ├── README.md                      # Technical documentation
    └── main.py                        # Entry point
```

---

## Running the Projects

### Prerequisites
Make sure you have Python 3.11 or later installed. Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Execution Commands
Navigate into the respective task directory and execute the entry point script `main.py`:

```bash
# Run Task 1 (Todo Manager)
python Task_1_Todo_Manager/main.py

# Run Task 2 (Scientific Calculator)
python Task_2_Scientific_Calculator/main.py

# Run Task 3 (Secure Password Generator)
python Task_3_Secure_Password_Generator/main.py
```

---

## Future Scope
- **GUI Extensions:** Introduce web-based (Streamlit/Flet) or graphical (Tkinter/PySide6) dashboards for each utility.
- **Database Migrations:** Move from raw JSON files to SQLite for relational integrity.
- **REST APIs:** Package the calculator and password generator engines as FastAPI microservices.

---

## Author Information

**Shri Sanjay Kumar**  
- **Role:** Python Programming Intern (CODSOFT)  
- **GitHub Repository:** [CODSOFT Repository](https://github.com/Shri-Sanjaykumar/CODSOFT.git)  
- **Date:** May - June 2026  
