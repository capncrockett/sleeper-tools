"""Test script to verify the mock draft ADP system is ready"""

import os
from dotenv import load_dotenv
from mock_draft_tracker import MockDraftTracker

def test_system_readiness():
    """Test that all components are working and ready for mock draft data."""
    print("=== Testing Mock Draft ADP System Readiness ===\n")
    
    # Test 1: Environment setup
    print("1. Testing environment setup...")
    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    if username:
        print(f"   ✅ Username found: {username}")
    else:
        print("   ❌ SLEEPER_USERNAME not found in .env")
        return False
    
    # Test 2: Mock Draft Tracker
    print("\n2. Testing Mock Draft Tracker...")
    try:
        tracker = MockDraftTracker("test_mock_drafts.json")
        print("   ✅ MockDraftTracker initialized successfully")
    except Exception as e:
        print(f"   ❌ Error initializing tracker: {e}")
        return False
    
    # Test 3: Sleeper API connectivity
    print("\n3. Testing Sleeper API connectivity...")
    try:
        from sleeper_api import get_user
        user = get_user(username)
        if user and 'user_id' in user:
            print(f"   ✅ Sleeper API working - User ID: {user['user_id']}")
        else:
            print("   ❌ Could not fetch user from Sleeper API")
            return False
    except Exception as e:
        print(f"   ❌ Sleeper API error: {e}")
        return False
    
    # Test 4: Import system
    print("\n4. Testing import system...")
    try:
        from sleeper_mock_importer import SleeperMockImporter
        importer = SleeperMockImporter()
        print("   ✅ SleeperMockImporter ready")
    except Exception as e:
        print(f"   ❌ Import system error: {e}")
        return False
    
    # Test 5: File permissions
    print("\n5. Testing file permissions...")
    try:
        # Test write permissions
        test_file = "test_permissions.txt"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("   ✅ File write permissions working")
    except Exception as e:
        print(f"   ❌ File permission error: {e}")
        return False
    
    # Clean up test file if it exists
    if os.path.exists("test_mock_drafts.json"):
        os.remove("test_mock_drafts.json")
    
    print("\n" + "="*50)
    print("🎉 SYSTEM READY FOR MOCK DRAFTS! 🎉")
    print("="*50)
    print("\nNext Steps:")
    print("1. Go to Sleeper and run mock drafts")
    print("2. Use: python3 find_mock_drafts_only.py")
    print("3. Import your mock draft data")
    print("4. Generate custom keeper league ADP")
    print("\nYour custom ADP system is fully operational!")
    
    return True

if __name__ == "__main__":
    test_system_readiness()
