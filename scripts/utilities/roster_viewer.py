import os
import sys
from dotenv import load_dotenv
from sleeper_api import SleeperAPI
import json

load_dotenv()

def get_roster_data(user_name, season='2024', verbose=True):
    """
    Get roster data from the Sleeper API with detailed player information
    including their draft positions from 2024.
    """
    if verbose:
        print(f"Looking up user: {user_name}")
    
    api = SleeperAPI(user_name)
    user = api.get_user(user_name)
    
    if not user:
        print(f"Error: User '{user_name}' not found.")
        return None

    user_id = user['user_id']
    if verbose:
        print(f"Found user with ID: {user_id}")
    
    leagues = api.get_leagues(season)
    if not leagues:
        print(f"Error: No leagues found for user '{user_name}' in the {season} season.")
        return None
    
    if verbose:
        print(f"Found {len(leagues)} leagues for {user_name} in {season}")
    
    # Find the Grundle league specifically
    league = None
    for l in leagues:
        if 'grundle' in l['name'].lower():
            league = l
            break
    
    if not league:
        print("Warning: 'Grundle' league not found. Please specify the league name:")
        for i, l in enumerate(leagues):
            print(f"{i+1}: {l['name']}")
        
        choice = input("Select league number: ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(leagues):
                league = leagues[idx]
            else:
                print("Invalid selection. Using first league.")
                league = leagues[0]
        except ValueError:
            print("Invalid input. Using first league.")
            league = leagues[0]
    
    league_id = league['league_id']
    if verbose:
        print(f"Using league: {league['name']} (ID: {league_id})")
    
    rosters = api.get_rosters(league_id)
    if verbose:
        print(f"Found {len(rosters)} rosters in league")
    
    users_in_league = api.get_league_users(league_id)
    if verbose:
        print(f"Found {len(users_in_league)} users in league")
    
    print("Loading player database...")
    all_players = api.get_players()
    print(f"Loaded {len(all_players)} players")
    
    # Try to find draft data from current season
    print("Looking for draft data...")
    draft_picks = []
    seasons_to_try = [season, str(int(season) - 1), str(int(season) - 2)]
    
    for try_season in seasons_to_try:
        if verbose:
            print(f"Checking for drafts in {try_season}...")
        
        drafts = api.get_all_drafts(league_id, try_season)
        
        if drafts:
            # Use the most recent draft from this season
            draft = drafts[0]  # Drafts are usually sorted by recency
            draft_id = draft['draft_id']
            if verbose:
                print(f"Found draft with ID: {draft_id}")
            
            draft_picks = api.get_draft_picks(draft_id)
            if draft_picks:
                print(f"Found {len(draft_picks)} draft picks from {try_season}")
                break
            else:
                print(f"No draft picks found for {try_season}")
    
    if not draft_picks:
        print("Warning: No draft picks found in any season.")
    
    # Create a map for user_id to display_name
    user_map = {u['user_id']: u['display_name'] for u in users_in_league}
    
    # Create a map for player_id to player details
    player_map = {p_id: p_info for p_id, p_info in all_players.items()}
    
    # Create a map for player_id to draft pick info
    draft_pick_map = {}
    for pick in draft_picks:
        if pick.get('player_id'):
            draft_pick_map[pick['player_id']] = {
                'round': pick.get('round', 'N/A'), 
                'pick': pick.get('pick_no', pick.get('draft_slot', 'N/A'))
            }
    
    teams_data = []
    for roster in rosters:
        owner_id = roster.get('owner_id')
        if not owner_id:
            continue
        
        players_in_roster = roster.get('players', [])
        if not players_in_roster:
            continue
        
        player_details_list = []
        for player_id in players_in_roster:
            player_info = player_map.get(player_id)
            if player_info:
                draft_info = draft_pick_map.get(player_id, {'round': 'N/A', 'pick': 'N/A'})
                # Get better position data for IDP players
                position = player_info.get('position', 'N/A')
                # For IDP players, try to get more specific position from fantasy_positions if available
                if position in ['DL', 'LB', 'DB'] and 'fantasy_positions' in player_info:
                    # Use the first fantasy position if available as it's often more specific
                    fantasy_pos = player_info.get('fantasy_positions', [])
                    if fantasy_pos and len(fantasy_pos) > 0:
                        position = fantasy_pos[0]
                
                player_details_list.append({
                    'id': player_id,
                    'name': player_info.get('full_name', 'Unknown Player'),
                    'position': position,
                    'draft_round': draft_info['round'],
                    'draft_pick': draft_info['pick'],
                    'team': player_info.get('team', 'FA')  # Add team info to help identify players
                })
        
        teams_data.append({
            'owner_id': owner_id,
            'owner_name': user_map.get(owner_id, 'Unknown Owner'),
            'players': sorted(player_details_list, key=lambda x: x['position'])
        })
    
    result = {
        'league_name': league['name'],
        'teams': sorted(teams_data, key=lambda x: x['owner_name'])
    }
    
    return result

def display_roster_data(data, format_type='simple'):
    """
    Display roster data in different formats
    """
    if not data:
        print("No data to display.")
        return
    
    print(f"\n=== {data['league_name']} ===\n")
    
    if format_type == 'simple':
        # Simple format with one line per player
        print("TEAM".ljust(20) + "PLAYER".ljust(30) + "POS".ljust(5) + "TEAM".ljust(5) + "DRAFT")
        print("-" * 70)
        
        all_players = []
        for team in data['teams']:
            owner = team['owner_name']
            for player in team['players']:
                all_players.append({
                    'owner': owner,
                    'name': player['name'],
                    'position': player['position'],
                    'team': player['team'],
                    'draft_round': player['draft_round'],
                    'draft_pick': player['draft_pick']
                })
        
        # Sort by position, then name
        all_players.sort(key=lambda x: (x['position'], x['name']))
        
        for player in all_players:
            draft_info = f"R{player['draft_round']}, P{player['draft_pick']}" if player['draft_round'] != 'N/A' else 'Undrafted'
            print(f"{player['owner'][:19].ljust(20)}{player['name'][:29].ljust(30)}{player['position'].ljust(5)}{player['team'].ljust(5)}{draft_info}")
    
    elif format_type == 'by_team':
        # Group by team
        for team in data['teams']:
            print(f"\n--- {team['owner_name']} ---")
            print("PLAYER".ljust(30) + "POS".ljust(5) + "TEAM".ljust(5) + "DRAFT")
            print("-" * 60)
            
            # Sort players by position
            sorted_players = sorted(team['players'], key=lambda x: (x['position'], x['name']))
            for player in sorted_players:
                draft_info = f"R{player['draft_round']}, P{player['draft_pick']}" if player['draft_round'] != 'N/A' else 'Undrafted'
                print(f"{player['name'][:29].ljust(30)}{player['position'].ljust(5)}{player['team'].ljust(5)}{draft_info}")
    
    elif format_type == 'by_position':
        # Group by position
        all_players = []
        for team in data['teams']:
            for player in team['players']:
                all_players.append({
                    'owner': team['owner_name'],
                    'name': player['name'],
                    'position': player['position'],
                    'team': player['team'],
                    'draft_round': player['draft_round'],
                    'draft_pick': player['draft_pick']
                })
        
        positions = sorted(set(p['position'] for p in all_players))
        for pos in positions:
            print(f"\n--- {pos} ---")
            print("PLAYER".ljust(30) + "TEAM".ljust(5) + "OWNER".ljust(20) + "DRAFT")
            print("-" * 70)
            
            pos_players = [p for p in all_players if p['position'] == pos]
            # Sort players by draft round, then name
            pos_players.sort(key=lambda x: (
                999 if x['draft_round'] == 'N/A' else int(x['draft_round']), 
                x['name']
            ))
            
            for player in pos_players:
                draft_info = f"R{player['draft_round']}, P{player['draft_pick']}" if player['draft_round'] != 'N/A' else 'Undrafted'
                print(f"{player['name'][:29].ljust(30)}{player['team'].ljust(5)}{player['owner'][:19].ljust(20)}{draft_info}")
    
    else:
        # JSON format
        print(json.dumps(data, indent=2))

def save_draftable_players(data, filename="draftable_players.txt"):
    """
    Save a list of players that you want to include in your draft board
    """
    if not data:
        print("No data to save.")
        return
    
    all_players = []
    for team in data['teams']:
        for player in team['players']:
            # Create player entry
            player_entry = {
                'id': player['id'],
                'name': player['name'],
                'position': player['position'],
                'team': player['team'],
                'owner': team['owner_name'],
                'draft_round': player['draft_round'],
                'draft_pick': player['draft_pick'],
                'include_in_draft': False  # Default to False
            }
            all_players.append(player_entry)
    
    # Sort by position, then name for easy reading
    all_players.sort(key=lambda x: (x['position'], x['name']))
    
    print("\n=== Player Selection ===")
    print("For each player, indicate if they should be included in your draft board (y/n):")
    print("(Press Enter to skip a player, which defaults to 'n')")
    
    selected_players = []
    for idx, player in enumerate(all_players):
        draft_info = f"R{player['draft_round']}, P{player['draft_pick']}" if player['draft_round'] != 'N/A' else 'Undrafted'
        choice = input(f"{player['position']} {player['name']} ({player['team']}) - Owner: {player['owner']} - {draft_info}: ")
        
        if choice.lower() == 'y':
            player['include_in_draft'] = True
            selected_players.append(player)
        
        # Display progress
        if (idx + 1) % 10 == 0:
            print(f"Processed {idx + 1}/{len(all_players)} players. Selected: {len(selected_players)}")
    
    # Save to file
    with open(filename, 'w') as f:
        f.write(f"# Draftable Players from {data['league_name']}\n")
        f.write("# Format: position,name,team,draft_round,draft_pick\n\n")
        
        for player in selected_players:
            f.write(f"{player['position']},{player['name']},{player['team']},{player['draft_round']},{player['draft_pick']}\n")
    
    print(f"\nSelected {len(selected_players)} players out of {len(all_players)}.")
    print(f"Saved to {filename}")

def main():
    # Check for SLEEPER_USERNAME environment variable
    sleeper_username = os.getenv('SLEEPER_USERNAME')
    if not sleeper_username:
        print("Error: SLEEPER_USERNAME environment variable not set.")
        print("Please set it before running this script.")
        print("Example: export SLEEPER_USERNAME=your_username")
        return
    
    print(f"Using Sleeper username: {sleeper_username}")
    
    # Get roster data
    roster_data = get_roster_data(sleeper_username)
    
    if not roster_data:
        print("Failed to retrieve roster data.")
        return
    
    # Menu for different views
    while True:
        print("\n=== Roster Viewer Menu ===")
        print("1: View all players (sorted by position)")
        print("2: View players by team")
        print("3: View players by position with draft info")
        print("4: Select players for draft board")
        print("5: Exit")
        
        choice = input("\nSelect an option (1-5): ")
        
        if choice == '1':
            display_roster_data(roster_data, 'simple')
        elif choice == '2':
            display_roster_data(roster_data, 'by_team')
        elif choice == '3':
            display_roster_data(roster_data, 'by_position')
        elif choice == '4':
            save_draftable_players(roster_data)
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
