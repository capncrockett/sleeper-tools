# Sleeper API Client

A Python client for interacting with the Sleeper Fantasy Football API.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your Sleeper user ID:
```
SLEEPER_USERNAME=your_username
```

3. Run the example:
```bash
python sleeper_api.py
```

### Data Analysis

The `data_analysis.py` script provides a tool to analyze your mock drafts. It calculates the "value" of each of your picks by comparing the player's draft position to their Average Draft Position (ADP) from Fantasy Football Calculator.

To run the analysis, you need to provide a mock draft ID as a command-line argument:

```bash
# Replace YOUR_DRAFT_ID with the actual ID of your mock draft
python data_analysis.py YOUR_DRAFT_ID
```

The script will output a summary of the best and worst value picks you made in that draft.

## Features

- Get user information from a username.
- Retrieve a user's leagues for a given season.
- Get rosters and team owners for a specific league.
- Access complete NFL player data.
- View matchup results for a league.
- Fetch all of a user's drafts for a season.
- Get all picks from a specific draft ID (for league or mock drafts).

## Usage

```python
from sleeper_api import SleeperAPI

api = SleeperAPI()

# Get user info
user = api.get_user()

# Get leagues for current season
leagues = api.get_leagues("2025")

# Get rosters for a specific league
rosters = api.get_rosters("league_id")

# Get player information
players = api.get_players()

# Get matchup results
matchups = api.get_matchup("league_id", 1)

# Get all drafts for a user
drafts = api.get_all_drafts("2025")

# Get all picks from a specific draft
draft_picks = api.get_draft_picks("your_draft_id")

# Get all users in a league (to find team owners)
users = api.get_league_users("league_id")
```

## API Documentation

For more information about the Sleeper API endpoints, visit: https://docs.sleeper.com/
