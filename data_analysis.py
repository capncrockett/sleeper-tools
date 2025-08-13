import requests
from sleeper_api import get_user, get_all_leagues, get_draft_picks, get_all_players

def get_draft_position(draft_picks, user_id):
    """Finds the draft position for a given user."""
    for pick in draft_picks:
        if pick.get('picked_by') == user_id:
            return pick.get('draft_slot')
    return None

def get_team(draft_picks, user_id, all_players):
    """Gets the final team for a given user."""
    team = []
    for pick in draft_picks:
        if pick.get('picked_by') == user_id:
            player_id = pick.get('player_id')
            player_info = all_players.get(player_id, {})
            first_name = player_info.get('first_name', 'N/A')
            last_name = player_info.get('last_name', '')
            team.append(f"{first_name} {last_name}".strip())
    return team

def main():
    """Main function to get draft results."""
    try:
        username = input("Enter your Sleeper username: ")
        season = input("Enter the season (e.g., 2024): ")

        user = get_user(username)
        if not user:
            print(f"User '{username}' not found.")
            return

        user_id = user['user_id']
        print(f"\nFound user '{username}' with ID: {user_id}")

        leagues = get_all_leagues(user_id, season)
        if not leagues:
            print(f"No leagues found for user '{username}' in {season}.")
            return

        print("\nAvailable leagues:")
        for i, league in enumerate(leagues):
            print(f"[{i + 1}] {league.get('name', 'N/A')}")

        choice = int(input("\nEnter the number of the league you want to analyze: ")) - 1
        selected_league = leagues[choice]
        draft_id = selected_league.get('draft_id')

        if not draft_id:
            print(f"No draft ID found for league '{selected_league.get('name', 'N/A')}'.")
            return

        print(f"\nAnalyzing draft for league: {selected_league.get('name', 'N/A')}")

        draft_picks = get_draft_picks(draft_id)
        all_players = get_all_players()

        draft_position = get_draft_position(draft_picks, user_id)
        if draft_position:
            print(f"\nDraft Position: {draft_position}")
        else:
            print("\nCould not determine your draft position.")

        final_team = get_team(draft_picks, user_id, all_players)
        if final_team:
            print("\nYour Final Team:")
            for player in final_team:
                print(f"- {player}")
        else:
            print("Could not determine your final team.")

    except requests.exceptions.HTTPError as e:
        print(f"API Error: {e.response.status_code} - {e.response.text}")
    except (ValueError, IndexError):
        print("Invalid selection. Please run the script again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
