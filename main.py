"""
PASSWORD STRENGTH ANALYZER - Main CLI Application

This is the entry point for using the Password Strength Analyzer.
It provides an interactive command-line interface for users.

MODES:
1. Interactive Mode: Step-by-step guided experience
2. CLI Mode: Quick one-command operations
3. Demo Mode: Show examples

Author: Educational Purpose
Date: June 2026
"""

import sys
import argparse
from password_analyzer import PasswordAnalyzer
from database_manager import DatabaseManager
import hashlib
import os


class PasswordAnalyzerApp:
    """Main application class for CLI interface."""
    
    def __init__(self):
        """Initialize the application."""
        self.analyzer = PasswordAnalyzer()
        self.db = None  # Optional database
        self.current_user_id = None
    
    def display_header(self):
        """Display application header."""
        print("\n" + "=" * 60)
        print("🔐 PASSWORD STRENGTH ANALYZER")
        print("=" * 60)
    
    def display_footer(self):
        """Display application footer."""
        print("=" * 60)
    
    def interactive_mode(self):
        """
        Interactive mode: Guide user through analysis step-by-step.
        
        This is the BEST mode for beginners - explains everything!
        """
        self.display_header()
        print("📚 INTERACTIVE MODE - Beginner Friendly")
        print("-" * 60)
        
        print("\n👋 Welcome to Password Strength Analyzer!")
        print("\nThis tool will help you understand password security.")
        print("Let's learn about what makes passwords strong...\n")
        
        while True:
            print("\n" + "-" * 60)
            print("WHAT WOULD YOU LIKE TO DO?")
            print("-" * 60)
            print("1. Analyze a password")
            print("2. Generate a strong password")
            print("3. Learn about password security")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                self._analyze_password_interactive()
            elif choice == "2":
                self._generate_password_interactive()
            elif choice == "3":
                self._show_security_lessons()
            elif choice == "4":
                print("\n👋 Thank you for using Password Strength Analyzer!")
                print("Stay secure! 🔐\n")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def _analyze_password_interactive(self):
        """Analyze password in interactive mode."""
        print("\n" + "=" * 60)
        print("ANALYZE YOUR PASSWORD")
        print("=" * 60)
        
        # Get password input
        while True:
            password = input("\nEnter a password to analyze: ")
            
            if not password:
                print("❌ Password cannot be empty!")
                continue
            
            if len(password) < 4:
                print("⚠️  Very short password - are you sure? (y/n): ", end="")
                if input().lower() != "y":
                    continue
            
            break
        
        # Analyze
        print("\n🔍 Analyzing password...")
        strength, feedback = self.analyzer.analyze(password)
        entropy = self.analyzer.calculate_entropy(password)
        
        # Display results
        print("\n" + "-" * 60)
        print("ANALYSIS RESULTS")
        print("-" * 60)
        
        # Strength with visual indicator
        strength_icons = {
            "Weak": "🔴",
            "Moderate": "🟡",
            "Strong": "🟢",
            "Very Strong": "💪"
        }
        
        print(f"\n💪 Strength: {strength_icons.get(strength, '❓')} {strength}")
        print(f"\n📊 Entropy: {entropy} bits ({self.analyzer.get_entropy_strength(entropy)})")
        
        print("\n📝 FEEDBACK:")
        for item in feedback:
            print(f"  {item}")
        
        # Complexity breakdown
        complexity_score, details = self.analyzer.check_complexity(password)
        print(f"\n🔍 COMPLEXITY BREAKDOWN (Score: {complexity_score}/4):")
        print(f"  {'✅' if details['uppercase'] else '❌'} Uppercase letters")
        print(f"  {'✅' if details['lowercase'] else '❌'} Lowercase letters")
        print(f"  {'✅' if details['numbers'] else '❌'} Numbers")
        print(f"  {'✅' if details['special'] else '❌'} Special characters")
        
        print("\n" + "-" * 60)
        
        # Ask for next action
        print("\nNEXT STEPS:")
        print("1. Try a stronger password")
        print("2. Generate a secure password")
        print("3. Return to main menu")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            suggestion = self.analyzer.suggest_improvement(password)
            print(f"\n💡 SUGGESTION: {suggestion}")
            self._analyze_password_interactive()
        elif choice == "2":
            self._generate_password_interactive()
    
    def _generate_password_interactive(self):
        """Generate password in interactive mode."""
        print("\n" + "=" * 60)
        print("GENERATE A STRONG PASSWORD")
        print("=" * 60)
        
        print("\n📋 PASSWORD GENERATION OPTIONS:")
        
        # Get length
        while True:
            try:
                length_input = input("\nDesired password length (8-32, default 16): ").strip()
                length = int(length_input) if length_input else 16
                
                if 8 <= length <= 32:
                    break
                else:
                    print("❌ Length must be between 8 and 32")
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Generate
        print("\n🔨 Generating secure password...")
        password = self.analyzer.generate_password(length)
        
        # Analyze generated password
        strength, feedback = self.analyzer.analyze(password)
        entropy = self.analyzer.calculate_entropy(password)
        
        print("\n" + "-" * 60)
        print("GENERATED PASSWORD")
        print("-" * 60)
        print(f"\n🔑 PASSWORD: {password}")
        print(f"\n💪 Strength: {strength}")
        print(f"📊 Entropy: {entropy} bits")
        
        print("\n✅ This password is secure because:")
        print("  ✓ Long enough (harder to guess)")
        print("  ✓ Mixed character types (uppercase, lowercase, numbers, symbols)")
        print("  ✓ Randomly generated (unpredictable)")
        print("  ✓ High entropy (lots of randomness)")
        
        print("\n💡 TIPS FOR USE:")
        print("  1. Use unique passwords for each website")
        print("  2. Store in a password manager (like Bitwarden, 1Password)")
        print("  3. Never share your password")
        print("  4. Change if compromised")
        
        print("\n📋 OPTIONS:")
        print("1. Generate another")
        print("2. Copy to clipboard")
        print("3. Analyze this password")
        print("4. Return to main menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            self._generate_password_interactive()
        elif choice == "2":
            print(f"\n✅ Password: {password}")
            print("(Copy manually - clipboard not available in this demo)")
        elif choice == "3":
            print("\n🔍 Analyzing generated password...")
            # Show analysis
            _, feedback_list = self.analyzer.analyze(password)
            print("Feedback:")
            for item in feedback_list:
                print(f"  {item}")
        elif choice == "4":
            pass
    
    def _show_security_lessons(self):
        """Show security education content."""
        print("\n" + "=" * 60)
        print("🎓 PASSWORD SECURITY LESSONS")
        print("=" * 60)
        
        lessons = {
            "1": {
                "title": "WHY PASSWORD LENGTH MATTERS",
                "content": """
Length = Number of characters in password

WHY IT MATTERS:
- Each additional character multiplies difficulty to crack
- 8 characters: 10^8 = 100 million combinations
- 12 characters: 10^12 = 1 trillion combinations
- 16 characters: 10^16 = 10 quadrillion combinations

EXPONENTIAL GROWTH:
- 1 more char = ~10x harder to crack
- 4 more chars = ~10,000x harder to crack

RECOMMENDATION: Use minimum 8, prefer 12+
                """
            },
            "2": {
                "title": "COMPLEXITY VS. LENGTH",
                "content": """
COMPLEXITY = Using different character types

TYPES OF CHARACTERS:
- Uppercase: A-Z (26 options)
- Lowercase: a-z (26 options)
- Numbers: 0-9 (10 options)
- Special: !@#$%^&* (32 options)

IMPACT:
- Only lowercase: 26^8 combinations
- Uppercase + lowercase: 52^8 combinations
- + Numbers: 62^8 combinations
- + Special: 94^8 combinations

94^8 is TRILLIONS times harder than 26^8!

TIP: Length is MORE important than complexity
     Prefer: Long + simple (MyDogIsFluffy2024)
     Over: Short + complex (P@!#)
                """
            },
            "3": {
                "title": "COMMON PASSWORD ATTACKS",
                "content": """
HOW HACKERS CRACK PASSWORDS:

1. DICTIONARY ATTACK
   - Try common words: password, 123456, letmein
   - Fast for dictionary words
   - Solution: Avoid common words

2. BRUTE FORCE
   - Try every possible combination
   - Takes longer with longer passwords
   - Solution: Use long passwords (8+)

3. RAINBOW TABLE
   - Pre-computed hashes of common passwords
   - Very fast for common passwords
   - Solution: Hashing + salting (server's job)

4. PHISHING
   - Trick users into giving password
   - Can't prevent with strong password
   - Solution: Verify site is real, use 2FA

5. KEYLOGGER
   - Record what user types
   - Can't prevent with strong password
   - Solution: Use password manager

BEST DEFENSE: Use unique, long passwords everywhere
             Use password manager to remember them
             Enable two-factor authentication (2FA)
                """
            },
            "4": {
                "title": "HASHING 101",
                "content": """
WHAT IS HASHING?

Hashing = Converting data into fixed-size code (ONE-WAY)

EXAMPLE:
Input: "MyPassword123"
Output: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6" (SHA-256)

KEY PROPERTIES:
1. DETERMINISTIC: Same input = same output
   "MyPassword123" → always same hash

2. ONE-WAY: Can't reverse the process
   Hash → Can't get back original password

3. SENSITIVE: Tiny change = completely different hash
   "MyPassword123" → hash1
   "MyPassword124" → hash2 (completely different!)

4. FIXED SIZE: Any size input → fixed output
   "a" → 64-character hash
   "MyVeryLongPasswordWith1000Characters" → 64-character hash

WHY USE FOR PASSWORDS:
- Never store raw passwords
- If database hacked, attacker gets hashes, not passwords
- Can verify without exposing password

HASHING ≠ ENCRYPTION:
- Hashing: One-way (no decryption possible)
- Encryption: Two-way (can decrypt with key)
                """
            }
        }
        
        while True:
            print("\n" + "-" * 60)
            print("CHOOSE A LESSON:")
            print("-" * 60)
            for key in sorted(lessons.keys()):
                print(f"{key}. {lessons[key]['title']}")
            print("0. Return to main menu")
            
            choice = input("\nEnter your choice (0-4): ").strip()
            
            if choice == "0":
                break
            elif choice in lessons:
                print("\n" + "=" * 60)
                print(lessons[choice]['title'].upper())
                print("=" * 60)
                print(lessons[choice]['content'])
            else:
                print("❌ Invalid choice")
    
    def cli_mode(self, args):
        """
        CLI mode: Quick command-line operations.
        
        Args:
            args: Command-line arguments
        """
        if args.command == "check":
            password = args.password
            strength, feedback = self.analyzer.analyze(password)
            
            print(f"\n🔐 Password: {password}")
            print(f"💪 Strength: {strength}")
            print(f"📊 Entropy: {self.analyzer.calculate_entropy(password)} bits")
            print(f"\nFeedback:")
            for item in feedback:
                print(f"  {item}")
        
        elif args.command == "generate":
            length = args.length if args.length else 16
            password = self.analyzer.generate_password(length)
            print(f"\n🔑 Generated Password: {password}")
            
            strength, _ = self.analyzer.analyze(password)
            print(f"💪 Strength: {strength}")
        
        elif args.command == "demo":
            self.show_demo()
    
    def show_demo(self):
        """Show demonstration with example passwords."""
        print("\n" + "=" * 60)
        print("DEMO: PASSWORD STRENGTH EXAMPLES")
        print("=" * 60)
        
        examples = [
            ("123456", "❌ Very weak - numbers only"),
            ("password", "❌ Very weak - common word"),
            ("Password123", "🟡 Moderate - missing special char"),
            ("P@ssw0rd!", "🟢 Strong - good variety"),
            ("MyS3cur3P@ss2024!", "💪 Very strong - excellent"),
        ]
        
        for pwd, description in examples:
            print(f"\n{description}")
            print(f"  Password: {pwd}")
            
            strength, feedback = self.analyzer.analyze(pwd)
            entropy = self.analyzer.calculate_entropy(pwd)
            
            print(f"  Strength: {strength}")
            print(f"  Entropy: {entropy} bits")
            print(f"  Feedback: {feedback[0] if feedback else 'None'}")


def main():
    """Main entry point for the application."""
    
    parser = argparse.ArgumentParser(
        description='Password Strength Analyzer - Learn Password Security',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
USAGE EXAMPLES:
  python main.py                          # Interactive mode (recommended)
  python main.py check "MyPassword123"    # Check a password
  python main.py generate --length 16     # Generate password
  python main.py demo                     # Show examples
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Analyze a password')
    check_parser.add_argument('password', help='Password to analyze')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate strong password')
    gen_parser.add_argument('--length', type=int, default=16, help='Password length')
    
    # Demo command
    subparsers.add_parser('demo', help='Show example analysis')
    
    args = parser.parse_args()
    
    app = PasswordAnalyzerApp()
    
    if args.command:
        app.cli_mode(args)
    else:
        # Interactive mode (default)
        app.interactive_mode()


if __name__ == "__main__":
    main()
