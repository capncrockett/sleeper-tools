"""Find ONLY mock drafts (not real league drafts)"""

import os
from dotenv import load_dotenv
from sleeper_api import get_user, get_all_drafts, get_draft_picks
from sleeper_mock_importer import SleeperMockImporter
from datetime import datetime
import requests

def find_mock_drafts_only():
    """Find only mock drafts, excluding all real league drafts."""
    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    
    if not username:
        print("SLEEPER_USERNAME not found in .env file")
        return
    
    print(f"=== Finding MOCK DRAFTS ONLY for {username} ===\n")
    
    try:
        # Get user info
        user = get_user(username)
        user_id = user['user_id']
        print(f"User: {username} (ID: {user_id})")
        
        # Search multiple seasons for mock drafts
        seasons = [2025, 2024, 2023]
        all_mock_drafts = []
        
        for season in seasons:
            print(f"\nSearching {season} season for mock drafts...")
            try:
                drafts = get_all_drafts(user_id, season)
                if not drafts:
                    print(f"  No drafts found in {season}")
                    continue
                
                # Filter for mock drafts only
                mock_drafts = []
                for draft in drafts:
                    draft_type = draft.get('type', '').lower()
                    draft_status = draft.get('status', '').lower()
                    
                    # Look for mock draft indicators
                    is_mock = (
                        'mock' in draft_type or
                        draft.get('league_id') is None or  # Mock drafts often have no league_id
                        'practice' in draft_type
                    )
                    
                    if is_mock:
                        draft_time = datetime.fromtimestamp(draft.get('created', 0) / 1000)
                        mock_info = {
                            'draft_id': draft['draft_id'],
                            'created': draft_time,
                            'status': draft_status,
                            'type': draft_type,
                            'season': season,
                            'days_ago': (datetime.now() - draft_time).days,
                            'league_id': draft.get('league_id', 'None')
                        }
                        mock_drafts.append(mock_info)
                
                if mock_drafts:
                    print(f"  Found {len(mock_drafts)} mock drafts in {season}")
                    all_mock_drafts.extend(mock_drafts)
                else:
                    print(f"  No mock drafts found in {season}")
                    
            except Exception as e:
                print(f"  Error searching {season}: {e}")
        
        if not all_mock_drafts:
            print(f"\n❌ No mock drafts found for {username}")
            print("\nThis could mean:")
            print("1. You haven't run any mock drafts on Sleeper yet")
            print("2. Mock drafts might be stored differently in Sleeper's API")
            print("3. You might need to run some mock drafts first")
            print("\nTo run mock drafts on Sleeper:")
            print("- Go to Sleeper app/website")
            print("- Look for 'Mock Draft' or 'Practice Draft' option")
            print("- Run a few mock drafts")
            print("- Then re-run this script")
            return []
        
        # Sort by date (most recent first)
        all_mock_drafts.sort(key=lambda x: x['created'], reverse=True)
        
        print(f"\n=== Found {len(all_mock_drafts)} Mock Drafts ===")
        print("-" * 90)
        
        for i, draft in enumerate(all_mock_drafts, 1):
            status_emoji = "✅" if draft['status'] == 'complete' else "⏳"
            
            print(f"{i:2}. {status_emoji} {draft['draft_id']}")
            print(f"    Date: {draft['created'].strftime('%Y-%m-%d %H:%M')} ({draft['days_ago']} days ago)")
            print(f"    Status: {draft['status']} | Type: {draft['type']} | Season: {draft['season']}")
            print(f"    League ID: {draft['league_id']}")
            print()
        
        # Filter for completed mock drafts
        completed_mocks = [d for d in all_mock_drafts if d['status'] == 'complete']
        
        if not completed_mocks:
            print("❌ No completed mock drafts found")
            print("You need to complete some mock drafts first before we can analyze ADP")
            return []
        
        print(f"✅ Found {len(completed_mocks)} completed mock drafts")
        
        # Let user select which mock drafts to import
        print("\nWhich mock drafts would you like to import for ADP analysis?")
        print("Enter numbers separated by commas (e.g., 1,3,5) or 'all' for all completed:")
        selection = input("Selection: ").strip().lower()
        
        if selection == 'all':
            selected_drafts = completed_mocks
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                selected_drafts = [all_mock_drafts[i] for i in indices if 0 <= i < len(all_mock_drafts)]
                # Only keep completed drafts
                selected_drafts = [d for d in selected_drafts if d['status'] == 'complete']
            except (ValueError, IndexError):
                print("Invalid selection")
                return []
        
        if not selected_drafts:
            print("No valid completed mock drafts selected")
            return []
        
        # Get keeper information
        print(f"\nBefore importing {len(selected_drafts)} mock drafts, let's set up keepers.")
        print("Enter players that will be keepers in your upcoming draft (one per line, empty line to finish):")
        print("(These are players that won't be available in the draft pool)")
        keepers = []
        while True:
            keeper = input("Keeper: ").strip()
            if not keeper:
                break
            keepers.append(keeper)
        
        print(f"Keepers set: {keepers}")
        
        # Import selected mock drafts
        importer = SleeperMockImporter()
        imported_count = 0
        
        for draft in selected_drafts:
            try:
                print(f"\nImporting mock draft {draft['draft_id']} ({draft['created'].strftime('%Y-%m-%d')})...")
                mock_draft = importer.import_draft_by_id(draft['draft_id'], keepers)
                
                # Add mock draft info to notes
                mock_draft.notes = f"Mock Draft - Season {draft['season']} - {mock_draft.notes}"
                
                importer.tracker.add_mock_draft(mock_draft)
                imported_count += 1
                print(f"✅ Imported {len(mock_draft.picks)} picks")
                
            except Exception as e:
                print(f"❌ Error importing {draft['draft_id']}: {e}")
        
        if imported_count > 0:
            print(f"\n🎉 Successfully imported {imported_count} mock drafts!")
            
            # Show summary
            importer.tracker.print_summary()
            
            # Calculate and show ADP
            adp_data = importer.tracker.calculate_adp()
            if adp_data:
                print(f"\n=== Mock Draft ADP Analysis (Top 25) ===")
                sorted_players = sorted(adp_data.values(), key=lambda x: x['average_pick'])[:25]
                print(f"{'Rank':<4} {'Player':<25} {'ADP':<6} {'Times':<6} {'%':<6} {'Range':<10} {'StdDev'}")
                print("-" * 75)
                for i, player in enumerate(sorted_players, 1):
                    range_str = f"{player['earliest_pick']}-{player['latest_pick']}"
                    pct_str = f"{player['draft_percentage']:.0f}%"
                    print(f"{i:<4} {player['player_name']:<25} {player['average_pick']:<6.1f} "
                          f"{player['times_drafted']:<6} {pct_str:<6} {range_str:<10} {player['std_dev']}")
            
            # Export option
            export = input(f"\nExport mock draft ADP to CSV? (y/n): ").strip().lower()
            if export == 'y':
                filename = importer.tracker.export_adp_to_csv("mock_draft_adp.csv")
                print(f"✅ Exported to: {filename}")
        
        return selected_drafts
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    find_mock_drafts_only()
