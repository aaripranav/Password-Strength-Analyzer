"""
DATABASE MANAGER - Optional Password History Tracking

This module handles optional database operations for:
1. Storing password hashes securely
2. Tracking password history (preventing reuse)
3. Storing user information

KEY CONCEPTS:
- Never store plain passwords
- Store hashes with salts
- Track password timestamps
- Prevent old password reuse

Author: Educational Purpose
Date: June 2026
"""

import sqlite3
import hashlib
import os
from datetime import datetime


class DatabaseManager:
    """
    Manages database operations for password history tracking.
    
    This class demonstrates how real systems prevent password reuse
    and maintain secure password records.
    """
    
    def __init__(self, db_path="password_history.db"):
        """
        Initialize database connection.
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """
        Create database tables if they don't exist.
        
        Tables:
        1. users: Stores user information
        2. password_history: Stores hashes of past passwords
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table 1: Users
        # Stores basic user information (NOT passwords!)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table 2: Password History
        # Stores hashes of PREVIOUS passwords (never raw passwords!)
        # WHY: Prevents reusing the same password
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS password_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username, email=None):
        """
        Create a new user account.
        
        Args:
            username (str): Username (must be unique)
            email (str): User email (optional)
            
        Returns:
            int: User ID, or None if failed
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, email)
                VALUES (?, ?)
            ''', (username, email))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            print(f"✅ User '{username}' created (ID: {user_id})")
            return user_id
        
        except sqlite3.IntegrityError:
            print(f"❌ Error: Username '{username}' already exists")
            return None
    
    def store_password_hash(self, user_id, password_hash, salt):
        """
        Store password hash in history.
        
        This happens when:
        1. User creates account
        2. User changes password
        
        WHY: We store hashes to prevent password reuse
        
        Args:
            user_id (int): ID of user
            password_hash (str): SHA-256 hash of password
            salt (str): Salt used in hashing
            
        Returns:
            bool: True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO password_history (user_id, password_hash, salt)
                VALUES (?, ?, ?)
            ''', (user_id, password_hash, salt))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Password hash stored for user {user_id}")
            return True
        
        except Exception as e:
            print(f"❌ Error storing password: {e}")
            return False
    
    def get_password_history(self, user_id, limit=10):
        """
        Retrieve password history for a user.
        
        Args:
            user_id (int): ID of user
            limit (int): Maximum number of old passwords to check
            
        Returns:
            list: List of tuples (password_hash, salt, changed_at)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT password_hash, salt, changed_at
                FROM password_history
                WHERE user_id = ?
                ORDER BY changed_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            history = cursor.fetchall()
            conn.close()
            
            return history
        
        except Exception as e:
            print(f"❌ Error retrieving history: {e}")
            return []
    
    def check_password_reuse(self, user_id, new_password_hash, new_salt):
        """
        Check if user is trying to reuse an old password.
        
        WHY: Some systems prevent reusing old passwords for security
        
        PROCESS:
        1. Get user's password history
        2. Hash the new password same way each old one was hashed
        3. Compare hashes
        
        Args:
            user_id (int): ID of user
            new_password_hash (str): Hash of new password
            new_salt (str): Salt used for new password
            
        Returns:
            bool: True if password is reused (not allowed), False if unique
        """
        history = self.get_password_history(user_id)
        
        for old_hash, old_salt, _ in history:
            # Compare with stored hashes
            if new_password_hash == old_hash:
                print("🚨 Warning: This password was used before!")
                return True
        
        print("✅ This is a new password (not reused)")
        return False
    
    def get_user_by_username(self, username):
        """
        Get user information by username.
        
        Args:
            username (str): Username to search for
            
        Returns:
            tuple: (user_id, username, email, created_at) or None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, username, email, created_at
                FROM users
                WHERE username = ?
            ''', (username,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def delete_user(self, user_id):
        """
        Delete a user and their password history.
        
        Args:
            user_id (int): ID of user to delete
            
        Returns:
            bool: True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete password history first (foreign key)
            cursor.execute('DELETE FROM password_history WHERE user_id = ?', (user_id,))
            
            # Delete user
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            
            conn.commit()
            conn.close()
            
            print(f"✅ User {user_id} and their history deleted")
            return True
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def get_all_users(self):
        """
        Get list of all users (for admin purposes).
        
        Returns:
            list: List of (user_id, username, email, created_at) tuples
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT user_id, username, email, created_at FROM users')
            users = cursor.fetchall()
            conn.close()
            
            return users
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def get_password_stats(self):
        """
        Get statistics about stored passwords.
        
        Returns:
            dict: Statistics about users and passwords
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM users')
            total_users = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM password_history')
            total_passwords = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_users': total_users,
                'total_password_records': total_passwords,
                'avg_passwords_per_user': total_passwords / max(total_users, 1)
            }
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return {}


# Example usage (for testing)
if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MANAGER - Example Usage")
    print("=" * 60)
    
    # Initialize database
    db = DatabaseManager("test_passwords.db")
    
    # Create test user
    print("\n1️⃣  Creating users...")
    user_id = db.create_user("john_doe", "john@example.com")
    db.create_user("jane_smith", "jane@example.com")
    
    # Store password hashes
    print("\n2️⃣  Storing password hashes...")
    
    # Simulate storing different passwords
    hash1 = hashlib.sha256("MyPassword123".encode()).hexdigest()
    salt1 = os.urandom(16).hex()
    db.store_password_hash(user_id, hash1, salt1)
    
    # Simulate password change after some time
    hash2 = hashlib.sha256("NewPassword456!".encode()).hexdigest()
    salt2 = os.urandom(16).hex()
    db.store_password_hash(user_id, hash2, salt2)
    
    # Check password reuse
    print("\n3️⃣  Checking password reuse prevention...")
    hash3 = hashlib.sha256("MyPassword123".encode()).hexdigest()
    db.check_password_reuse(user_id, hash3, salt1)
    
    # View password history
    print("\n4️⃣  Password history for user:")
    history = db.get_password_history(user_id)
    for i, (hash_val, salt, timestamp) in enumerate(history, 1):
        print(f"  {i}. Changed at: {timestamp}")
        print(f"     Hash: {hash_val[:20]}... (truncated)")
    
    # Get all users
    print("\n5️⃣  All users in system:")
    users = db.get_all_users()
    for user_id, username, email, created in users:
        print(f"  - {username} ({email}) - Created: {created}")
    
    # Get statistics
    print("\n6️⃣  Database Statistics:")
    stats = db.get_password_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ Database example complete!")
    print("=" * 60)
