"""Check the status and details of specific drafts"""

import os
from dotenv import load_dotenv
from sleeper_api import get_draft_picks
from datetime import datetime

def check_draft_status(draft_ids):
    """Check the status and pick count of specific drafts."""
    load_dotenv()
    
    print("=== Checking Draft Status ===\n")
    
    for draft_id in draft_ids:
        print(f"Checking draft: {draft_id}")
        try:
            picks = get_draft_picks(draft_id)
            
            if picks:
                print(f"  ✅ Draft has {len(picks)} picks")
                
                # Check if draft is complete (has picks in final rounds)
                if len(picks) > 100:  # Rough estimate for a complete draft
                    print(f"  ✅ Appears to be a complete draft")
                else:
                    print(f"  ⚠️  May be incomplete ({len(picks)} picks)")
                
                # Show first few picks
                print(f"  First few picks:")
                for i, pick in enumerate(picks[:5]):
                    player_id = pick.get('player_id', 'Unknown')
                    round_num = pick.get('round', '?')
                    pick_num = pick.get('pick_no', '?')
                    print(f"    {i+1}. Round {round_num}, Pick {pick_num} - Player ID: {player_id}")
                    
            else:
                print(f"  ❌ No picks found - draft may be incomplete or inaccessible")
                
        except Exception as e:
            print(f"  ❌ Error accessing draft: {e}")
        
        print()

if __name__ == "__main__":
    # Check the recent drafts we found
    recent_draft_ids = [
        "1254170833421619200",  # 11:59ers
        "1251950356196249600"   # Grundle
    ]
    
    check_draft_status(recent_draft_ids)
