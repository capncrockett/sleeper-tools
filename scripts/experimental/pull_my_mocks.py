"""Quick script to pull your mock draft data from Sleeper"""

import os
from dotenv import load_dotenv
from sleeper_mock_importer import SleeperMockImporter
from datetime import datetime

def pull_user_mocks():
    """Pull mock drafts for the user."""
    # Load environment variables
    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    
    importer = SleeperMockImporter()
    
    print("=== Pulling Your Mock Draft Data ===\n")
    
    if not username:
        print("SLEEPER_USERNAME not found in .env file")
        username = input("Enter your Sleeper username: ").strip()
        if not username:
            print("Username required to find your drafts.")
            return
    
    print(f"Using username: {username}")
    
    try:
        # Find recent drafts
        print(f"\nSearching for recent mock drafts for {username}...")
        recent_drafts = importer.find_recent_drafts(username, 2024)
        
        if not recent_drafts:
            print("No recent drafts found in the last 7 days.")
            print("You may need to:")
            print("1. Run some mock drafts on Sleeper first")
            print("2. Check that your username is correct")
            print("3. Make sure the drafts are from 2024")
            return
        
        print(f"\nFound {len(recent_drafts)} recent drafts:")
        print("-" * 80)
        for i, draft in enumerate(recent_drafts, 1):
            status_emoji = "✅" if draft['status'] == 'complete' else "⏳"
            print(f"{i:2}. {status_emoji} {draft['draft_id']}")
            print(f"    Date: {draft['created'].strftime('%Y-%m-%d %H:%M')}")
            print(f"    Status: {draft['status']} | Type: {draft['type']} | Days ago: {draft['days_ago']}")
            print()
        
        # Let user select which drafts to import
        print("Which drafts would you like to import?")
        print("Enter numbers separated by commas (e.g., 1,3,5) or 'all' for all drafts:")
        selection = input("Selection: ").strip().lower()
        
        if selection == 'all':
            selected_indices = list(range(len(recent_drafts)))
        else:
            try:
                selected_indices = [int(x.strip()) - 1 for x in selection.split(',')]
                selected_indices = [i for i in selected_indices if 0 <= i < len(recent_drafts)]
            except ValueError:
                print("Invalid selection format.")
                return
        
        if not selected_indices:
            print("No valid drafts selected.")
            return
        
        # Get keepers info once
        print(f"\nBefore importing, let's set up your keeper information.")
        print("Enter the players that are keepers in your league (one per line, empty line to finish):")
        keepers = []
        while True:
            keeper = input("Keeper: ").strip()
            if not keeper:
                break
            keepers.append(keeper)
        
        print(f"\nKeepers set: {keepers}")
        
        # Import selected drafts
        imported_count = 0
        for idx in selected_indices:
            draft = recent_drafts[idx]
            try:
                print(f"\nImporting draft {draft['draft_id']}...")
                mock_draft = importer.import_draft_by_id(draft['draft_id'], keepers)
                importer.tracker.add_mock_draft(mock_draft)
                imported_count += 1
                print(f"✅ Successfully imported {len(mock_draft.picks)} picks")
            except Exception as e:
                print(f"❌ Error importing draft {draft['draft_id']}: {e}")
        
        print(f"\n=== Import Complete ===")
        print(f"Successfully imported {imported_count} mock drafts")
        
        # Show summary and export ADP
        if imported_count > 0:
            print("\n" + "="*50)
            importer.tracker.print_summary()
            
            # Calculate and show ADP
            adp_data = importer.tracker.calculate_adp()
            if adp_data:
                print(f"\n=== Top 20 Players by ADP ===")
                sorted_players = sorted(adp_data.values(), key=lambda x: x['average_pick'])[:20]
                print(f"{'Rank':<4} {'Player':<25} {'ADP':<6} {'Drafted':<8} {'Range'}")
                print("-" * 65)
                for i, player in enumerate(sorted_players, 1):
                    range_str = f"{player['earliest_pick']}-{player['latest_pick']}"
                    print(f"{i:<4} {player['player_name']:<25} {player['average_pick']:<6.1f} "
                          f"{player['times_drafted']:<8} {range_str}")
            
            # Export to CSV
            export_choice = input(f"\nExport ADP data to CSV? (y/n): ").strip().lower()
            if export_choice == 'y':
                filename = importer.tracker.export_adp_to_csv()
                print(f"✅ ADP data exported to: {filename}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your Sleeper username is correct and you have recent draft activity.")

if __name__ == "__main__":
    pull_user_mocks()
