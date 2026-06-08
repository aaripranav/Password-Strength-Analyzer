# 🔴 Weak Password Example

## Input
```
Password: 12345
```

## Output from Password Strength Analyzer
```
🔐 Password: 12345
💪 Strength: Weak
📊 Entropy: 16.61 bits

Feedback:
  ❌ Too short - use at least 8 characters (minimum)
  ❌ Add uppercase letters (A-Z)
  ❌ Add lowercase letters (a-z)
  ✅ Contains numbers
  ❌ Add special characters (!@#$%^&*, etc.)
  🚨 WARNING: This is a common/known password
```

## Analysis

**Why this password is weak:**
- ❌ **Too Short** - Only 5 characters (minimum 8 recommended)
- ❌ **No Uppercase** - Missing A-Z (doubles character set)
- ❌ **No Lowercase** - Missing a-z
- ✅ **Has Numbers** - Good, but not enough
- ❌ **No Symbols** - Missing special characters
- ❌ **Common Password** - Known dictionary word
- 📊 **Entropy: 16.61 bits** - Very low (easy to crack)

**What attackers could do:**
- Crack in seconds using brute force
- Found in common password lists
- Dictionary attack would find it immediately

**To make it stronger:**
- Use at least 8-12 characters
- Add uppercase letters
- Add lowercase letters
- Add special characters (!@#$%)
- Avoid common words

---

*This demonstrates why strong passwords are essential for security.*
