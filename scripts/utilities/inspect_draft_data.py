"""Inspect the actual draft data to see what's wrong with ADP calculation"""

from mock_draft_tracker import MockDraftTracker

def inspect_draft_data():
    """Look at the raw draft data to understand the ADP calculation issue."""
    tracker = MockDraftTracker()
    
    print("=== Inspecting Draft Data ===\n")
    
    if not tracker.drafts:
        print("No draft data found")
        return
    
    print(f"Found {len(tracker.drafts)} drafts")
    
    # Look at first overall picks in each draft
    print("\n=== First Overall Picks (1.01) ===")
    first_picks = []
    
    for i, draft in enumerate(tracker.drafts, 1):
        print(f"\nDraft {i} ({draft.draft_id}):")
        print(f"  Total picks: {len(draft.picks)}")
        
        # Find the first overall pick
        first_pick = None
        for pick in draft.picks:
            if pick.overall_pick == 1:
                first_pick = pick
                break
        
        if first_pick:
            print(f"  1.01: {first_pick.player_name}")
            first_picks.append(first_pick.player_name)
        else:
            print(f"  1.01: NOT FOUND")
            # Show first few picks to debug
            sorted_picks = sorted(draft.picks, key=lambda x: x.overall_pick)
            print(f"  First 5 picks:")
            for pick in sorted_picks[:5]:
                print(f"    {pick.overall_pick}: {pick.player_name}")
    
    print(f"\n=== First Pick Summary ===")
    from collections import Counter
    first_pick_counts = Counter(first_picks)
    for player, count in first_pick_counts.items():
        print(f"  {player}: {count} times")
    
    # Look at Saquon and Chase specifically
    print(f"\n=== Saquon Barkley Analysis ===")
    saquon_picks = []
    for draft in tracker.drafts:
        for pick in draft.picks:
            if "Saquon" in pick.player_name:
                saquon_picks.append(pick.overall_pick)
                print(f"  Draft {draft.draft_id[-4:]}: Pick {pick.overall_pick}")
    
    if saquon_picks:
        avg_saquon = sum(saquon_picks) / len(saquon_picks)
        print(f"  Saquon average pick: {avg_saquon:.1f}")
        print(f"  Saquon picks: {saquon_picks}")
    
    print(f"\n=== Ja'Marr Chase Analysis ===")
    chase_picks = []
    for draft in tracker.drafts:
        for pick in draft.picks:
            if "Ja'Marr" in pick.player_name:
                chase_picks.append(pick.overall_pick)
                print(f"  Draft {draft.draft_id[-4:]}: Pick {pick.overall_pick}")
    
    if chase_picks:
        avg_chase = sum(chase_picks) / len(chase_picks)
        print(f"  Chase average pick: {avg_chase:.1f}")
        print(f"  Chase picks: {chase_picks}")
    
    # Show first round of each draft
    print(f"\n=== First Round Analysis ===")
    for i, draft in enumerate(tracker.drafts, 1):
        print(f"\nDraft {i} - First Round:")
        first_round = [p for p in draft.picks if p.round_num == 1]
        first_round.sort(key=lambda x: x.overall_pick)
        
        for pick in first_round[:12]:  # Show first 12 picks
            print(f"  {pick.overall_pick:2d}. {pick.player_name}")

if __name__ == "__main__":
    inspect_draft_data()
