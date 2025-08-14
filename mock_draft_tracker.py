"""Mock Draft Tracker for Custom ADP Calculation

This module handles the collection and analysis of mock draft data
to calculate custom Average Draft Position (ADP) for keeper leagues.
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import statistics

@dataclass
class DraftPick:
    """Represents a single draft pick."""
    player_name: str
    player_id: Optional[str]
    position: str
    team: str
    round_num: int
    pick_num: int
    overall_pick: int
    drafted_by_team: str

@dataclass
class MockDraft:
    """Represents a complete mock draft."""
    draft_id: str
    draft_date: datetime
    league_size: int
    rounds: int
    keepers: List[str]  # List of keeper player names
    picks: List[DraftPick]
    notes: Optional[str] = None

class MockDraftTracker:
    """Main class for tracking and analyzing mock drafts."""
    
    def __init__(self, data_file: str = "mock_drafts.json"):
        self.data_file = data_file
        self.drafts: List[MockDraft] = []
        self.load_data()
    
    def load_data(self) -> None:
        """Load existing mock draft data from file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.drafts = [self._dict_to_mock_draft(draft_dict) for draft_dict in data]
                print(f"Loaded {len(self.drafts)} mock drafts from {self.data_file}")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading data: {e}. Starting with empty dataset.")
                self.drafts = []
        else:
            print(f"No existing data file found. Starting fresh.")
            self.drafts = []
    
    def save_data(self) -> None:
        """Save mock draft data to file."""
        data = [self._mock_draft_to_dict(draft) for draft in self.drafts]
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"Saved {len(self.drafts)} mock drafts to {self.data_file}")
    
    def _mock_draft_to_dict(self, draft: MockDraft) -> dict:
        """Convert MockDraft to dictionary for JSON serialization."""
        draft_dict = asdict(draft)
        draft_dict['draft_date'] = draft.draft_date.isoformat()
        return draft_dict
    
    def _dict_to_mock_draft(self, draft_dict: dict) -> MockDraft:
        """Convert dictionary to MockDraft object."""
        draft_dict['draft_date'] = datetime.fromisoformat(draft_dict['draft_date'])
        picks = [DraftPick(**pick) for pick in draft_dict['picks']]
        draft_dict['picks'] = picks
        return MockDraft(**draft_dict)
    
    def add_mock_draft(self, draft: MockDraft) -> None:
        """Add a new mock draft to the tracker."""
        self.drafts.append(draft)
        self.save_data()
        print(f"Added mock draft {draft.draft_id} with {len(draft.picks)} picks")
    
    def create_mock_draft_from_input(self) -> MockDraft:
        """Interactive method to create a mock draft from user input."""
        print("\n=== Creating New Mock Draft ===")
        
        draft_id = input("Enter draft ID (or press Enter for auto-generated): ").strip()
        if not draft_id:
            draft_id = f"mock_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        league_size = int(input("League size (default 12): ") or "12")
        rounds = int(input("Number of rounds (default 16): ") or "16")
        
        # Get keepers
        print("\nEnter keeper players (one per line, empty line to finish):")
        keepers = []
        while True:
            keeper = input("Keeper: ").strip()
            if not keeper:
                break
            keepers.append(keeper)
        
        # Get draft picks
        print(f"\nEnter draft picks (expecting {league_size * rounds} total picks)")
        print("Format: PlayerName,Position,Team,Round,Pick")
        print("Example: Josh Allen,QB,BUF,1,5")
        
        picks = []
        for overall_pick in range(1, league_size * rounds + 1):
            round_num = ((overall_pick - 1) // league_size) + 1
            pick_in_round = ((overall_pick - 1) % league_size) + 1
            
            while True:
                try:
                    pick_input = input(f"Pick {overall_pick} (Round {round_num}, Pick {pick_in_round}): ").strip()
                    if not pick_input:
                        print("Pick cannot be empty. Please enter pick data.")
                        continue
                    
                    parts = pick_input.split(',')
                    if len(parts) < 4:
                        print("Please use format: PlayerName,Position,Team,Round,Pick")
                        continue
                    
                    player_name = parts[0].strip()
                    position = parts[1].strip()
                    team = parts[2].strip()
                    drafted_by_team = parts[4].strip() if len(parts) > 4 else f"Team{pick_in_round}"
                    
                    pick = DraftPick(
                        player_name=player_name,
                        player_id=None,  # We'll populate this later if needed
                        position=position,
                        team=team,
                        round_num=round_num,
                        pick_num=pick_in_round,
                        overall_pick=overall_pick,
                        drafted_by_team=drafted_by_team
                    )
                    picks.append(pick)
                    break
                    
                except (ValueError, IndexError) as e:
                    print(f"Error parsing pick: {e}. Please try again.")
        
        notes = input("\nAny notes about this draft (optional): ").strip() or None
        
        mock_draft = MockDraft(
            draft_id=draft_id,
            draft_date=datetime.now(),
            league_size=league_size,
            rounds=rounds,
            keepers=keepers,
            picks=picks,
            notes=notes
        )
        
        return mock_draft
    
    def calculate_adp(self, min_drafts: int = 3) -> Dict[str, Dict]:
        """Calculate Average Draft Position for all players."""
        if len(self.drafts) < min_drafts:
            print(f"Warning: Only {len(self.drafts)} drafts available. Recommend at least {min_drafts} for reliable ADP.")
        
        player_picks = defaultdict(list)
        
        # Collect all picks for each player
        for draft in self.drafts:
            for pick in draft.picks:
                player_picks[pick.player_name].append(pick.overall_pick)
        
        adp_data = {}
        for player_name, picks in player_picks.items():
            if len(picks) >= 1:  # At least one draft
                adp_data[player_name] = {
                    'player_name': player_name,
                    'times_drafted': len(picks),
                    'draft_percentage': (len(picks) / len(self.drafts)) * 100,
                    'average_pick': round(statistics.mean(picks), 1),
                    'median_pick': statistics.median(picks),
                    'earliest_pick': min(picks),
                    'latest_pick': max(picks),
                    'std_dev': round(statistics.stdev(picks) if len(picks) > 1 else 0, 1),
                    'all_picks': sorted(picks)
                }
        
        return adp_data
    
    def export_adp_to_csv(self, filename: str = None) -> str:
        """Export ADP data to CSV file."""
        if filename is None:
            filename = f"custom_adp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        adp_data = self.calculate_adp()
        
        # Sort by average pick
        sorted_players = sorted(adp_data.values(), key=lambda x: x['average_pick'])
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [
                'rank', 'player_name', 'times_drafted', 'draft_percentage',
                'average_pick', 'median_pick', 'earliest_pick', 'latest_pick', 'std_dev'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for rank, player_data in enumerate(sorted_players, 1):
                row = player_data.copy()
                row['rank'] = rank
                row['draft_percentage'] = f"{row['draft_percentage']:.1f}%"
                del row['all_picks']  # Remove detailed picks from CSV
                writer.writerow(row)
        
        print(f"ADP data exported to {filename}")
        print(f"Total players: {len(sorted_players)}")
        print(f"Based on {len(self.drafts)} mock drafts")
        
        return filename
    
    def get_player_analysis(self, player_name: str) -> Optional[Dict]:
        """Get detailed analysis for a specific player."""
        adp_data = self.calculate_adp()
        return adp_data.get(player_name)
    
    def print_summary(self) -> None:
        """Print a summary of all tracked drafts."""
        print(f"\n=== Mock Draft Summary ===")
        print(f"Total drafts: {len(self.drafts)}")
        
        if self.drafts:
            total_picks = sum(len(draft.picks) for draft in self.drafts)
            avg_picks_per_draft = total_picks / len(self.drafts)
            
            print(f"Total picks tracked: {total_picks}")
            print(f"Average picks per draft: {avg_picks_per_draft:.1f}")
            
            # Show recent drafts
            print(f"\nRecent drafts:")
            for draft in sorted(self.drafts, key=lambda x: x.draft_date, reverse=True)[:5]:
                print(f"  {draft.draft_id}: {draft.draft_date.strftime('%Y-%m-%d %H:%M')} "
                      f"({len(draft.picks)} picks, {len(draft.keepers)} keepers)")

def main():
    """Main function for interactive mock draft tracking."""
    tracker = MockDraftTracker()
    
    while True:
        print("\n=== Mock Draft Tracker ===")
        print("1. Add new mock draft")
        print("2. View summary")
        print("3. Export ADP to CSV")
        print("4. Analyze specific player")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            try:
                mock_draft = tracker.create_mock_draft_from_input()
                tracker.add_mock_draft(mock_draft)
            except KeyboardInterrupt:
                print("\nDraft entry cancelled.")
            except Exception as e:
                print(f"Error creating draft: {e}")
        
        elif choice == '2':
            tracker.print_summary()
        
        elif choice == '3':
            try:
                filename = tracker.export_adp_to_csv()
                print(f"\nADP data saved to: {filename}")
            except Exception as e:
                print(f"Error exporting ADP: {e}")
        
        elif choice == '4':
            player_name = input("Enter player name: ").strip()
            analysis = tracker.get_player_analysis(player_name)
            if analysis:
                print(f"\n=== Analysis for {player_name} ===")
                print(f"Times drafted: {analysis['times_drafted']}")
                print(f"Draft percentage: {analysis['draft_percentage']:.1f}%")
                print(f"Average pick: {analysis['average_pick']}")
                print(f"Pick range: {analysis['earliest_pick']} - {analysis['latest_pick']}")
                print(f"All picks: {analysis['all_picks']}")
            else:
                print(f"No data found for {player_name}")
        
        elif choice == '5':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()
