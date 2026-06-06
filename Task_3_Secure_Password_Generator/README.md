# Task 3: Enterprise Secure Password Generator

This is a command-line security token utility designed to generate cryptographically secure passwords. It incorporates complexity constraints, Shannon Information Entropy rating calculations, and clipboard copy functions.

---

## Technical Design Notes

### 1. Cryptographically Secure Pseudo-Random Number Generator (CSPRNG)
Unlike standard implementations using Python's default `random` module (which utilizes a predictable Mersenne Twister algorithm), this application uses the **`secrets`** module. This relies on operating system-level sources of entropy (such as Windows CNG or Linux `/dev/urandom`), rendering generated passwords cryptographically secure and suitable for production-level accounts.

### 2. Shannon Entropy Rating
Information entropy (measured in bits) measures password unpredictability. It is calculated as:
$$H = L \log_2(R)$$
Where:
- $L$ is the character length of the generated password.
- $R$ is the size of the selected character pool (uppercase: 26, lowercase: 26, digits: 10, symbols: 26).

We classify strength based on standard entropy thresholds:
- **Weak:** $H < 40$ bits (easily brute-forced)
- **Medium:** $40 \le H < 60$ bits (moderately secure)
- **Strong:** $60 \le H < 80$ bits (highly secure)
- **Very Strong:** $H \ge 80$ bits (nearly impossible to crack with current computing capabilities)

---

## Features
- **Strict Custom Constraints:** Toggle uppercase, lowercase, numbers, and symbols. Guaranteed pool representation (e.g. if numbers are toggled, at least one number will be included).
- **Batch Generation:** Generate lists of up to 10 passwords at a time.
- **Auto Clipboard Copy:** Integrates with `pyperclip` to copy passwords straight to the clipboard (with safe console fallback instructions if system clipboard drivers are missing).
- **Log Audit:** Logs all generation metrics, pool counts, and execution events to `logs/application.log` in UTF-8 format.
- **Graceful Shutdowns:** Handles KeyboardInterrupts cleanly without printing stack trace dumps.

---

## Security Best Practices Included
- Never use words from standard dictionaries.
- Always use passwords exceeding 12 characters.
- Ensure unique passwords for each service.
- Maintain logs locally and never upload raw generated secrets to remote monitoring services.

---

## Running the Application
To run the generator:

```bash
python Task_3_Secure_Password_Generator/main.py
```
