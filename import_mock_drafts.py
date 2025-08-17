"""Import the specific mock drafts provided by user"""

import os
from dotenv import load_dotenv
from sleeper_mock_importer import SleeperMockImporter

def import_specific_mocks():
    """Import the 5 specific mock drafts."""
    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    
    # The 5 mock draft IDs from the URLs
    draft_ids = [
        "1261756291928313856",
        "1261753158875500544", 
        "1261750771418943488",
        "1261743236129501184",
        "1261474618305167360"
    ]
    
    print("=== Importing 5 Mock Drafts for 11:59ers League ===\n")
    print(f"User: {username}")
    print(f"Mock Draft IDs:")
    for i, draft_id in enumerate(draft_ids, 1):
        print(f"{i}. {draft_id}")
    
    # Set up keepers (can be empty for now)
    print(f"\nSetting up keepers for 11:59ers league...")
    print("Enter keeper players (one per line, empty line to finish):")
    keepers = []
    while True:
        keeper = input("Keeper: ").strip()
        if not keeper:
            break
        keepers.append(keeper)
    
    print(f"Keepers: {keepers if keepers else 'None'}")
    
    # Import each mock draft
    importer = SleeperMockImporter()
    imported_count = 0
    failed_imports = []
    
    for i, draft_id in enumerate(draft_ids, 1):
        try:
            print(f"\nImporting mock draft {i}/5: {draft_id}...")
            mock_draft = importer.import_draft_by_id(draft_id, keepers)
            
            # Add mock draft info to notes
            mock_draft.notes = f"11:59ers Mock Draft #{i} - 2025 Season"
            
            importer.tracker.add_mock_draft(mock_draft)
            imported_count += 1
            print(f"✅ Successfully imported {len(mock_draft.picks)} picks")
            
        except Exception as e:
            print(f"❌ Error importing {draft_id}: {e}")
            failed_imports.append(draft_id)
    
    # Show results
    print(f"\n{'='*60}")
    print(f"IMPORT RESULTS:")
    print(f"✅ Successfully imported: {imported_count}/5 mock drafts")
    if failed_imports:
        print(f"❌ Failed imports: {len(failed_imports)}")
        for draft_id in failed_imports:
            print(f"   - {draft_id}")
    
    if imported_count > 0:
        # Show summary
        print(f"\n{'='*60}")
        importer.tracker.print_summary()
        
        # Calculate and show ADP
        adp_data = importer.tracker.calculate_adp()
        if adp_data:
            print(f"\n=== 11:59ers Mock Draft ADP (Top 30) ===")
            sorted_players = sorted(adp_data.values(), key=lambda x: x['average_pick'])[:30]
            print(f"{'Rank':<4} {'Player':<25} {'ADP':<6} {'Times':<6} {'%':<6} {'Range':<10} {'StdDev'}")
            print("-" * 75)
            for i, player in enumerate(sorted_players, 1):
                range_str = f"{player['earliest_pick']}-{player['latest_pick']}"
                pct_str = f"{player['draft_percentage']:.0f}%"
                print(f"{i:<4} {player['player_name']:<25} {player['average_pick']:<6.1f} "
                      f"{player['times_drafted']:<6} {pct_str:<6} {range_str:<10} {player['std_dev']}")
        
        # Export to CSV
        print(f"\n{'='*60}")
        filename = importer.tracker.export_adp_to_csv("eleveners_2025_mock_adp.csv")
        print(f"✅ Exported custom ADP to: {filename}")
        print(f"\n🎉 Your 11:59ers keeper league ADP is ready!")
        print(f"Use this CSV for draft day reference.")
    
    return imported_count

if __name__ == "__main__":
    import_specific_mocks()
