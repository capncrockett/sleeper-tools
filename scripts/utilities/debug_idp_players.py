"""
Debug script to investigate IDP player data issues in the keeper tool.
"""
import os
import json
from dotenv import load_dotenv
from sleeper_api import SleeperAPI
from keeper_tool import get_keeper_data

def debug_idp_players():
    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    if not username:
        print("SLEEPER_USERNAME not set in environment variables.")
        return

    # Initialize the API client
    api = SleeperAPI(username)
    
    # Get all players
    print("Fetching all players data...")
    all_players = api.get_players()
    
    # Filter for IDP players (Defensive positions)
    idp_positions = ['DL', 'LB', 'DB', 'DE', 'DT', 'CB', 'S']
    idp_players = {
        player_id: player_data 
        for player_id, player_data in all_players.items() 
        if player_data.get('position') in idp_positions
    }
    
    print(f"Found {len(idp_players)} IDP players out of {len(all_players)} total players")
    
    # Check a sample of IDP players
    print("\nSample of IDP players:")
    sample_count = 0
    for player_id, player_data in idp_players.items():
        if sample_count >= 5:  # Show just a few samples
            break
        print(f"ID: {player_id}")
        print(f"  Name: {player_data.get('full_name', 'N/A')}")
        print(f"  Position: {player_data.get('position', 'N/A')}")
        print(f"  Team: {player_data.get('team', 'N/A')}")
        print(f"  Status: {player_data.get('status', 'N/A')}")
        print(f"  Fantasy positions: {player_data.get('fantasy_positions', ['N/A'])}")
        print()
        sample_count += 1
    
    # Get keeper data to see how IDP players are processed
    try:
        print("\nFetching keeper data to analyze IDP player processing...")
        keeper_info = get_keeper_data(username)
        
        # Look for IDP players in the keeper data
        idp_players_in_rosters = []
        for team in keeper_info.get('teams', []):
            for player in team.get('players', []):
                if player.get('position') in idp_positions:
                    idp_players_in_rosters.append(player)
        
        print(f"Found {len(idp_players_in_rosters)} IDP players in keeper data")
        
        # Check IDP player details in keeper data
        print("\nIDP players in keeper data:")
        for idx, player in enumerate(idp_players_in_rosters[:5]):  # First 5 IDP players
            print(f"{idx + 1}. {player.get('name')} ({player.get('position')})")
            print(f"  ID: {player.get('id')}")
            print(f"  Draft Round: {player.get('draft_round')}")
            print(f"  Draft Pick: {player.get('draft_pick')}")
            
            # Check original data
            original_data = all_players.get(player.get('id'), {})
            print(f"  Original Name: {original_data.get('full_name', 'N/A')}")
            print()
    
    except Exception as e:
        print(f"Error getting keeper data: {e}")

if __name__ == "__main__":
    debug_idp_players()
