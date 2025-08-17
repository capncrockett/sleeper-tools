"""Comprehensive search for ALL 2025 drafts including mock drafts"""

import os
from dotenv import load_dotenv
from sleeper_api import get_user, get_all_leagues, get_all_drafts
from datetime import datetime
import requests

def find_all_2025_drafts():
    """Find ALL 2025 drafts - both league and mock drafts."""
    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    
    if not username:
        print("SLEEPER_USERNAME not found in .env file")
        return
    
    print(f"=== Finding ALL 2025 Drafts for {username} ===\n")
    
    try:
        # Get user info
        user = get_user(username)
        user_id = user['user_id']
        print(f"User: {username} (ID: {user_id})")
        
        # Method 1: Get all user drafts for 2025
        print(f"\n1. Checking user drafts for 2025...")
        try:
            user_drafts = get_all_drafts(user_id, 2025)
            print(f"   Found {len(user_drafts) if user_drafts else 0} drafts via user endpoint")
            
            if user_drafts:
                for draft in user_drafts:
                    draft_time = datetime.fromtimestamp(draft.get('created', 0) / 1000)
                    print(f"   - {draft['draft_id']} | {draft_time.strftime('%Y-%m-%d %H:%M')} | {draft.get('type', 'unknown')} | League: {draft.get('league_id', 'None')}")
        except Exception as e:
            print(f"   Error: {e}")
            user_drafts = []
        
        # Method 2: Get all leagues and check their drafts
        print(f"\n2. Checking league-based drafts for 2025...")
        try:
            leagues = get_all_leagues(user_id, 2025)
            print(f"   Found {len(leagues) if leagues else 0} leagues")
            
            league_drafts = []
            if leagues:
                for league in leagues:
                    league_name = league.get('name', 'Unknown')
                    league_id = league.get('league_id')
                    print(f"   League: {league_name} (ID: {league_id})")
                    
                    # Try to get drafts for this league
                    # Note: Sleeper API doesn't have a direct league->drafts endpoint
                    # We need to filter user drafts by league_id
                    if user_drafts:
                        league_specific_drafts = [d for d in user_drafts if d.get('league_id') == league_id]
                        if league_specific_drafts:
                            print(f"     Found {len(league_specific_drafts)} drafts in this league")
                            for draft in league_specific_drafts:
                                draft_time = datetime.fromtimestamp(draft.get('created', 0) / 1000)
                                print(f"     - {draft['draft_id']} | {draft_time.strftime('%Y-%m-%d %H:%M')} | {draft.get('type', 'unknown')}")
                        else:
                            print(f"     No drafts found in this league")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Method 3: Try direct API call to mock draft endpoint (if it exists)
        print(f"\n3. Checking for mock draft specific endpoints...")
        try:
            # Try a few different mock draft endpoints
            base_url = "https://api.sleeper.app/v1"
            mock_endpoints = [
                f"{base_url}/user/{user_id}/mock_drafts/nfl/2025",
                f"{base_url}/user/{user_id}/practice_drafts/nfl/2025",
                f"{base_url}/mock_drafts/user/{user_id}/2025"
            ]
            
            mock_drafts_found = []
            for endpoint in mock_endpoints:
                try:
                    response = requests.get(endpoint)
                    if response.status_code == 200:
                        data = response.json()
                        if data:
                            print(f"   ✅ Found data at: {endpoint}")
                            mock_drafts_found.extend(data if isinstance(data, list) else [data])
                        else:
                            print(f"   Empty response from: {endpoint}")
                    else:
                        print(f"   No data at: {endpoint} (Status: {response.status_code})")
                except Exception as e:
                    print(f"   Error checking {endpoint}: {e}")
            
            if mock_drafts_found:
                print(f"   Found {len(mock_drafts_found)} mock drafts via direct endpoints")
            else:
                print(f"   No mock drafts found via direct endpoints")
                
        except Exception as e:
            print(f"   Error checking mock endpoints: {e}")
        
        # Method 4: Check recent activity (last 30 days)
        print(f"\n4. Filtering for recent drafts (last 30 days)...")
        all_drafts = user_drafts or []
        recent_drafts = []
        
        for draft in all_drafts:
            draft_time = datetime.fromtimestamp(draft.get('created', 0) / 1000)
            days_ago = (datetime.now() - draft_time).days
            
            if days_ago <= 30:  # Last 30 days
                recent_drafts.append({
                    'draft_id': draft['draft_id'],
                    'created': draft_time,
                    'status': draft.get('status', 'unknown'),
                    'type': draft.get('type', 'unknown'),
                    'league_id': draft.get('league_id', 'None'),
                    'days_ago': days_ago
                })
        
        if recent_drafts:
            print(f"   Found {len(recent_drafts)} recent drafts:")
            for draft in sorted(recent_drafts, key=lambda x: x['created'], reverse=True):
                status_emoji = "✅" if draft['status'] == 'complete' else "⏳"
                print(f"   {status_emoji} {draft['draft_id']} | {draft['created'].strftime('%Y-%m-%d %H:%M')} | {draft['type']} | League: {draft['league_id']} | {draft['days_ago']} days ago")
        else:
            print(f"   No recent drafts found")
        
        # Summary and recommendations
        print(f"\n{'='*80}")
        print(f"SUMMARY:")
        print(f"- Total 2025 drafts found: {len(all_drafts)}")
        print(f"- Recent drafts (30 days): {len(recent_drafts)}")
        
        if recent_drafts:
            print(f"\nRECOMMENDATION:")
            print(f"Your recent drafts are listed above. If these include your 5 mock drafts,")
            print(f"you can import them using their Draft IDs with:")
            print(f"python3 import_by_draft_id.py")
            
            print(f"\nRecent Draft IDs:")
            for draft in recent_drafts:
                print(f"  {draft['draft_id']}")
        else:
            print(f"\nNo recent drafts found. This suggests:")
            print(f"1. Mock drafts might not be accessible via the API")
            print(f"2. You might need to manually get Draft IDs from Sleeper app")
            print(f"3. Mock drafts might be stored in a different system")
        
        return recent_drafts
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    find_all_2025_drafts()
