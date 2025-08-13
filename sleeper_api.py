import requests

BASE_URL = "https://api.sleeper.app/v1"

def get_user(username):
    """Fetches a user by username."""
    response = requests.get(f"{BASE_URL}/user/{username}")
    response.raise_for_status()
    return response.json()

def get_all_drafts(user_id, season):
    """Fetches all drafts for a user for a given season."""
    response = requests.get(f"{BASE_URL}/user/{user_id}/drafts/nfl/{season}")
    response.raise_for_status()
    return response.json()

def get_draft_picks(draft_id):
    """Fetches all picks for a given draft."""
    response = requests.get(f"{BASE_URL}/draft/{draft_id}/picks")
    response.raise_for_status()
    return response.json()

def get_all_players():
    """Fetches all players."""
    response = requests.get(f"{BASE_URL}/players/nfl")
    response.raise_for_status()
    return response.json()
import json
from dotenv import load_dotenv
import os

class SleeperAPI:
    def __init__(self, username):
        self.base_url = "https://api.sleeper.app/v1"
        self.username = username
        self.user_id = None
        self._get_user_id()

    def _make_request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None

    def _get_user_id(self):
        """Fetch user ID from username and store it."""
        user_data = self.get_user(self.username)
        if user_data and 'user_id' in user_data:
            self.user_id = user_data['user_id']
        else:
            raise ValueError(f"Could not find user ID for username: {self.username}")

    def get_user(self, username):
        """Get user information by username"""
        url = f"{self.base_url}/user/{username}"
        return self._make_request(url)

    def get_leagues(self, season):
        """Get leagues for a specific season"""
        if not self.user_id:
            print("User ID not set. Cannot fetch leagues.")
            return None
        url = f"{self.base_url}/user/{self.user_id}/leagues/nfl/{season}"
        return self._make_request(url)

    def get_rosters(self, league_id):
        """Get rosters for a specific league"""
        url = f"{self.base_url}/league/{league_id}/rosters"
        return requests.get(url).json()

    def get_players(self):
        """Get all NFL players"""
        url = f"{self.base_url}/players/nfl"
        return requests.get(url).json()

    def get_matchup(self, league_id, week):
        """Get matchup results for a specific week"""
        url = f"{self.base_url}/league/{league_id}/matchups/{week}"
        return self._make_request(url)

    def get_all_drafts(self, season):
        """Get all drafts for a user in a given season."""
        if not self.user_id:
            print("User ID not set. Cannot fetch drafts.")
            return None
        url = f"{self.base_url}/user/{self.user_id}/drafts/nfl/{season}"
        return self._make_request(url)

    def get_draft_picks(self, draft_id):
        """Get all picks for a specific draft."""
        url = f"{self.base_url}/draft/{draft_id}/picks"
        return self._make_request(url)

    def get_league_users(self, league_id):
        """Get all users in a specific league."""
        url = f"{self.base_url}/league/{league_id}/users"
        return self._make_request(url)

# Example usage
if __name__ == "__main__":
    load_dotenv()
    username = os.getenv('SLEEPER_USERNAME')
    if not username:
        print("SLEEPER_USERNAME not found in .env file.")
    else:
        try:
            # Initialize API client
            api = SleeperAPI(username)
            print(f"Fetching data for user: {api.username} (ID: {api.user_id})")

            # Get user's leagues for the current season
            season = "2025"  # Current NFL season
            leagues = api.get_leagues(season)
            if leagues:
                print(f"\nLeagues for {season}:")
                for league in leagues:
                    print(f"- {league['name']}")

                # --- Get Team Info for the first league ---
                first_league = leagues[0]
                league_id = first_league['league_id']
                print(f"\n--- Teams in '{first_league['name']}' ---")
                
                rosters = api.get_rosters(league_id)
                users = api.get_league_users(league_id)

                if rosters and users:
                    user_map = {user['user_id']: user for user in users}
                    for roster in rosters:
                        owner_id = roster.get('owner_id')
                        owner_name = user_map.get(owner_id, {}).get('display_name', 'Unknown Owner')
                        team_name = user_map.get(owner_id, {}).get('metadata', {}).get('team_name', owner_name)
                        print(f"- {team_name} (Owner: {owner_name})")
                else:
                    print("Could not retrieve team information for the league.")
            else:
                print(f"No leagues found for the {season} season.")

            # Get players for name lookups
            all_players = api.get_players()

            # --- Get results from the latest completed league draft ---
            drafts = api.get_all_drafts(season)
            if drafts:
                completed_drafts = [d for d in drafts if d.get('status') == 'complete']
                if completed_drafts:
                    latest_draft = max(completed_drafts, key=lambda x: x.get('last_picked', 0))
                    draft_id = latest_draft['draft_id']
                    league_name = latest_draft.get('metadata', {}).get('name', 'Unknown League')
                    print(f"\n--- Results for Latest Completed Draft: '{league_name}' (ID: {draft_id}) ---")
                    picks = api.get_draft_picks(draft_id)
                    if picks:
                        for pick in picks[:10]: # Show first 10 picks as a sample
                            player_id = pick['player_id']
                            player_info = all_players.get(player_id, {})
                            player_name = player_info.get('full_name', 'Unknown Player')
                            print(f"  Pick {pick['pick_no']}: {player_name}")
                        if len(picks) > 10:
                            print("  ... and more.")
                else:
                    print("\nNo completed league drafts found for this season.")
            else:
                print("\nCould not retrieve league draft information.")

            # --- Get picks for the specific mock draft ID you provided ---
            specific_draft_id = "1261474618305167360"
            print(f"\n--- Picks for Specific Mock Draft (ID: {specific_draft_id}) ---")
            picks = api.get_draft_picks(specific_draft_id)
            if picks:
                print(f"Found {len(picks)} picks. Your picks were:")
                for pick in picks:
                    if pick['picked_by'] == api.user_id:
                        player_id = pick['player_id']
                        player_info = all_players.get(player_id, {})
                        player_name = player_info.get('full_name', 'Unknown Player')
                        print(f"  - Pick {pick['pick_no']}: {player_name}")
            else:
                print("Could not retrieve picks for the specified mock draft ID.")

        except ValueError as e:
            print(e)
