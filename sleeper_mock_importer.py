"""Sleeper Mock Draft Importer

This utility helps import mock draft data from Sleeper API into the Mock Draft Tracker.
Since Sleeper API can't start mocks automatically, this helps you quickly import
the results after you manually run mock drafts.
"""

from datetime import datetime
from typing import List, Optional
from mock_draft_tracker import MockDraft, DraftPick, MockDraftTracker
from sleeper_api import get_draft_picks, get_all_players, get_user, get_all_drafts

class SleeperMockImporter:
    """Import mock drafts from Sleeper API."""
    
    def __init__(self):
        self.all_players = None
        self.tracker = MockDraftTracker()
    
    def load_players(self):
        """Load all NFL players from Sleeper API."""
        if self.all_players is None:
            print("Loading NFL players from Sleeper API...")
            self.all_players = get_all_players()
            print(f"Loaded {len(self.all_players)} players")
    
    def get_player_name(self, player_id: str) -> str:
        """Get formatted player name from player ID."""
        if not self.all_players:
            self.load_players()
        
        if player_id in self.all_players:
            player = self.all_players[player_id]
            first_name = player.get('first_name', '')
            last_name = player.get('last_name', '')
            return f"{first_name} {last_name}".strip()
        return f"Unknown Player ({player_id})"
    
    def import_draft_by_id(self, draft_id: str, keepers: List[str] = None) -> MockDraft:
        """Import a draft by its Sleeper draft ID."""
        print(f"Importing draft {draft_id}...")
        
        # Get draft picks
        draft_picks_raw = get_draft_picks(draft_id)
        
        if not draft_picks_raw:
            raise ValueError(f"No picks found for draft {draft_id}")
        
        # Load players if needed
        self.load_players()
        
        # Process picks
        picks = []
        for pick_data in draft_picks_raw:
            player_id = pick_data.get('player_id')
            if not player_id:
                continue  # Skip empty picks
            
            player_name = self.get_player_name(player_id)
            
            # Get player info for position and team
            player_info = self.all_players.get(player_id, {})
            position = player_info.get('position', 'UNK')
            team = player_info.get('team', 'FA')
            
            pick = DraftPick(
                player_name=player_name,
                player_id=player_id,
                position=position,
                team=team,
                round_num=pick_data.get('round', 0),
                pick_num=pick_data.get('pick_no', 0),
                overall_pick=pick_data.get('pick_no', 0),
                drafted_by_team=f"Team{pick_data.get('draft_slot', 0)}"
            )
            picks.append(pick)
        
        # Determine league size and rounds from picks
        if picks:
            max_round = max(pick.round_num for pick in picks)
            league_size = len(set(pick.drafted_by_team for pick in picks))
        else:
            max_round = 16  # Default
            league_size = 12  # Default
        
        mock_draft = MockDraft(
            draft_id=draft_id,
            draft_date=datetime.now(),
            league_size=league_size,
            rounds=max_round,
            keepers=keepers or [],
            picks=picks,
            notes=f"Imported from Sleeper draft {draft_id}"
        )
        
        return mock_draft
    
    def find_recent_drafts(self, username: str, season: int = 2024) -> List[dict]:
        """Find recent drafts for a user."""
        print(f"Finding recent drafts for {username} in {season}...")
        
        try:
            user = get_user(username)
            user_id = user['user_id']
            
            drafts = get_all_drafts(user_id, season)
            
            # Filter for recent drafts (last 7 days)
            recent_drafts = []
            now = datetime.now()
            
            for draft in drafts:
                # Sleeper timestamps are in milliseconds
                draft_time = datetime.fromtimestamp(draft.get('created', 0) / 1000)
                days_ago = (now - draft_time).days
                
                if days_ago <= 7:  # Last 7 days
                    recent_drafts.append({
                        'draft_id': draft['draft_id'],
                        'created': draft_time,
                        'status': draft.get('status', 'unknown'),
                        'type': draft.get('type', 'unknown'),
                        'league_id': draft.get('league_id'),
                        'days_ago': days_ago
                    })
            
            return sorted(recent_drafts, key=lambda x: x['created'], reverse=True)
            
        except Exception as e:
            print(f"Error finding drafts: {e}")
            return []
    
    def interactive_import(self):
        """Interactive method to import drafts."""
        print("\n=== Sleeper Mock Draft Importer ===")
        
        # Option 1: Import by draft ID
        print("\nOption 1: Import by Draft ID")
        draft_id = input("Enter Sleeper draft ID (or press Enter to skip): ").strip()
        
        if draft_id:
            try:
                # Get keepers
                print("\nEnter keeper players for this draft (one per line, empty line to finish):")
                keepers = []
                while True:
                    keeper = input("Keeper: ").strip()
                    if not keeper:
                        break
                    keepers.append(keeper)
                
                mock_draft = self.import_draft_by_id(draft_id, keepers)
                self.tracker.add_mock_draft(mock_draft)
                print(f"Successfully imported draft {draft_id} with {len(mock_draft.picks)} picks")
                return
                
            except Exception as e:
                print(f"Error importing draft: {e}")
        
        # Option 2: Find recent drafts
        print("\nOption 2: Find Recent Drafts")
        username = input("Enter your Sleeper username (or press Enter to skip): ").strip()
        
        if username:
            try:
                recent_drafts = self.find_recent_drafts(username)
                
                if not recent_drafts:
                    print("No recent drafts found.")
                    return
                
                print(f"\nFound {len(recent_drafts)} recent drafts:")
                for i, draft in enumerate(recent_drafts, 1):
                    print(f"{i}. {draft['draft_id']} - {draft['created'].strftime('%Y-%m-%d %H:%M')} "
                          f"({draft['days_ago']} days ago, {draft['status']})")
                
                choice = input(f"\nSelect draft to import (1-{len(recent_drafts)}) or press Enter to cancel: ").strip()
                
                if choice.isdigit() and 1 <= int(choice) <= len(recent_drafts):
                    selected_draft = recent_drafts[int(choice) - 1]
                    
                    # Get keepers for selected draft
                    print(f"\nImporting draft {selected_draft['draft_id']}")
                    print("Enter keeper players for this draft (one per line, empty line to finish):")
                    keepers = []
                    while True:
                        keeper = input("Keeper: ").strip()
                        if not keeper:
                            break
                        keepers.append(keeper)
                    
                    mock_draft = self.import_draft_by_id(selected_draft['draft_id'], keepers)
                    self.tracker.add_mock_draft(mock_draft)
                    print(f"Successfully imported draft with {len(mock_draft.picks)} picks")
                
            except Exception as e:
                print(f"Error finding recent drafts: {e}")

def main():
    """Main function for the importer."""
    importer = SleeperMockImporter()
    
    while True:
        print("\n=== Sleeper Mock Draft Importer ===")
        print("1. Import mock draft")
        print("2. View current ADP data")
        print("3. Export ADP to CSV")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            try:
                importer.interactive_import()
            except KeyboardInterrupt:
                print("\nImport cancelled.")
            except Exception as e:
                print(f"Error during import: {e}")
        
        elif choice == '2':
            importer.tracker.print_summary()
            
            # Show top 20 ADP
            adp_data = importer.tracker.calculate_adp()
            if adp_data:
                sorted_players = sorted(adp_data.values(), key=lambda x: x['average_pick'])[:20]
                print(f"\nTop 20 Players by ADP:")
                print(f"{'Rank':<4} {'Player':<25} {'ADP':<6} {'Times Drafted':<13} {'Range'}")
                print("-" * 70)
                for i, player in enumerate(sorted_players, 1):
                    range_str = f"{player['earliest_pick']}-{player['latest_pick']}"
                    print(f"{i:<4} {player['player_name']:<25} {player['average_pick']:<6.1f} "
                          f"{player['times_drafted']:<13} {range_str}")
        
        elif choice == '3':
            try:
                filename = importer.tracker.export_adp_to_csv()
                print(f"ADP exported to {filename}")
            except Exception as e:
                print(f"Error exporting ADP: {e}")
        
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
