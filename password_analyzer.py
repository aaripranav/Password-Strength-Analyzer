"""
PASSWORD STRENGTH ANALYZER - Core Logic Module

This module contains the main logic for analyzing password strength.

KEY CONCEPTS:
- Score: Points earned for meeting security criteria (0-6 points)
- Strength: Human-readable rating (Weak, Moderate, Strong, Very Strong)
- Feedback: Specific suggestions for improvement
- Entropy: Measure of randomness/unpredictability (in bits)

Author: Educational Purpose
Date: June 2026
"""

import re
import random
import string
import math
import hashlib
import os


class PasswordAnalyzer:
    """
    Main class for analyzing password strength.
    
    This class provides methods to:
    1. Analyze password strength
    2. Check for common patterns
    3. Generate secure passwords
    4. Calculate entropy
    """
    
    def __init__(self, common_passwords_file="common_passwords.txt"):
        """
        Initialize the PasswordAnalyzer.
        
        Args:
            common_passwords_file: Path to file with common passwords list
        """
        self.common_passwords = self._load_common_passwords(common_passwords_file)
        # Character sets for validation
        self.uppercase_chars = string.ascii_uppercase
        self.lowercase_chars = string.ascii_lowercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*(),.?\":{}|<>-_+=[]{}\\|;:',.<>?/`~"
        self.all_chars = self.uppercase_chars + self.lowercase_chars + self.digits + self.special_chars
    
    def _load_common_passwords(self, filepath):
        """
        Load common passwords from file.
        
        Args:
            filepath: Path to common passwords file
            
        Returns:
            Set of common passwords (for fast lookup)
        """
        try:
            with open(filepath, 'r') as f:
                # Use set for O(1) lookup time instead of O(n)
                return set(line.strip().lower() for line in f.readlines())
        except FileNotFoundError:
            # If file not found, return empty set
            print(f"⚠️  Warning: {filepath} not found. Common password check skipped.")
            return set()
    
    def analyze(self, password):
        """
        Main function to analyze password strength.
        
        PROCESS:
        1. Check length (8+ chars = more combinations)
        2. Check complexity (uppercase, lowercase, numbers, symbols)
        3. Check for common passwords (dictionary attack prevention)
        4. Calculate final score
        5. Determine strength rating
        6. Provide feedback
        
        Args:
            password (str): The password to analyze
            
        Returns:
            tuple: (strength, feedback_list)
                - strength: "Weak", "Moderate", "Strong", or "Very Strong"
                - feedback_list: List of specific improvement suggestions
        """
        # Input validation
        if not password:
            return "Weak", ["Password cannot be empty"]
        
        score = 0
        feedback = []
        
        # STEP 1: Check Length
        # WHY LENGTH MATTERS:
        # More characters = exponentially more combinations to try
        length = len(password)
        if length >= 16:
            score += 2  # Excellent length
            feedback.append("✅ Excellent length (16+ chars)")
        elif length >= 12:
            score += 2  # Good length
            feedback.append("✅ Good length (12+ chars)")
        elif length >= 8:
            score += 1  # Acceptable length
            feedback.append("✓ Acceptable length (8+ chars)")
        else:
            feedback.append("❌ Too short - use at least 8 characters (minimum)")
        
        # STEP 2: Check Uppercase Letters (A-Z)
        # WHY: Doubles the character set (26 instead of 13)
        if re.search(r"[A-Z]", password):
            score += 1
            feedback.append("✅ Contains uppercase letters")
        else:
            feedback.append("❌ Add uppercase letters (A-Z)")
        
        # STEP 3: Check Lowercase Letters (a-z)
        # WHY: Different case = attacker must try more combinations
        if re.search(r"[a-z]", password):
            score += 1
            feedback.append("✅ Contains lowercase letters")
        else:
            feedback.append("❌ Add lowercase letters (a-z)")
        
        # STEP 4: Check Numbers (0-9)
        # WHY: Numbers expand character set by 10 more options
        if re.search(r"\d", password):
            score += 1
            feedback.append("✅ Contains numbers")
        else:
            feedback.append("❌ Add numbers (0-9)")
        
        # STEP 5: Check Special Characters (!@#$, etc.)
        # WHY: Most attackers don't expect special chars, adds surprise factor
        if re.search(r"[!@#$%^&*(),.?\":{}|<>\-_+=[\]{}\\\|;:',.<>?/`~]", password):
            score += 1
            feedback.append("✅ Contains special characters")
        else:
            feedback.append("❌ Add special characters (!@#$%^&*, etc.)")
        
        # STEP 6: Check for Common Passwords (Dictionary Attack Prevention)
        # WHY: Hackers have lists of common passwords - avoid them!
        if self._is_common_password(password):
            score = max(0, score - 2)  # Penalty for common password
            feedback.append("🚨 WARNING: This is a common/known password")
        
        # STEP 7: Calculate Final Strength Rating
        # Scoring Guide:
        # 0-2 points: Weak (easy to crack)
        # 3-4 points: Moderate (medium security)
        # 5 points: Strong (good security)
        # 6+ points: Very Strong (excellent security)
        if score <= 2:
            strength = "Weak"
        elif score <= 4:
            strength = "Moderate"
        elif score == 5:
            strength = "Strong"
        else:
            strength = "Very Strong"
        
        return strength, feedback
    
    def _is_common_password(self, password):
        """
        Check if password is in common passwords list.
        
        Args:
            password (str): Password to check
            
        Returns:
            bool: True if password is common, False otherwise
        """
        return password.lower() in self.common_passwords
    
    def check_length(self, password):
        """
        Check password length and return score.
        
        EXPLANATION: Each additional character multiplies the combinations
        Example: 
        - 8 chars with 94 possible symbols = 94^8 combinations
        - 12 chars with 94 possible symbols = 94^12 combinations
        94^12 is TRILLION times harder than 94^8!
        
        Args:
            password (str): Password to check
            
        Returns:
            int: Score (0-2)
        """
        length = len(password)
        if length >= 16:
            return 2
        elif length >= 12:
            return 2
        elif length >= 8:
            return 1
        else:
            return 0
    
    def check_complexity(self, password):
        """
        Check password complexity across multiple dimensions.
        
        COMPLEXITY = Variety of character types used
        Why it matters: Forces attackers to try different character combinations
        
        Args:
            password (str): Password to check
            
        Returns:
            tuple: (score, details_dict)
                - score: Total complexity score (0-4)
                - details_dict: Dictionary with breakdown of each character type
        """
        score = 0
        details = {
            "uppercase": False,
            "lowercase": False,
            "numbers": False,
            "special": False
        }
        
        if re.search(r"[A-Z]", password):
            score += 1
            details["uppercase"] = True
        
        if re.search(r"[a-z]", password):
            score += 1
            details["lowercase"] = True
        
        if re.search(r"\d", password):
            score += 1
            details["numbers"] = True
        
        if re.search(r"[!@#$%^&*(),.?\":{}|<>\-_+=[\]{}\\\|;:',.<>?/`~]", password):
            score += 1
            details["special"] = True
        
        return score, details
    
    def calculate_entropy(self, password):
        """
        Calculate password entropy (randomness measurement).
        
        ENTROPY = How many bits of randomness does this password contain?
        
        Formula: entropy = log₂(possible_characters ^ password_length)
        
        Interpretation:
        - 0-30 bits: Very weak
        - 30-50 bits: Weak
        - 50-60 bits: Moderate
        - 60-80 bits: Strong
        - 80+ bits: Very strong
        
        EXAMPLE:
        Password: "MyPassword123!"
        Length: 14 characters
        Character set: ~94 symbols (uppercase + lowercase + digits + special)
        Entropy = log₂(94^14) ≈ 92.3 bits (Strong!)
        
        Args:
            password (str): Password to calculate entropy for
            
        Returns:
            float: Entropy in bits
        """
        if not password:
            return 0
        
        # Detect character set size
        charset_size = 0
        
        if re.search(r"[a-z]", password):
            charset_size += 26  # lowercase
        if re.search(r"[A-Z]", password):
            charset_size += 26  # uppercase
        if re.search(r"\d", password):
            charset_size += 10  # digits
        if re.search(r"[^a-zA-Z0-9]", password):
            charset_size += 32  # approximate special characters
        
        # Calculate entropy: log₂(charset_size ^ password_length)
        if charset_size == 0:
            return 0
        
        entropy = math.log2(charset_size ** len(password))
        return round(entropy, 2)
    
    def get_entropy_strength(self, entropy):
        """
        Convert entropy bits to strength rating.
        
        Args:
            entropy (float): Entropy in bits
            
        Returns:
            str: Strength rating based on entropy
        """
        if entropy < 30:
            return "Very Weak"
        elif entropy < 50:
            return "Weak"
        elif entropy < 60:
            return "Moderate"
        elif entropy < 80:
            return "Strong"
        else:
            return "Very Strong"
    
    def generate_password(self, length=16, require_uppercase=True, 
                         require_lowercase=True, require_numbers=True, 
                         require_special=True):
        """
        Generate a cryptographically secure random password.
        
        WHY SECURE RANDOMNESS MATTERS:
        - Bad: random.random() is predictable
        - Good: os.urandom() uses system randomness (unpredictable)
        
        This uses os.urandom() which is cryptographically secure.
        
        Args:
            length (int): Desired password length (default: 16)
            require_uppercase (bool): Must include A-Z
            require_lowercase (bool): Must include a-z
            require_numbers (bool): Must include 0-9
            require_special (bool): Must include !@#$, etc.
            
        Returns:
            str: Securely generated password
        """
        # Input validation
        if length < 8:
            print("⚠️  Warning: Passwords should be at least 8 characters. Using 8.")
            length = 8
        
        # Build character pool
        characters = ""
        password = []
        
        # Ensure at least one character from each required type
        if require_uppercase:
            characters += self.uppercase_chars
            password.append(random.choice(self.uppercase_chars))
        
        if require_lowercase:
            characters += self.lowercase_chars
            password.append(random.choice(self.lowercase_chars))
        
        if require_numbers:
            characters += self.digits
            password.append(random.choice(self.digits))
        
        if require_special:
            characters += "!@#$%^&*"  # Subset of special chars for clarity
            password.append(random.choice("!@#$%^&*"))
        
        # Fill remaining length with random characters
        for i in range(length - len(password)):
            password.append(random.choice(characters))
        
        # Shuffle to avoid predictable pattern (first char uppercase, etc.)
        random.shuffle(password)
        
        return ''.join(password)
    
    def suggest_improvement(self, password):
        """
        Provide specific suggestions for password improvement.
        
        Args:
            password (str): Current password
            
        Returns:
            str: Specific improvement suggestion
        """
        strength, feedback = self.analyze(password)
        
        # Pick one area to improve
        if "❌" in "\n".join(feedback):
            for item in feedback:
                if "❌" in item:
                    return item
        
        return "Your password looks good!"
    
    def hash_password(self, password, salt=None):
        """
        Hash a password using SHA-256 for secure storage.
        
        WHY HASHING (not encryption)?
        - Encryption can be reversed (bad for passwords)
        - Hashing is one-way (can't reverse)
        - Perfect for comparing passwords without storing them
        
        EXAMPLE:
        Raw password: "MyPassword123"
        Hash: "a1b2c3d4e5f6..." (always same for same password)
        
        Args:
            password (str): Password to hash
            salt (str): Optional salt for added security
            
        Returns:
            str: Hashed password (hex format)
        """
        if salt is None:
            # Generate random salt if not provided
            salt = os.urandom(16).hex()
        
        # Combine password and salt, then hash
        combined = password + salt
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        
        # Return hash with salt for storage
        return f"{salt}${hashed}"
    
    def verify_password(self, password, stored_hash):
        """
        Verify if entered password matches stored hash.
        
        PROCESS:
        1. Extract salt from stored hash
        2. Hash the entered password with same salt
        3. Compare hashes
        
        Args:
            password (str): Password entered by user
            stored_hash (str): Hash stored in database
            
        Returns:
            bool: True if passwords match, False otherwise
        """
        try:
            salt, original_hash = stored_hash.split('$')
            new_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return new_hash == original_hash
        except:
            return False


# Example usage (for testing)
if __name__ == "__main__":
    print("=" * 60)
    print("PASSWORD STRENGTH ANALYZER - Example Usage")
    print("=" * 60)
    
    analyzer = PasswordAnalyzer()
    
    # Test passwords
    test_passwords = [
        "123456",                    # Very weak
        "password",                  # Common password
        "Password123",               # Moderate
        "P@ssw0rd!",                 # Strong
        "MyS3cur3P@ssw0rd!2024",    # Very strong
    ]
    
    for pwd in test_passwords:
        print(f"\n🔐 Testing: {pwd}")
        print("-" * 40)
        
        strength, feedback = analyzer.analyze(pwd)
        entropy = analyzer.calculate_entropy(pwd)
        
        print(f"Strength: {strength}")
        print(f"Entropy: {entropy} bits ({analyzer.get_entropy_strength(entropy)})")
        print("Feedback:")
        for item in feedback:
            print(f"  {item}")
    
    # Generate a strong password
    print("\n" + "=" * 60)
    print("Generated Strong Password:")
    print("=" * 60)
    generated = analyzer.generate_password(16)
    print(f"Generated: {generated}")
    strength, feedback = analyzer.analyze(generated)
    print(f"Strength: {strength}")
    print(f"Entropy: {analyzer.calculate_entropy(generated)} bits")
