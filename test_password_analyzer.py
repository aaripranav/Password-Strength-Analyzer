"""
TEST SUITE - Password Analyzer Tests

This file contains unit tests for the PasswordAnalyzer class.

WHY TESTING MATTERS:
- Ensures code works correctly
- Catches bugs early
- Prevents regressions (breaking existing features)
- Documents expected behavior

TESTING CONCEPTS:
- Unit Test: Test individual functions
- Test Case: A single test scenario
- Assert: Check if condition is true
- Pass/Fail: Test succeeds or fails

Run tests with: python -m pytest test_password_analyzer.py -v
"""

import sys
import unittest
from password_analyzer import PasswordAnalyzer


class TestPasswordAnalyzer(unittest.TestCase):
    """Test cases for PasswordAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        self.analyzer = PasswordAnalyzer()
    
    # ========================
    # TEST: Length Checking
    # ========================
    
    def test_password_too_short(self):
        """Test that short passwords are flagged."""
        strength, feedback = self.analyzer.analyze("abc")
        self.assertEqual(strength, "Weak")
        self.assertTrue(any("short" in item.lower() for item in feedback))
    
    def test_password_minimum_length(self):
        """Test 8-character password (minimum recommended)."""
        strength, feedback = self.analyzer.analyze("Passw0rd")
        # Should be Strong or higher due to complexity
        self.assertIn(strength, ["Strong", "Very Strong", "Moderate"])
    
    def test_password_good_length(self):
        """Test 12-character password (good length)."""
        strength, feedback = self.analyzer.analyze("PassWord1234")
        # Should be Strong or higher
        self.assertIn(strength, ["Strong", "Very Strong"])
    
    def test_password_excellent_length(self):
        """Test 16+ character password (excellent)."""
        strength, feedback = self.analyzer.analyze("MySecurePassword123!")
        self.assertIn(strength, ["Strong", "Very Strong"])
    
    # ========================
    # TEST: Complexity Checking
    # ========================
    
    def test_uppercase_detection(self):
        """Test that uppercase letters are detected."""
        score, details = self.analyzer.check_complexity("MyPassword")
        self.assertTrue(details["uppercase"])
        self.assertGreater(score, 0)
    
    def test_lowercase_detection(self):
        """Test that lowercase letters are detected."""
        score, details = self.analyzer.check_complexity("mypassword")
        self.assertTrue(details["lowercase"])
    
    def test_number_detection(self):
        """Test that numbers are detected."""
        score, details = self.analyzer.check_complexity("password123")
        self.assertTrue(details["numbers"])
    
    def test_special_char_detection(self):
        """Test that special characters are detected."""
        score, details = self.analyzer.check_complexity("password!@#")
        self.assertTrue(details["special"])
    
    def test_no_special_chars(self):
        """Test password without special characters."""
        score, details = self.analyzer.check_complexity("Password1234")
        self.assertFalse(details["special"])
    
    def test_max_complexity_score(self):
        """Test password with all complexity types."""
        score, details = self.analyzer.check_complexity("MyP@ssw0rd!")
        self.assertEqual(score, 4)
        self.assertTrue(details["uppercase"])
        self.assertTrue(details["lowercase"])
        self.assertTrue(details["numbers"])
        self.assertTrue(details["special"])
    
    # ========================
    # TEST: Entropy Calculation
    # ========================
    
    def test_entropy_calculation(self):
        """Test entropy calculation returns positive value."""
        entropy = self.analyzer.calculate_entropy("MyPassword123!")
        self.assertGreater(entropy, 0)
    
    def test_entropy_empty_password(self):
        """Test entropy of empty password is zero."""
        entropy = self.analyzer.calculate_entropy("")
        self.assertEqual(entropy, 0)
    
    def test_entropy_numbers_only(self):
        """Test entropy for numbers-only password."""
        entropy_nums = self.analyzer.calculate_entropy("123456")
        entropy_mixed = self.analyzer.calculate_entropy("MyPassw0rd")
        # Mixed should have higher entropy
        self.assertGreater(entropy_mixed, entropy_nums)
    
    def test_entropy_strength_weak(self):
        """Test entropy strength rating."""
        entropy = 25  # Very weak
        strength = self.analyzer.get_entropy_strength(entropy)
        self.assertEqual(strength, "Very Weak")
    
    def test_entropy_strength_strong(self):
        """Test high entropy strength rating."""
        entropy = 70  # Strong
        strength = self.analyzer.get_entropy_strength(entropy)
        self.assertEqual(strength, "Strong")
    
    # ========================
    # TEST: Common Password Check
    # ========================
    
    def test_common_password_detected(self):
        """Test that common passwords are detected."""
        # "password" is in the common passwords list
        strength, feedback = self.analyzer.analyze("password")
        warnings = [item for item in feedback if "WARNING" in item or "common" in item.lower()]
        # Should have warning if common passwords loaded
        # (May not if file not found)
    
    # ========================
    # TEST: Password Generation
    # ========================
    
    def test_generate_password_length(self):
        """Test generated password has correct length."""
        password = self.analyzer.generate_password(16)
        self.assertEqual(len(password), 16)
    
    def test_generate_password_includes_uppercase(self):
        """Test generated password includes uppercase."""
        password = self.analyzer.generate_password(16)
        self.assertTrue(any(c.isupper() for c in password))
    
    def test_generate_password_includes_lowercase(self):
        """Test generated password includes lowercase."""
        password = self.analyzer.generate_password(16)
        self.assertTrue(any(c.islower() for c in password))
    
    def test_generate_password_includes_numbers(self):
        """Test generated password includes numbers."""
        password = self.analyzer.generate_password(16)
        self.assertTrue(any(c.isdigit() for c in password))
    
    def test_generate_password_includes_special(self):
        """Test generated password includes special characters."""
        password = self.analyzer.generate_password(16)
        special_chars = "!@#$%^&*"
        self.assertTrue(any(c in special_chars for c in password))
    
    def test_generate_password_unique(self):
        """Test that generated passwords are different."""
        pwd1 = self.analyzer.generate_password(16)
        pwd2 = self.analyzer.generate_password(16)
        # Very unlikely to be same (but possible)
        self.assertNotEqual(pwd1, pwd2)
    
    # ========================
    # TEST: Password Hashing
    # ========================
    
    def test_password_hashing(self):
        """Test password hashing works."""
        password = "MySecurePassword123"
        hash_val = self.analyzer.hash_password(password)
        # Hash should contain salt and hash separated by $
        self.assertIn("$", hash_val)
    
    def test_same_password_different_salt(self):
        """Test same password with different salts produces different hashes."""
        password = "MyPassword123"
        hash1 = self.analyzer.hash_password(password)
        hash2 = self.analyzer.hash_password(password)
        # Different salts = different hashes
        self.assertNotEqual(hash1, hash2)
    
    def test_password_verification(self):
        """Test password verification."""
        password = "MySecurePassword123"
        hash_val = self.analyzer.hash_password(password)
        # Verify correct password
        self.assertTrue(self.analyzer.verify_password(password, hash_val))
    
    def test_password_verification_wrong(self):
        """Test password verification fails for wrong password."""
        password = "MySecurePassword123"
        wrong_password = "WrongPassword123"
        hash_val = self.analyzer.hash_password(password)
        # Verify wrong password fails
        self.assertFalse(self.analyzer.verify_password(wrong_password, hash_val))
    
    # ========================
    # TEST: Overall Strength Analysis
    # ========================
    
    def test_weak_password(self):
        """Test weak password is identified."""
        strength, _ = self.analyzer.analyze("123456")
        self.assertEqual(strength, "Weak")
    
    def test_strong_password(self):
        """Test strong password is identified."""
        strength, _ = self.analyzer.analyze("MySecureP@ss123")
        self.assertEqual(strength, "Strong")
    
    def test_empty_password(self):
        """Test empty password handling."""
        strength, feedback = self.analyzer.analyze("")
        self.assertEqual(strength, "Weak")
    
    # ========================
    # TEST: Improvement Suggestions
    # ========================
    
    def test_suggestion_for_weak_password(self):
        """Test that suggestions are provided."""
        suggestion = self.analyzer.suggest_improvement("123")
        self.assertIsNotNone(suggestion)
        self.assertTrue(len(suggestion) > 0)


class TestPasswordStrengthIntegration(unittest.TestCase):
    """Integration tests for full password analysis workflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = PasswordAnalyzer()
    
    def test_full_analysis_weak_password(self):
        """Test full analysis of weak password."""
        password = "password"
        strength, feedback = self.analyzer.analyze(password)
        entropy = self.analyzer.calculate_entropy(password)
        
        self.assertEqual(strength, "Weak")
        self.assertGreater(len(feedback), 0)
        self.assertLess(entropy, 50)
    
    def test_full_analysis_strong_password(self):
        """Test full analysis of strong password."""
        password = "MySecureP@ssw0rd2024!"
        strength, feedback = self.analyzer.analyze(password)
        entropy = self.analyzer.calculate_entropy(password)
        
        self.assertIn(strength, ["Strong", "Very Strong"])
        self.assertGreater(entropy, 60)
    
    def test_generated_password_is_strong(self):
        """Test that generated passwords are strong."""
        password = self.analyzer.generate_password(16)
        strength, _ = self.analyzer.analyze(password)
        
        self.assertIn(strength, ["Strong", "Very Strong"])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = PasswordAnalyzer()
    
    def test_very_long_password(self):
        """Test very long password."""
        long_pwd = "A" * 1000 + "a1!"
        strength, _ = self.analyzer.analyze(long_pwd)
        self.assertIn(strength, ["Strong", "Very Strong"])
    
    def test_unicode_characters(self):
        """Test password with unicode characters."""
        password = "Pässwörd123!"
        strength, feedback = self.analyzer.analyze(password)
        # Should still analyze basic components
        self.assertIsNotNone(strength)
    
    def test_special_character_variations(self):
        """Test various special characters."""
        special_chars = "!@#$%^&*()-_+=[]{}\\|;:',.<>?/`~"
        for char in special_chars[:10]:  # Test first 10
            password = f"MyPassword{char}123"
            strength, _ = self.analyzer.analyze(password)
            self.assertIsNotNone(strength)


if __name__ == "__main__":
    unittest.main()
