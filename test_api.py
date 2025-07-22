#!/usr/bin/env python3
"""
Test script for the Article Parser API
"""

import requests
import json
import sys
import time

# Configuration
API_BASE = "http://localhost:3002"
TOKEN = "your-secure-token-here"  # Change this to match your token
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_single_parse():
    """Test parsing a single article"""
    print("\n📰 Testing single article parsing...")

    # Test with a sample news article
    test_url = "https://www.bbc.com/news/world-us-canada-12345678"

    try:
        response = requests.post(
            f"{API_BASE}/parse",
            headers=HEADERS,
            json={"url": test_url},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                article = data['article']
                print("✅ Single article parsing successful")
                print(f"   Title: {article.get('title', 'N/A')}")
                print(f"   Text length: {len(article.get('text', ''))} characters")
                print(f"   Authors: {article.get('authors', [])}")
                print(f"   Keywords: {article.get('keywords', [])[:5]}...")  # Show first 5 keywords
            else:
                print(f"❌ Parsing failed: {data.get('error')}")
        elif response.status_code == 401:
            print("❌ Authentication failed - check your API token")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_batch_parse():
    """Test parsing multiple articles"""
    print("\n📊 Testing batch article parsing...")

    # Test with multiple URLs
    test_urls = [
        "https://www.bbc.com/news/world-us-canada-12345678",
        "https://www.bbc.com/news/technology-12345678"
    ]

    try:
        response = requests.post(
            f"{API_BASE}/parse/batch",
            headers=HEADERS,
            json={"urls": test_urls},
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                results = data['results']
                print(f"✅ Batch parsing completed: {len(results)} articles processed")

                for i, result in enumerate(results):
                    if result.get('success'):
                        print(f"   Article {i+1}: {result.get('title', 'N/A')}")
                    else:
                        print(f"   Article {i+1}: Failed - {result.get('error')}")
            else:
                print(f"❌ Batch parsing failed: {data.get('error')}")
        elif response.status_code == 401:
            print("❌ Authentication failed - check your API token")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_authentication():
    """Test authentication with invalid token"""
    print("\n🔐 Testing authentication...")

    # Test with invalid token
    invalid_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer invalid-token"
    }

    try:
        response = requests.post(
            f"{API_BASE}/parse",
            headers=invalid_headers,
            json={"url": "https://example.com"},
            timeout=10
        )

        if response.status_code == 401:
            print("✅ Authentication correctly rejected invalid token")
        else:
            print(f"❌ Authentication test failed: expected 401, got {response.status_code}")

    except Exception as e:
        print(f"❌ Authentication test error: {e}")

def test_missing_token():
    """Test request without token"""
    print("\n🚫 Testing request without token...")

    headers_no_token = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            f"{API_BASE}/parse",
            headers=headers_no_token,
            json={"url": "https://example.com"},
            timeout=10
        )

        if response.status_code == 401:
            print("✅ Correctly rejected request without token")
        else:
            print(f"❌ Missing token test failed: expected 401, got {response.status_code}")

    except Exception as e:
        print(f"❌ Missing token test error: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Article Parser API Tests")
    print("=" * 50)

    # Check if API is running
    if not test_health():
        print("\n❌ API is not running. Please start the API first:")
        print("   docker-compose up --build")
        sys.exit(1)

    # Run tests
    test_authentication()
    test_missing_token()
    test_single_parse()
    test_batch_parse()

    print("\n" + "=" * 50)
    print("✅ All tests completed!")

if __name__ == "__main__":
    main()