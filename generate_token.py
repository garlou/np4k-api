#!/usr/bin/env python3
"""
Utility script to generate secure API tokens
"""

import secrets
import string
import sys

def generate_token(length=32):
    """Generate a secure random token"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_hex_token(length=32):
    """Generate a secure random hex token"""
    return secrets.token_hex(length // 2)

def main():
    print("🔐 API Token Generator")
    print("=" * 30)

    # Generate different types of tokens
    print("1. Alphanumeric token (32 chars):")
    print(f"   {generate_token(32)}")
    print()

    print("2. Hex token (32 chars):")
    print(f"   {generate_hex_token(32)}")
    print()

    print("3. Long hex token (64 chars):")
    print(f"   {generate_hex_token(64)}")
    print()

    print("📝 Usage:")
    print("   Copy one of the tokens above and update your docker-compose.yml:")
    print("   environment:")
    print("     - API_TOKEN=your-generated-token-here")
    print()
    print("   Or set it as an environment variable:")
    print("   export API_TOKEN=your-generated-token-here")

if __name__ == "__main__":
    main()