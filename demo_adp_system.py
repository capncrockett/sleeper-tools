"""Demo script showing how to use the Custom ADP System

This demonstrates the key features of your keeper league ADP tracker.
"""

from datetime import datetime
from mock_draft_tracker import MockDraft, DraftPick, MockDraftTracker

def create_sample_data():
    """Create some sample mock draft data for demonstration."""
    tracker = MockDraftTracker("demo_mock_drafts.json")
    
    # Sample keepers (players off the board)
    keepers = ["Christian McCaffrey", "Josh Allen", "Tyreek Hill", "Travis Kelce"]
    
    # Sample Draft 1
    sample_picks_1 = [
        DraftPick("Ja'Marr Chase", "1001", "WR", "CIN", 1, 1, 1, "Team1"),
        DraftPick("Austin Ekeler", "1002", "RB", "LAC", 1, 2, 2, "Team2"),
        DraftPick("Stefon Diggs", "1003", "WR", "BUF", 1, 3, 3, "Team3"),
        DraftPick("Derrick Henry", "1004", "RB", "TEN", 1, 4, 4, "Team4"),
        DraftPick("Cooper Kupp", "1005", "WR", "LAR", 1, 5, 5, "Team5"),
        DraftPick("Nick Chubb", "1006", "RB", "CLE", 1, 6, 6, "Team6"),
        DraftPick("Davante Adams", "1007", "WR", "LV", 1, 7, 7, "Team7"),
        DraftPick("Saquon Barkley", "1008", "RB", "NYG", 1, 8, 8, "Team8"),
        DraftPick("CeeDee Lamb", "1009", "WR", "DAL", 1, 9, 9, "Team9"),
        DraftPick("Alvin Kamara", "1010", "RB", "NO", 1, 10, 10, "Team10"),
        DraftPick("Mike Evans", "1011", "WR", "TB", 1, 11, 11, "Team11"),
        DraftPick("Joe Mixon", "1012", "RB", "CIN", 1, 12, 12, "Team12"),
        # Round 2
        DraftPick("Lamar Jackson", "2001", "QB", "BAL", 2, 1, 13, "Team12"),
        DraftPick("A.J. Brown", "2002", "WR", "PHI", 2, 2, 14, "Team11"),
        DraftPick("Jaylen Waddle", "2003", "WR", "MIA", 2, 3, 15, "Team10"),
        DraftPick("Josh Jacobs", "2004", "RB", "LV", 2, 4, 16, "Team9"),
        DraftPick("Amon-Ra St. Brown", "2005", "WR", "DET", 2, 5, 17, "Team8"),
        DraftPick("Kenneth Walker III", "2006", "RB", "SEA", 2, 6, 18, "Team7"),
        DraftPick("DK Metcalf", "2007", "WR", "SEA", 2, 7, 19, "Team6"),
        DraftPick("Tony Pollard", "2008", "RB", "DAL", 2, 8, 20, "Team5"),
    ]
    
    draft1 = MockDraft(
        draft_id="demo_draft_1",
        draft_date=datetime(2024, 8, 10, 14, 30),
        league_size=12,
        rounds=16,
        keepers=keepers,
        picks=sample_picks_1,
        notes="First demo draft - standard scoring"
    )
    
    # Sample Draft 2 (slightly different order)
    sample_picks_2 = [
        DraftPick("Austin Ekeler", "1002", "RB", "LAC", 1, 1, 1, "Team1"),
        DraftPick("Ja'Marr Chase", "1001", "WR", "CIN", 1, 2, 2, "Team2"),
        DraftPick("Derrick Henry", "1004", "RB", "TEN", 1, 3, 3, "Team3"),
        DraftPick("Stefon Diggs", "1003", "WR", "BUF", 1, 4, 4, "Team4"),
        DraftPick("Nick Chubb", "1006", "RB", "CLE", 1, 5, 5, "Team5"),
        DraftPick("Cooper Kupp", "1005", "WR", "LAR", 1, 6, 6, "Team6"),
        DraftPick("Saquon Barkley", "1008", "RB", "NYG", 1, 7, 7, "Team7"),
        DraftPick("Davante Adams", "1007", "WR", "LV", 1, 8, 8, "Team8"),
        DraftPick("Alvin Kamara", "1010", "RB", "NO", 1, 9, 9, "Team9"),
        DraftPick("CeeDee Lamb", "1009", "WR", "DAL", 1, 10, 10, "Team10"),
        DraftPick("Joe Mixon", "1012", "RB", "CIN", 1, 11, 11, "Team11"),
        DraftPick("Mike Evans", "1011", "WR", "TB", 1, 12, 12, "Team12"),
        # Round 2
        DraftPick("Josh Jacobs", "2004", "RB", "LV", 2, 1, 13, "Team12"),
        DraftPick("A.J. Brown", "2002", "WR", "PHI", 2, 2, 14, "Team11"),
        DraftPick("Lamar Jackson", "2001", "QB", "BAL", 2, 3, 15, "Team10"),
        DraftPick("Amon-Ra St. Brown", "2005", "WR", "DET", 2, 4, 16, "Team9"),
        DraftPick("Kenneth Walker III", "2006", "RB", "SEA", 2, 5, 17, "Team8"),
        DraftPick("Jaylen Waddle", "2003", "WR", "MIA", 2, 6, 18, "Team7"),
        DraftPick("Tony Pollard", "2008", "RB", "DAL", 2, 7, 19, "Team6"),
        DraftPick("DK Metcalf", "2007", "WR", "SEA", 2, 8, 20, "Team5"),
    ]
    
    draft2 = MockDraft(
        draft_id="demo_draft_2",
        draft_date=datetime(2024, 8, 11, 16, 15),
        league_size=12,
        rounds=16,
        keepers=keepers,
        picks=sample_picks_2,
        notes="Second demo draft - PPR scoring"
    )
    
    # Add drafts to tracker
    tracker.add_mock_draft(draft1)
    tracker.add_mock_draft(draft2)
    
    return tracker

def demo_analysis():
    """Demonstrate ADP analysis features."""
    print("=== Custom Keeper League ADP System Demo ===\n")
    
    # Create sample data
    print("Creating sample mock draft data...")
    tracker = create_sample_data()
    
    # Show summary
    print("\n1. Draft Summary:")
    tracker.print_summary()
    
    # Calculate and show ADP
    print("\n2. ADP Analysis:")
    adp_data = tracker.calculate_adp()
    
    # Show top 15 players by ADP
    sorted_players = sorted(adp_data.values(), key=lambda x: x['average_pick'])[:15]
    print(f"\nTop 15 Players by Custom ADP:")
    print(f"{'Rank':<4} {'Player':<25} {'ADP':<6} {'Drafted':<8} {'Range':<10} {'Std Dev'}")
    print("-" * 75)
    
    for i, player in enumerate(sorted_players, 1):
        range_str = f"{player['earliest_pick']}-{player['latest_pick']}"
        print(f"{i:<4} {player['player_name']:<25} {player['average_pick']:<6.1f} "
              f"{player['times_drafted']:<8} {range_str:<10} {player['std_dev']}")
    
    # Show specific player analysis
    print("\n3. Individual Player Analysis:")
    test_player = "Ja'Marr Chase"
    analysis = tracker.get_player_analysis(test_player)
    if analysis:
        print(f"\n{test_player} Analysis:")
        print(f"  Times drafted: {analysis['times_drafted']}")
        print(f"  Draft percentage: {analysis['draft_percentage']:.1f}%")
        print(f"  Average pick: {analysis['average_pick']}")
        print(f"  Pick range: {analysis['earliest_pick']} - {analysis['latest_pick']}")
        print(f"  Standard deviation: {analysis['std_dev']}")
        print(f"  All picks: {analysis['all_picks']}")
    
    # Export to CSV
    print("\n4. CSV Export:")
    filename = tracker.export_adp_to_csv("demo_custom_adp.csv")
    print(f"Sample ADP data exported to: {filename}")
    
    print(f"\n=== Demo Complete ===")
    print(f"Key Benefits for Your Keeper League:")
    print(f"• Custom ADP accounts for keepers being off the board")
    print(f"• Track variance in player draft positions")
    print(f"• Identify value picks and reaches")
    print(f"• Export data for draft day reference")
    print(f"• Build strategy based on YOUR league's tendencies")

if __name__ == "__main__":
    demo_analysis()
