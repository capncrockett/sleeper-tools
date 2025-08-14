"""Find mock drafts from specific league (11:59ers)"""

import os
from dotenv import load_dotenv
from sleeper_api import get_user, get_all_leagues, get_all_drafts, get_draft_picks
from sleeper_mock_importer import SleeperMockImporter
from datetime import datetime

def find_league_mocks():
    """Find mock drafts from the 11:59ers league."""
    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    
    if not username:
        print("SLEEPER_USERNAME not found in .env file")
        return
    
    print(f"=== Finding 11:59ers League Mock Drafts ===\n")
    
    try:
        # Get user info
        user = get_user(username)
        user_id = user['user_id']
        print(f"User: {username} (ID: {user_id})")
        
        # Get all leagues for 2024
        print(f"\nFinding your 2024 leagues...")
        leagues = get_all_leagues(user_id, 2024)
        
        if not leagues:
            print("No leagues found for 2024")
            return
        
        print(f"Found {len(leagues)} leagues in 2024:")
        target_league_id = None
        
        for league in leagues:
            league_name = league.get('name', 'Unknown')
            league_id = league.get('league_id')
            print(f"  - {league_name} (ID: {league_id})")
            
            # Look for 11:59ers league (case insensitive)
            if '11:59' in league_name.lower() or 'eleven' in league_name.lower():
                target_league_id = league_id
                print(f"    ✅ Found 11:59ers league!")
        
        if not target_league_id:
            print(f"\n❌ Could not find 11:59ers league automatically.")
            print("Available leagues:")
            for i, league in enumerate(leagues, 1):
                print(f"{i}. {league.get('name', 'Unknown')} (ID: {league.get('league_id')})")
            
            choice = input(f"\nSelect league number (1-{len(leagues)}): ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(leagues):
                    target_league_id = leagues[idx]['league_id']
                    print(f"Selected: {leagues[idx].get('name', 'Unknown')}")
                else:
                    print("Invalid selection")
                    return
            except ValueError:
                print("Invalid input")
                return
        
        # Now find all drafts for this league
        print(f"\nSearching for drafts in league {target_league_id}...")
        
        # Get all user drafts and filter by league
        all_drafts = get_all_drafts(user_id, 2024)
        league_drafts = [d for d in all_drafts if d.get('league_id') == target_league_id]
        
        if not league_drafts:
            print("No drafts found for this league")
            return
        
        print(f"Found {len(league_drafts)} drafts in this league:")
        
        # Sort by date
        for draft in league_drafts:
            draft_time = datetime.fromtimestamp(draft.get('created', 0) / 1000)
            draft['created_dt'] = draft_time
            draft['days_ago'] = (datetime.now() - draft_time).days
        
        league_drafts.sort(key=lambda x: x['created_dt'], reverse=True)
        
        # Display drafts
        for i, draft in enumerate(league_drafts, 1):
            status_emoji = "✅" if draft['status'] == 'complete' else "⏳"
            type_info = draft.get('type', 'unknown')
            
            print(f"{i}. {status_emoji} {draft['draft_id']}")
            print(f"   Date: {draft['created_dt'].strftime('%Y-%m-%d %H:%M')} ({draft['days_ago']} days ago)")
            print(f"   Status: {draft['status']} | Type: {type_info}")
            print()
        
        # Let user select drafts to import
        print("Which drafts would you like to import for ADP analysis?")
        print("Enter numbers separated by commas (e.g., 1,2) or 'all' for all completed drafts:")
        selection = input("Selection: ").strip().lower()
        
        if selection == 'all':
            selected_drafts = [d for d in league_drafts if d['status'] == 'complete']
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                selected_drafts = [league_drafts[i] for i in indices if 0 <= i < len(league_drafts)]
            except (ValueError, IndexError):
                print("Invalid selection")
                return
        
        if not selected_drafts:
            print("No drafts selected")
            return
        
        # Get keeper information
        print(f"\nBefore importing {len(selected_drafts)} drafts, let's set up keepers.")
        print("Enter players that are keepers in the 11:59ers league (one per line, empty line to finish):")
        keepers = []
        while True:
            keeper = input("Keeper: ").strip()
            if not keeper:
                break
            keepers.append(keeper)
        
        print(f"Keepers for 11:59ers league: {keepers}")
        
        # Import selected drafts
        importer = SleeperMockImporter()
        imported_count = 0
        
        for draft in selected_drafts:
            try:
                print(f"\nImporting draft {draft['draft_id']} ({draft['created_dt'].strftime('%Y-%m-%d')})...")
                mock_draft = importer.import_draft_by_id(draft['draft_id'], keepers)
                
                # Add league info to notes
                mock_draft.notes = f"11:59ers League - {mock_draft.notes}"
                
                importer.tracker.add_mock_draft(mock_draft)
                imported_count += 1
                print(f"✅ Imported {len(mock_draft.picks)} picks")
                
            except Exception as e:
                print(f"❌ Error importing {draft['draft_id']}: {e}")
        
        if imported_count > 0:
            print(f"\n🎉 Successfully imported {imported_count} drafts from 11:59ers league!")
            
            # Show summary
            importer.tracker.print_summary()
            
            # Calculate and show ADP
            adp_data = importer.tracker.calculate_adp()
            if adp_data:
                print(f"\n=== 11:59ers League ADP (Top 20) ===")
                sorted_players = sorted(adp_data.values(), key=lambda x: x['average_pick'])[:20]
                print(f"{'Rank':<4} {'Player':<25} {'ADP':<6} {'Drafted':<8} {'Range'}")
                print("-" * 65)
                for i, player in enumerate(sorted_players, 1):
                    range_str = f"{player['earliest_pick']}-{player['latest_pick']}"
                    print(f"{i:<4} {player['player_name']:<25} {player['average_pick']:<6.1f} "
                          f"{player['times_drafted']:<8} {range_str}")
            
            # Export option
            export = input(f"\nExport 11:59ers ADP to CSV? (y/n): ").strip().lower()
            if export == 'y':
                filename = importer.tracker.export_adp_to_csv("eleveners_league_adp.csv")
                print(f"✅ Exported to: {filename}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_league_mocks()
