"""Thorough search for mock drafts based on API documentation"""

import os
from dotenv import load_dotenv
from sleeper_api import get_user, get_all_drafts
from datetime import datetime
import requests

def find_mock_drafts_thorough():
    """Thorough search for mock drafts using all available methods."""
    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    
    if not username:
        print("SLEEPER_USERNAME not found in .env file")
        return
    
    print(f"=== Thorough Mock Draft Search for {username} ===\n")
    
    try:
        # Get user info
        user = get_user(username)
        user_id = user['user_id']
        print(f"User: {username} (ID: {user_id})")
        
        # Search 2025 season thoroughly
        season = 2025
        print(f"\nSearching {season} season for ALL drafts...")
        
        try:
            all_drafts = get_all_drafts(user_id, season)
            print(f"Found {len(all_drafts) if all_drafts else 0} total drafts")
            
            if not all_drafts:
                print("No drafts found at all for 2025")
                return []
            
            # Analyze each draft in detail
            mock_drafts = []
            league_drafts = []
            
            for draft in all_drafts:
                draft_time = datetime.fromtimestamp(draft.get('created', 0) / 1000)
                league_id = draft.get('league_id')
                draft_type = draft.get('type', 'unknown')
                status = draft.get('status', 'unknown')
                
                draft_info = {
                    'draft_id': draft['draft_id'],
                    'created': draft_time,
                    'status': status,
                    'type': draft_type,
                    'league_id': league_id,
                    'days_ago': (datetime.now() - draft_time).days,
                    'metadata': draft.get('metadata', {}),
                    'settings': draft.get('settings', {})
                }
                
                # Classify as mock or league draft
                if league_id is None or league_id == "null":
                    mock_drafts.append(draft_info)
                    print(f"  MOCK: {draft['draft_id']} | {draft_time.strftime('%Y-%m-%d %H:%M')} | {status} | {draft_type}")
                else:
                    league_drafts.append(draft_info)
                    print(f"  LEAGUE: {draft['draft_id']} | {draft_time.strftime('%Y-%m-%d %H:%M')} | {status} | {draft_type} | League: {league_id}")
            
            print(f"\nSUMMARY:")
            print(f"  Mock drafts found: {len(mock_drafts)}")
            print(f"  League drafts found: {len(league_drafts)}")
            
            if mock_drafts:
                print(f"\n=== MOCK DRAFTS ===")
                for i, draft in enumerate(mock_drafts, 1):
                    status_emoji = "✅" if draft['status'] == 'complete' else "⏳"
                    print(f"{i}. {status_emoji} {draft['draft_id']}")
                    print(f"   Date: {draft['created'].strftime('%Y-%m-%d %H:%M')} ({draft['days_ago']} days ago)")
                    print(f"   Status: {draft['status']} | Type: {draft['type']}")
                    
                    # Show metadata if available
                    metadata = draft.get('metadata', {})
                    if metadata:
                        name = metadata.get('name', 'Unnamed')
                        print(f"   Name: {name}")
                    
                    print()
                
                return mock_drafts
            else:
                print(f"\n❌ No mock drafts found")
                print(f"All {len(league_drafts)} drafts are associated with leagues")
                
                # Maybe mock drafts are stored differently - let's check if any have specific indicators
                print(f"\nChecking for other mock draft indicators...")
                possible_mocks = []
                
                for draft in league_drafts:
                    metadata = draft.get('metadata', {})
                    name = metadata.get('name', '').lower()
                    
                    # Look for mock indicators in name or metadata
                    if any(keyword in name for keyword in ['mock', 'practice', 'test']):
                        possible_mocks.append(draft)
                        print(f"  Possible mock: {draft['draft_id']} - {metadata.get('name', 'Unnamed')}")
                
                if possible_mocks:
                    print(f"\nFound {len(possible_mocks)} possible mock drafts based on name")
                    return possible_mocks
                else:
                    print(f"No obvious mock draft indicators found")
                    return []
                
        except Exception as e:
            print(f"Error searching drafts: {e}")
            return []
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    mock_drafts = find_mock_drafts_thorough()
    
    if mock_drafts:
        print(f"\n🎉 Found {len(mock_drafts)} mock drafts!")
        print(f"You can import these using their Draft IDs:")
        for draft in mock_drafts:
            print(f"  {draft['draft_id']}")
    else:
        print(f"\n❌ No mock drafts found through API")
        print(f"You may need to manually get Draft IDs from Sleeper interface")
