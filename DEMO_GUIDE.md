# CODSOFT Python Internship - Project Demo & Submission Guide

This guide is designed to help you run through the applications for local testing, record your demonstration video, and prepare your portfolio showcase for GitHub and LinkedIn.

---

## Suggested Demo Order

For the most logical presentation flow, showcase the applications in the following order:
1. **Task 1: Advanced To-Do List Manager** (Shows data management, filtering, and stats).
2. **Task 2: Professional Scientific Calculator** (Shows mathematical precision, exceptions, and history export).
3. **Task 3: Enterprise Password Generator** (Shows security practices, entropy, and clipboard features).

---

## 1. Task 1: Advanced To-Do List Manager

### Key Features to Demonstrate:
1. **Startup Banner:** Launch the app and show the colorful ASCII banner, about info, and version metadata.
2. **Add Tasks:** Create a couple of tasks with different priorities (Low, Medium, High) and due dates (e.g. `YYYY-MM-DD`).
3. **View & Tabular Output:** Display the tasks. Point out the clean table layout constructed using `tabulate`.
4. **Productivity Stats:** Select the statistics option to show the dashboard (total, completed, pending, and completion percentage).
5. **Mark Tasks:** Mark a task as complete and view statistics again to demonstrate the live percentage increase.
6. **Search & Filter:** Search for tasks by title/description or filter by priority.
7. **Graceful Exit:** Quit the application using the menu option or press `Ctrl+C` to show the clean shutdown message.

### Suggested Command:
```bash
python Task_1_Todo_Manager/main.py
```

---

## 2. Task 2: Professional Scientific Calculator

### Key Features to Demonstrate:
1. **Arithmetic & Precision:** Perform a few basic arithmetic operations (e.g. division showing decimal precision).
2. **Scientific Functions:** Run power ($x^y$), square root, and trigonometric calculations (e.g., $sin(90)$ in degrees, showing value `1.0`).
3. **Memory Register:** Save a result using `M+`, recall it with `MR`, and clear it with `MC`.
4. **Robust Exception Handling:** Try dividing by zero or taking the logarithm of a negative number to showcase the user-friendly domain error messages.
5. **History Log:** View the session history and export it to a file. Verify that the file `Task_2_Scientific_Calculator/data/history.txt` is created with all logged operations.

### Suggested Command:
```bash
python Task_2_Scientific_Calculator/main.py
```

---

## 3. Task 3: Enterprise Password Generator

### Key Features to Demonstrate:
1. **Custom Constraints:** Show how users can set character pools (uppercase, lowercase, digits, symbols) and custom length.
2. **Security Entropy Check:** Generate a password and highlight the entropy (bits) and the security ranking (Weak, Medium, Strong, Very Strong).
3. **Clipboard Copying:** Generate a password and choose the copy option. Paste it elsewhere to demonstrate clipboard integration.
4. **Multiple Password Generation:** Generate a batch of 5 passwords at once to show batch-generation support.
5. **Logs Verification:** Exit the app and open `Task_3_Secure_Password_Generator/logs/application.log` to show that all security events are logged.

### Suggested Command:
```bash
python Task_3_Secure_Password_Generator/main.py
```

---

## Recommended Screenshots to Take

For your GitHub readme files and portfolio slides, capture the following:
- **Task 1:** The Task Table containing multiple items and the Productivity Statistics card.
- **Task 2:** A sequence of mathematical operations followed by the exported `history.txt` file content.
- **Task 3:** The entropy analysis report table highlighting a "Very Strong" password rating.

---

## LinkedIn Posting Checklist
- [ ] **Create a Demo Video:** Record a short screen capture (2-3 minutes) demonstrating all 3 tasks.
- [ ] **Draft the Post:** 
  - Briefly introduce the CODSOFT Python internship.
  - Summarize the three projects and the technical choices (OOP, security entropy, robust logging).
  - Mention key technologies used (`colorama`, `tabulate`, `pyperclip`, `secrets`).
- [ ] **Tag and Hashtag:**
  - Tag `@CODSOFT`.
  - Add hashtags: `#codsoft #internship #pythonprogramming #softwareengineering #cleanarchitecture #github #linkedin`
- [ ] **Provide Links:** Include a link to your GitHub repository: `https://github.com/Shri-Sanjaykumar/CODSOFT.git`.

---

## GitHub Showcase Checklist
- [ ] **Verify Repository Structure:** Ensure all task folders, `.gitignore`, and `requirements.txt` are at the root level.
- [ ] **Check Code Layout:** Confirm all imports are relative/absolute, pathlib is used, and type hints are present.
- [ ] **Perform a final Pull & Push:** Check that the origin matches `https://github.com/Shri-Sanjaykumar/CODSOFT.git` and matches local changes.
