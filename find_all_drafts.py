"""Find all drafts for the user with expanded search"""

import os
from dotenv import load_dotenv
from sleeper_api import get_user, get_all_drafts
from datetime import datetime

def find_all_user_drafts():
    """Find all drafts for the user with expanded timeframe."""
    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    
    if not username:
        print("SLEEPER_USERNAME not found in .env file")
        return
    
    print(f"=== Finding All Drafts for {username} ===\n")
    
    try:
        # Get user info
        user = get_user(username)
        user_id = user['user_id']
        print(f"User ID: {user_id}")
        
        # Check multiple seasons and expand timeframe
        seasons = [2024, 2023]
        all_drafts = []
        
        for season in seasons:
            print(f"\nChecking {season} season...")
            try:
                drafts = get_all_drafts(user_id, season)
                if drafts:
                    print(f"Found {len(drafts)} drafts in {season}")
                    for draft in drafts:
                        # Convert timestamp
                        draft_time = datetime.fromtimestamp(draft.get('created', 0) / 1000)
                        days_ago = (datetime.now() - draft_time).days
                        
                        draft_info = {
                            'draft_id': draft['draft_id'],
                            'created': draft_time,
                            'status': draft.get('status', 'unknown'),
                            'type': draft.get('type', 'unknown'),
                            'league_id': draft.get('league_id'),
                            'season': season,
                            'days_ago': days_ago
                        }
                        all_drafts.append(draft_info)
                else:
                    print(f"No drafts found in {season}")
            except Exception as e:
                print(f"Error checking {season}: {e}")
        
        if not all_drafts:
            print("\n❌ No drafts found in any season.")
            print("This could mean:")
            print("1. You haven't participated in any drafts on Sleeper")
            print("2. The username might be incorrect")
            print("3. There might be an API issue")
            return
        
        # Sort by date (most recent first)
        all_drafts.sort(key=lambda x: x['created'], reverse=True)
        
        print(f"\n=== Found {len(all_drafts)} Total Drafts ===")
        print("-" * 100)
        
        for i, draft in enumerate(all_drafts, 1):
            status_emoji = "✅" if draft['status'] == 'complete' else "⏳"
            type_emoji = "🏈" if 'mock' in draft['type'].lower() else "🏆"
            
            print(f"{i:2}. {status_emoji}{type_emoji} {draft['draft_id']}")
            print(f"    Date: {draft['created'].strftime('%Y-%m-%d %H:%M')} ({draft['days_ago']} days ago)")
            print(f"    Status: {draft['status']} | Type: {draft['type']} | Season: {draft['season']}")
            print(f"    League: {draft['league_id']}")
            print()
        
        # Filter for mock drafts specifically
        mock_drafts = [d for d in all_drafts if 'mock' in d['type'].lower()]
        if mock_drafts:
            print(f"\n🎯 Found {len(mock_drafts)} Mock Drafts:")
            for i, draft in enumerate(mock_drafts, 1):
                print(f"{i}. {draft['draft_id']} - {draft['created'].strftime('%Y-%m-%d')} ({draft['days_ago']} days ago)")
        
        # Filter for recent drafts (last 30 days instead of 7)
        recent_drafts = [d for d in all_drafts if d['days_ago'] <= 30]
        if recent_drafts:
            print(f"\n📅 Found {len(recent_drafts)} Recent Drafts (last 30 days):")
            for i, draft in enumerate(recent_drafts, 1):
                print(f"{i}. {draft['draft_id']} - {draft['created'].strftime('%Y-%m-%d')} ({draft['days_ago']} days ago) - {draft['type']}")
        
        return all_drafts
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    find_all_user_drafts()
