#!/usr/bin/env python3
"""Generate a secure secret key for JobSift"""

import secrets
import string
import sys
import os

def generate_secret_key(length=32):
    """Generate a secure random string"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def update_env_file(secret_key, env_file_path='backend/.env'):
    """Update the .env file with the new secret key"""
    try:
        with open(env_file_path, 'r') as f:
            content = f.read()
        
        # Replace the placeholder
        updated_content = content.replace(
            'your-super-secret-key-here-minimum-32-characters-long',
            secret_key
        )
        
        with open(env_file_path, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Secret key updated in {env_file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating secret key: {e}")
        return False

if __name__ == "__main__":
    secret_key = generate_secret_key()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--print":
        print(secret_key)
    else:
        if update_env_file(secret_key):
            print(f"Generated secret key: {secret_key[:8]}...")
        else:
            sys.exit(1)
