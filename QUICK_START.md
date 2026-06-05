# 🚀 Quick Start Guide - Password Strength Analyzer

Get started in 2 minutes!

## ⚡ Installation (30 seconds)

```bash
cd /workspaces/Password-Strength-Analyzer

# Install dependencies
pip install -r requirements.txt
```

## 🎯 First Test (Interactive Mode - Best for Beginners)

```bash
python main.py
```

You'll see a menu:
```
WHAT WOULD YOU LIKE TO DO?
1. Analyze a password
2. Generate a strong password
3. Learn about password security
4. Exit
```

**Try this:**
1. Choose option 1
2. Enter password: `MyPassword123`
3. See the results!
4. Try option 2 to generate a secure password

## 💻 Command-Line Mode

```bash
# Analyze a password
python main.py check "MyPassword123"

# Generate a password
python main.py generate --length 16

# See demo examples
python main.py demo
```

## 📚 Running Examples

See 8 complete examples:
```bash
python example_usage.py
```

## 🧪 Running Tests

```bash
# Install test dependencies (optional)
pip install pytest pytest-cov

# Run all tests
pytest test_password_analyzer.py -v

# Run specific test
pytest test_password_analyzer.py::TestPasswordAnalyzer::test_password_too_short -v
```

## 📖 Learning Path

1. **Day 1:** Run `python main.py` - Try both interactive modes
2. **Day 2:** Read [BEGINNERS_GUIDE.md](BEGINNERS_GUIDE.md) - Deep dive into concepts
3. **Day 3:** Run `python example_usage.py` - See practical examples
4. **Day 4:** Read [README.md](README.md) - Architecture and advanced topics

## 🔍 Quick Examples

### Example 1: Analyze Password
```python
from password_analyzer import PasswordAnalyzer

analyzer = PasswordAnalyzer()
strength, feedback = analyzer.analyze("MyPassword123!")

print(f"Strength: {strength}")
for item in feedback:
    print(f"  {item}")
```

### Example 2: Generate Password
```python
from password_analyzer import PasswordAnalyzer

analyzer = PasswordAnalyzer()
secure_pwd = analyzer.generate_password(16)
print(f"Generated: {secure_pwd}")
```

### Example 3: Calculate Entropy
```python
from password_analyzer import PasswordAnalyzer

analyzer = PasswordAnalyzer()
entropy = analyzer.calculate_entropy("MyPassword123!")
print(f"Entropy: {entropy} bits")
```

## ❓ Common First Steps

**Q: Which mode should I try first?**
A: Interactive mode! Run `python main.py` (no arguments)

**Q: What if I get an error?**
A: Make sure you:
1. Are in the correct directory: `cd /workspaces/Password-Strength-Analyzer`
2. Have Python 3.8+: `python --version`
3. Installed requirements: `pip install -r requirements.txt`

**Q: What's the difference between check and demo?**
A: 
- `check` - Analyze YOUR password
- `demo` - Show example passwords and their results

**Q: Can I use this in my own code?**
A: Yes! See "Using as a Library" in [BEGINNERS_GUIDE.md](BEGINNERS_GUIDE.md)

## 📚 Next Steps

- Read [BEGINNERS_GUIDE.md](BEGINNERS_GUIDE.md) for detailed explanations
- Check [README.md](README.md) for full documentation
- Run `python example_usage.py` to see all capabilities
- Try modifying the code to add features!

## 🎓 What You'll Learn

- ✅ What makes passwords strong
- ✅ How entropy measures security
- ✅ How hashing protects passwords
- ✅ Python programming fundamentals
- ✅ Cryptography basics
- ✅ Database design

---

**Ready?** Run: `python main.py` 🚀
