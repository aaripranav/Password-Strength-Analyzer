# Password Strength Analyzer 🔐

A comprehensive tool to evaluate password strength and help users create secure passwords. Perfect for learning password security concepts and cryptography basics.

## 📚 Table of Contents
1. [What You'll Learn](#what-youll-learn)
2. [Installation & Setup](#installation--setup)
3. [Features](#features)
4. [How It Works](#how-it-works)
5. [Usage Guide](#usage-guide)
6. [Understanding Password Security](#understanding-password-security)
7. [Architecture](#architecture)

---

## 🎓 What You'll Learn

### Password Security Concepts
- **Entropy**: How randomness makes passwords secure
- **Complexity**: Importance of character variety
- **Dictionary Attacks**: Why common words are dangerous
- **Hashing**: How passwords are securely stored (not reversible)
- **Salting**: Adding randomness to prevent rainbow table attacks

### Technical Skills
- Python fundamentals (functions, loops, regex, file I/O)
- Regular expressions for pattern matching
- Hashing with cryptographic libraries (hashlib)
- SQLite database basics
- Building a command-line interface (CLI)
- Unit testing and validation

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone or Setup the Project
```bash
cd /workspaces/Password-Strength-Analyzer
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python main.py --help
```

---

## ✨ Features

### 1. **Password Strength Analysis**
   - Checks length (minimum 8 characters recommended)
   - Analyzes complexity (uppercase, lowercase, numbers, symbols)
   - Provides strength rating: Weak → Moderate → Strong → Very Strong
   - Detailed feedback for improvements

### 2. **Password Suggestions**
   - Generates random secure passwords
   - Customizable length
   - Optional: enforces specific character types

### 3. **Common Password Detection**
   - Checks against top 1000 common passwords
   - Alerts if password is too similar to common patterns
   - Learns from password history

### 4. **Optional: Database Integration**
   - Store password hashes (never raw passwords!)
   - Prevent reuse of old passwords
   - Track password history
   - Uses SQLite for simplicity

### 5. **Security Best Practices**
   - Never stores raw passwords
   - Uses secure hashing (SHA-256)
   - Implements salting for added security
   - Validates input safely

---

## 🔍 How It Works

### Step-by-Step Flow

```
User enters password
        ↓
[PASSWORD STRENGTH ANALYZER]
        ↓
    ┌───────────────────────────────┐
    │ 1. Check Length (8+ chars)    │
    │ 2. Check Uppercase (A-Z)      │
    │ 3. Check Lowercase (a-z)      │
    │ 4. Check Numbers (0-9)        │
    │ 5. Check Symbols (!@#$, etc)  │
    │ 6. Check Common Words         │
    └───────────────────────────────┘
        ↓
    Calculate Score & Strength
        ↓
    Provide Feedback & Suggestions
        ↓
    Optional: Store in Database
        ↓
    Display Result to User
```

### Scoring System

| Score | Strength    | Security Level |
|-------|-------------|-----------------|
| ≤ 2   | Weak        | 🔴 Low          |
| 3-4   | Moderate    | 🟡 Medium       |
| 5     | Strong      | 🟢 High         |
| 6+    | Very Strong | 💪 Very High    |

---

## 💻 Usage Guide

### 1. **Interactive Mode** (Easiest for beginners)
```bash
python main.py
```

Then follow the interactive prompts:
- Enter a password
- View strength analysis
- Get suggestions
- Test new password

### 2. **Command-Line Mode** (For scripting)
```bash
# Check a password
python main.py check "MyPassword123!"

# Generate a new password
python main.py generate --length 16

# Check with history (requires database)
python main.py check-with-history "MyPassword123!" --username john_doe
```

### 3. **Using as a Library** (Advanced)
```python
from password_analyzer import PasswordAnalyzer

analyzer = PasswordAnalyzer()
strength, feedback = analyzer.analyze("MyPassword123!")
print(f"Strength: {strength}")
print(f"Feedback: {feedback}")
```

---

## 🔐 Understanding Password Security

### Entropy (Randomness)
**What is it?** The measure of unpredictability in a password.

**Formula**: Entropy = log₂(possible_characters ^ password_length)

**Example**:
- "123456" (only numbers) = log₂(10^6) ≈ 20 bits (Weak ❌)
- "MyP@ss123" (mixed) = log₂(94^9) ≈ 60 bits (Strong ✅)

**Why it matters**: Hackers use brute-force attacks trying all combinations. More entropy = exponentially harder to crack.

### Common Attack Methods

| Attack Type | How It Works | Prevention |
|-------------|------------|-----------|
| **Brute Force** | Try every possible combination | Use long passwords (8+ chars) |
| **Dictionary** | Try common words and patterns | Avoid dictionary words |
| **Rainbow Table** | Compare against pre-computed hashes | Use salt + strong hashing |
| **Phishing** | Social engineering to steal passwords | Be vigilant online |

### Hashing vs Encryption
```
PASSWORD SECURITY PYRAMID:
    ┌──────────────┐
    │   Hashing    │  ← ONE-WAY (can't reverse)
    │   (SHA-256)  │     Like shredding: you can't un-shred
    └──────────────┘
         ↓
    ┌──────────────┐
    │ Encryption   │  ← TWO-WAY (can reverse with key)
    │   (AES)      │     Like locking: can unlock with key
    └──────────────┘
```

**Example**:
```
Password: "MyPassword123"
    ↓ (hashing)
Hash: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6" (permanent)

You enter: "MyPassword123"
    ↓ (hash same way)
Hash: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
    ↓ (compare)
Match! ✅ Password correct
```

### Salting
**Problem**: Same password = same hash. Hackers recognize patterns.

**Solution**: Add random data (salt) before hashing.
```
Password: "MyPassword123"
Salt: "r@nd0mStr1ng"
    ↓
Combined: "MyPassword123r@nd0mStr1ng"
    ↓ (hash)
Unique Hash: "xyz789abc123..."

Another user with "MyPassword123" + different salt
    ↓
Different Hash: "qwe456def789..."

Even identical passwords produce different hashes! 🎯
```

---

## 🏗️ Architecture

### File Structure
```
Password-Strength-Analyzer/
├── README.md (this file)
├── requirements.txt (dependencies)
├── main.py (entry point - CLI interface)
├── password_analyzer.py (core logic)
├── database_manager.py (optional - stores password history)
├── common_passwords.txt (list of 1000+ common passwords)
├── tests/
│   ├── test_password_analyzer.py
│   ├── test_database_manager.py
│   └── test_main.py
└── examples/
    ├── example_usage.py (how to use as library)
    └── example_demo.py (demonstration)
```

### Module Breakdown

#### 1. **password_analyzer.py** - Core Logic
```
Main Class: PasswordAnalyzer
├── analyze(password) → (strength, feedback)
├── check_length(password) → score
├── check_complexity(password) → score, details
├── check_common_words(password) → is_common
├── generate_password(length) → secure_password
└── calculate_entropy(password) → bits
```

#### 2. **database_manager.py** - Optional History Tracking
```
Main Class: DatabaseManager
├── init_database() → create tables
├── store_password_hash(username, password_hash)
├── check_password_exists(username, password_hash) → bool
├── get_password_history(username) → list
└── clear_history(username)
```

#### 3. **main.py** - User Interface
```
Functions:
├── interactive_mode() → guide user through analysis
├── command_line_mode(args) → process CLI arguments
├── display_results(strength, feedback) → formatted output
└── main() → entry point
```

---

## 🧪 Testing

Run all tests:
```bash
python -m pytest tests/ -v
```

Run specific test:
```bash
python -m pytest tests/test_password_analyzer.py -v
```

---

## 🎯 Learning Path (Step-by-Step)

### Beginner (Week 1)
- [ ] Understand password strength concepts
- [ ] Read through `password_analyzer.py`
- [ ] Run `python main.py` and test with different passwords
- [ ] Study the scoring system

### Intermediate (Week 2)
- [ ] Learn about regular expressions (regex patterns)
- [ ] Understand hashing and entropy
- [ ] Study the code comments
- [ ] Modify password requirements (e.g., require special chars)

### Advanced (Week 3)
- [ ] Set up database integration
- [ ] Implement password history checking
- [ ] Add machine learning for common pattern detection
- [ ] Build a web interface with Flask/Django

### Expert (Week 4+)
- [ ] Implement bcrypt hashing (more secure)
- [ ] Add two-factor authentication concepts
- [ ] Create API for password validation
- [ ] Deploy to production

---

## 📋 Common Questions (FAQ)

### Q1: Why not just check password == "correct_password"?
**A**: That's storing passwords in plain text - the #1 security mistake! If the database is hacked, all passwords are compromised.

### Q2: Can I recover a password from its hash?
**A**: No! That's the whole point. Hashing is one-way. If you forget the password, you can't recover it - you must reset it.

### Q3: Why do we need length requirements?
**A**: Longer passwords have exponentially more combinations:
- 6 characters: 10^6 = 1,000,000 (cracked in seconds)
- 8 characters: 10^8 = 100,000,000 (cracked in minutes)
- 12 characters: 10^12 = 1 trillion (cracked in days)
- 16 characters: 10^16 = 10 quadrillion (cracked in years)

### Q4: Is "MyPassword123" strong?
**A**: Somewhat. It has:
- ✅ Length (12 chars)
- ✅ Uppercase
- ✅ Lowercase
- ✅ Numbers
- ❌ No special characters
- ❌ Somewhat predictable pattern

Strength: **Strong** (but could be better)

---

## 🔗 Additional Resources

- [OWASP Password Guidelines](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Cryptography Basics](https://www.khanacademy.org/computing/computer-science/cryptography)
- [How Hashing Works](https://www.youtube.com/watch?v=b4b8ketLM1s)
- [Password Entropy Calculator](https://www.omnicalculator.com/other/password-entropy)

---

## 📝 License

This project is for educational purposes. Feel free to use and modify!

---

## 👤 Author

Created as an educational tool for learning password security and Python basics.

**Last Updated**: June 2026

password = input("Enter Password: ")

strength, feedback = check_password_strength(password)

print("\nPassword Strength:", strength)

if feedback:
    print("\nSuggestions:")
    for item in feedback:
        print("-", item)

print("\nSuggested Strong Password:")
print(generate_password())