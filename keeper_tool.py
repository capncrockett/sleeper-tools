import os
from dotenv import load_dotenv
from sleeper_api import SleeperAPI

load_dotenv()

def get_keeper_data(user_name, season='2024'):
    api = SleeperAPI(user_name)
    user = api.get_user(user_name)
    if not user:
        raise ValueError(f"User '{user_name}' not found.")

    user_id = user['user_id']
    leagues = api.get_leagues(season)
    if not leagues:
        raise ValueError(f"No leagues found for user '{user_name}' in the {season} season.")

    # Find the Grundle league specifically
    league = None
    for l in leagues:
        if 'grundle' in l['name'].lower():
            league = l
            break
    
    if not league:
        # Fallback to first league if Grundle not found
        league = leagues[0]
    league_id = league['league_id']

    rosters = api.get_rosters(league_id)
    users_in_league = api.get_league_users(league_id)
    all_players = api.get_players()

    # Try to find draft data from current season first, then previous seasons
    draft_picks = []
    seasons_to_try = [season, str(int(season) - 1), str(int(season) - 2)]
    
    for try_season in seasons_to_try:
        drafts = api.get_all_drafts(try_season)
        
        if drafts:
            # Use the most recent draft from this season
            draft = drafts[0]  # Drafts are usually sorted by recency
            draft_id = draft['draft_id']
            draft_picks = api.get_draft_picks(draft_id)
            if draft_picks:
                break

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
                player_details_list.append({
                    'id': player_id,
                    'name': player_info.get('full_name', 'Unknown Player'),
                    'position': player_info.get('position', 'N/A'),
                    'draft_round': draft_info['round'],
                    'draft_pick': draft_info['pick']
                })

        teams_data.append({
            'owner_id': owner_id,
            'owner_name': user_map.get(owner_id, 'Unknown Owner'),
            'players': player_details_list
        })

    return {
        'league_name': league['name'],
        'teams': teams_data
    }

if __name__ == '__main__':
    # Example usage:
    try:
        sleeper_username = os.getenv('SLEEPER_USERNAME')
        if not sleeper_username:
            raise ValueError("SLEEPER_USERNAME environment variable not set.")
        keeper_info = get_keeper_data(sleeper_username)
        import json
        print(json.dumps(keeper_info, indent=2))
    except ValueError as e:
        print(f"Error: {e}")
