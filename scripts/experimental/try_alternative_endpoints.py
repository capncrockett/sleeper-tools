"""Try alternative API endpoints for mock drafts"""

import os
import requests
from dotenv import load_dotenv
from sleeper_api import get_user

def try_alternative_endpoints():
    """Try various API endpoints that might contain mock drafts."""
    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    
    if not username:
        print("SLEEPER_USERNAME not found in .env file")
        return
    
    try:
        user = get_user(username)
        user_id = user['user_id']
        print(f"User: {username} (ID: {user_id})")
        
        base_url = "https://api.sleeper.app/v1"
        
        # Try different variations of the drafts endpoint
        endpoints_to_try = [
            # Standard endpoint with different sports/seasons
            f"{base_url}/user/{user_id}/drafts/nfl/2025",
            f"{base_url}/user/{user_id}/drafts/mock/2025",
            f"{base_url}/user/{user_id}/drafts/practice/2025",
            
            # Try without season
            f"{base_url}/user/{user_id}/drafts/nfl",
            f"{base_url}/user/{user_id}/drafts",
            
            # Try mock-specific endpoints
            f"{base_url}/user/{user_id}/mock_drafts/nfl/2025",
            f"{base_url}/user/{user_id}/mock_drafts/2025",
            f"{base_url}/user/{user_id}/mock_drafts",
            
            # Try practice drafts
            f"{base_url}/user/{user_id}/practice_drafts/nfl/2025",
            f"{base_url}/user/{user_id}/practice_drafts/2025",
            f"{base_url}/user/{user_id}/practice_drafts",
            
            # Try different structures
            f"{base_url}/mock_drafts/user/{user_id}/nfl/2025",
            f"{base_url}/mock_drafts/user/{user_id}/2025",
            f"{base_url}/mock_drafts/user/{user_id}",
            
            # Try drafts without user prefix
            f"{base_url}/drafts/user/{user_id}/nfl/2025",
            f"{base_url}/drafts/user/{user_id}/2025",
            
            # Try with different seasons in case mock drafts use different season logic
            f"{base_url}/user/{user_id}/drafts/nfl/2024",
            f"{base_url}/user/{user_id}/drafts/nfl/2026",
        ]
        
        results = []
        
        for endpoint in endpoints_to_try:
            try:
                print(f"Trying: {endpoint}")
                response = requests.get(endpoint)
                
                if response.status_code == 200:
                    data = response.json()
                    if data:  # Not empty
                        print(f"  ✅ SUCCESS! Found data: {len(data) if isinstance(data, list) else 1} items")
                        results.append({
                            'endpoint': endpoint,
                            'data': data,
                            'count': len(data) if isinstance(data, list) else 1
                        })
                        
                        # Show first few items
                        items_to_show = data[:3] if isinstance(data, list) else [data]
                        for item in items_to_show:
                            if isinstance(item, dict):
                                draft_id = item.get('draft_id', 'No ID')
                                league_id = item.get('league_id', 'No League')
                                status = item.get('status', 'No Status')
                                draft_type = item.get('type', 'No Type')
                                print(f"    - {draft_id} | {status} | {draft_type} | League: {league_id}")
                    else:
                        print(f"  Empty response")
                elif response.status_code == 404:
                    print(f"  404 - Endpoint not found")
                else:
                    print(f"  {response.status_code} - {response.reason}")
                    
            except Exception as e:
                print(f"  Error: {e}")
        
        print(f"\n{'='*60}")
        print(f"SUMMARY:")
        print(f"Successful endpoints: {len(results)}")
        
        for result in results:
            print(f"\n✅ {result['endpoint']}")
            print(f"   Found {result['count']} items")
            
            # Look for potential mock drafts
            data = result['data']
            items = data if isinstance(data, list) else [data]
            
            mock_candidates = []
            for item in items:
                if isinstance(item, dict):
                    league_id = item.get('league_id')
                    if league_id is None or league_id == "null":
                        mock_candidates.append(item)
            
            if mock_candidates:
                print(f"   🎯 {len(mock_candidates)} potential mock drafts (no league_id)")
                for mock in mock_candidates:
                    print(f"      - {mock.get('draft_id', 'No ID')} | {mock.get('status', 'No Status')}")
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    try_alternative_endpoints()
