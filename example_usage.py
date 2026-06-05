"""
EXAMPLE 1: Basic Usage - Using Password Analyzer as a Library

This example shows how to use the PasswordAnalyzer class
in your own Python code.

BEGINNER CONCEPTS:
- Importing modules
- Creating instances of classes
- Calling methods
- Working with return values
"""

from password_analyzer import PasswordAnalyzer


def example_1_basic_analysis():
    """Example 1: Analyze a single password."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Password Analysis")
    print("=" * 60)
    
    # Step 1: Create analyzer instance
    analyzer = PasswordAnalyzer()
    
    # Step 2: Analyze a password
    password = "MyPassword123"
    strength, feedback = analyzer.analyze(password)
    
    # Step 3: Display results
    print(f"\nPassword: {password}")
    print(f"Strength: {strength}")
    print("\nFeedback:")
    for item in feedback:
        print(f"  {item}")


def example_2_compare_passwords():
    """Example 2: Compare multiple passwords."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Compare Multiple Passwords")
    print("=" * 60)
    
    analyzer = PasswordAnalyzer()
    
    passwords = [
        "123456",
        "password",
        "MyPassword123",
        "MyS3cur3P@ssw0rd!",
    ]
    
    print("\nComparing passwords:\n")
    
    for pwd in passwords:
        strength, _ = analyzer.analyze(pwd)
        entropy = analyzer.calculate_entropy(pwd)
        
        print(f"'{pwd}'")
        print(f"  Strength: {strength}")
        print(f"  Entropy: {entropy} bits")
        print()


def example_3_full_analysis():
    """Example 3: Detailed analysis of a password."""
    print("=" * 60)
    print("EXAMPLE 3: Detailed Password Analysis")
    print("=" * 60)
    
    analyzer = PasswordAnalyzer()
    password = "MySecureP@ss2024"
    
    print(f"\nAnalyzing: {password}\n")
    
    # Get strength and feedback
    strength, feedback = analyzer.analyze(password)
    print(f"Overall Strength: {strength}")
    
    # Get complexity breakdown
    complexity_score, details = analyzer.check_complexity(password)
    print(f"\nComplexity Score: {complexity_score}/4")
    print(f"  Uppercase: {'✅' if details['uppercase'] else '❌'}")
    print(f"  Lowercase: {'✅' if details['lowercase'] else '❌'}")
    print(f"  Numbers: {'✅' if details['numbers'] else '❌'}")
    print(f"  Special Chars: {'✅' if details['special'] else '❌'}")
    
    # Calculate entropy
    entropy = analyzer.calculate_entropy(password)
    entropy_strength = analyzer.get_entropy_strength(entropy)
    print(f"\nEntropy: {entropy} bits")
    print(f"Entropy Strength: {entropy_strength}")
    
    # Get feedback
    print("\nFeedback:")
    for item in feedback:
        print(f"  {item}")


def example_4_generate_passwords():
    """Example 4: Generate strong passwords."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Generate Strong Passwords")
    print("=" * 60)
    
    analyzer = PasswordAnalyzer()
    
    print("\nGenerating 5 secure passwords:\n")
    
    for i in range(5):
        password = analyzer.generate_password(16)
        strength, _ = analyzer.analyze(password)
        
        print(f"{i+1}. {password}")
        print(f"   Strength: {strength}\n")


def example_5_custom_length():
    """Example 5: Generate passwords with custom settings."""
    print("=" * 60)
    print("EXAMPLE 5: Custom Password Generation")
    print("=" * 60)
    
    analyzer = PasswordAnalyzer()
    
    configs = [
        {"length": 8, "label": "Short (8 chars)"},
        {"length": 12, "label": "Medium (12 chars)"},
        {"length": 20, "label": "Long (20 chars)"},
    ]
    
    print()
    for config in configs:
        password = analyzer.generate_password(config["length"])
        strength, _ = analyzer.analyze(password)
        entropy = analyzer.calculate_entropy(password)
        
        print(f"{config['label']}:")
        print(f"  Password: {password}")
        print(f"  Strength: {strength}")
        print(f"  Entropy: {entropy} bits\n")


def example_6_password_hashing():
    """Example 6: Hash and verify passwords."""
    print("=" * 60)
    print("EXAMPLE 6: Password Hashing and Verification")
    print("=" * 60)
    
    analyzer = PasswordAnalyzer()
    
    password = "MySecurePassword123"
    
    # Hash the password
    print(f"\nOriginal Password: {password}")
    hash_value = analyzer.hash_password(password)
    print(f"Hashed: {hash_value[:50]}... (truncated)")
    
    # Verify correct password
    print("\nVerifying passwords:")
    correct = analyzer.verify_password("MySecurePassword123", hash_value)
    wrong = analyzer.verify_password("WrongPassword", hash_value)
    
    print(f"  'MySecurePassword123': {'✅ CORRECT' if correct else '❌ WRONG'}")
    print(f"  'WrongPassword': {'✅ CORRECT' if wrong else '❌ WRONG'}")


def example_7_security_best_practices():
    """Example 7: Demonstrate security best practices."""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Security Best Practices")
    print("=" * 60)
    
    analyzer = PasswordAnalyzer()
    
    print("\n🔒 BEST PRACTICES FOR PASSWORD SECURITY:")
    print("\n1. USE LONG PASSWORDS (12+ characters)")
    print("   Why: Exponentially harder to crack")
    
    password1 = "Pass1234"  # 8 chars
    password2 = "MySecurePassword1234"  # 20 chars
    
    entropy1 = analyzer.calculate_entropy(password1)
    entropy2 = analyzer.calculate_entropy(password2)
    
    print(f"   8 chars: {entropy1} bits")
    print(f"   20 chars: {entropy2} bits")
    print(f"   Difference: {entropy2 - entropy1} bits (much harder!)")
    
    print("\n2. USE MIXED CHARACTER TYPES")
    print("   Why: Increases character set from 26 to 94 possibilities")
    
    lowercase = "password"
    mixed = "MyPassword123!"
    
    strength_low, _ = analyzer.analyze(lowercase)
    strength_mix, _ = analyzer.analyze(mixed)
    
    print(f"   Lowercase only: {strength_low}")
    print(f"   Mixed chars: {strength_mix}")
    
    print("\n3. AVOID COMMON WORDS")
    print("   Why: Dictionary attacks try common passwords first")
    
    print("   ❌ DON'T USE: password, 123456, letmein")
    print("   ✅ DO USE: Random combinations")
    
    print("\n4. USE UNIQUE PASSWORDS FOR EACH SITE")
    print("   Why: If one site is hacked, others stay safe")
    
    print("   ❌ DON'T: Same password everywhere")
    print("   ✅ DO: Different password for each account")
    
    print("\n5. USE A PASSWORD MANAGER")
    print("   Why: Remember one master password, manage all others")
    print("   Examples: Bitwarden, 1Password, KeePass")


def example_8_batch_analysis():
    """Example 8: Batch analyze passwords from a list."""
    print("\n" + "=" * 60)
    print("EXAMPLE 8: Batch Analysis")
    print("=" * 60)
    
    analyzer = PasswordAnalyzer()
    
    # List of passwords to analyze
    test_passwords = [
        ("weak1", "123456"),
        ("moderate1", "Password123"),
        ("strong1", "MySecureP@ss2024"),
        ("common1", "password"),
    ]
    
    print("\nBatch Analysis Results:\n")
    print(f"{'Label':<12} {'Password':<20} {'Strength':<12} {'Entropy':>10}")
    print("-" * 60)
    
    for label, password in test_passwords:
        strength, _ = analyzer.analyze(password)
        entropy = analyzer.calculate_entropy(password)
        
        print(f"{label:<12} {password:<20} {strength:<12} {entropy:>10.2f}")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("PASSWORD STRENGTH ANALYZER - USAGE EXAMPLES")
    print("=" * 80)
    
    # Run all examples
    example_1_basic_analysis()
    example_2_compare_passwords()
    example_3_full_analysis()
    example_4_generate_passwords()
    example_5_custom_length()
    example_6_password_hashing()
    example_7_security_best_practices()
    example_8_batch_analysis()
    
    print("\n" + "=" * 80)
    print("✅ All examples completed!")
    print("=" * 80)
    print("\nFor more information:")
    print("  - Read README.md for detailed documentation")
    print("  - Check main.py for interactive mode: python main.py")
    print("  - Run tests: python -m pytest test_password_analyzer.py")
    print()


if __name__ == "__main__":
    main()
