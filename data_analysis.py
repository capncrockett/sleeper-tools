import requests
from sleeper_api import SleeperAPI
from dotenv import load_dotenv
import os

def get_adp_data(year, scoring='ppr', teams=12):
    """Fetch ADP data from Fantasy Football Calculator."""
    url = f"https://fantasyfootballcalculator.com/api/v1/adp/{scoring}?teams={teams}&year={year}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return {player['name']: player['adp'] for player in response.json()['players']}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ADP data: {e}")
        return None

def analyze_draft_value(draft_picks, adp_data, all_players):
    """Analyzes the value of each pick in a draft based on ADP."""
    value_picks = []
    for pick in draft_picks:
        player_id = pick['player_id']
        player_info = all_players.get(player_id, {})
        player_name = player_info.get('full_name')

        if player_name and player_name in adp_data:
            adp = adp_data[player_name]
            pick_number = pick['pick_no']
            value = adp - pick_number
            value_picks.append({'name': player_name, 'pick': pick_number, 'adp': adp, 'value': value})
    
    return sorted(value_picks, key=lambda x: x['value'], reverse=True)

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze a Sleeper mock draft for pick value based on ADP.')
    parser.add_argument('draft_id', help='The ID of the mock draft to analyze.')
    args = parser.parse_args()

    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    if not username:
        print("SLEEPER_USERNAME not found in .env file.")
    else:
        try:
            api = SleeperAPI(username)
            all_players = api.get_players()
            adp_data = get_adp_data(2025)

            if not all_players or not adp_data:
                raise ValueError("Could not fetch necessary data for analysis.")

            # Analyze the specific mock draft
            print(f"\n--- Draft Value Analysis for Mock Draft (ID: {args.draft_id}) ---")
            mock_draft_picks = api.get_draft_picks(args.draft_id)

            if mock_draft_picks:
                user_picks = [p for p in mock_draft_picks if p['picked_by'] == api.user_id]
                value_analysis = analyze_draft_value(user_picks, adp_data, all_players)

                if value_analysis:
                    print("\n--- Best Value Picks (Top 5) ---")
                    for item in value_analysis[:5]:
                        print(f"  - {item['name']}: Picked at {item['pick']:.0f}, ADP {item['adp']:.1f} (Value: +{item['value']:.1f})")

                    print("\n--- Worst Value Picks (Bottom 5) ---")
                    for item in value_analysis[-5:]:
                        sign = '+' if item['value'] >= 0 else ''
                        print(f"  - {item['name']}: Picked at {item['pick']:.0f}, ADP {item['adp']:.1f} (Value: {sign}{item['value']:.1f})")
                else:
                    print("Could not perform value analysis for your picks.")
            else:
                print("Could not retrieve picks for the specified mock draft ID.")

        except (ValueError, Exception) as e:
            print(e)
