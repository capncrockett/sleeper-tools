import os
from dotenv import load_dotenv
from sleeper_api import SleeperAPI

load_dotenv()

def get_keeper_data(user_name, season='2024'):
    api = SleeperAPI()
    user = api.get_user(user_name)
    if not user:
        raise ValueError(f"User '{user_name}' not found.")

    user_id = user['user_id']
    leagues = api.get_user_leagues(user_id, season)
    if not leagues:
        raise ValueError(f"No leagues found for user '{user_name}' in the {season} season.")

    # For simplicity, we'll use the first league found.
    # In a real app, you might let the user select a league.
    league = leagues[0]
    league_id = league['league_id']

    rosters = api.get_rosters(league_id)
    users_in_league = api.get_users_in_league(league_id)
    all_players = api.get_all_players()

    # Find the previous season's draft
    drafts = api.get_all_drafts_for_league(league_id)
    previous_season_draft = next((d for d in drafts if d['season'] == str(int(season) - 1)), None)
    
    draft_picks = []
    if previous_season_draft:
        draft_id = previous_season_draft['draft_id']
        draft_picks = api.get_draft_picks(draft_id)

    # Create a map for user_id to display_name
    user_map = {u['user_id']: u['display_name'] for u in users_in_league}

    # Create a map for player_id to player details
    player_map = {p_id: p_info for p_id, p_info in all_players.items()}

    # Create a map for player_id to draft pick info
    draft_pick_map = {pick['player_id']: {'round': pick['round'], 'pick': pick['pick']} for pick in draft_picks}

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
