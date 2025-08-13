# Sleeper API Client

A clean, well-organized Python client for interacting with the Sleeper Fantasy Football API.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your Sleeper username:
```
SLEEPER_USERNAME=your_username
```

3. Run the example:
```bash
python sleeper_api.py
```

## Scripts

### sleeper_api.py
Main API client with both standalone functions and a comprehensive `SleeperAPI` class. Includes:
- Clean, organized code structure
- Consistent error handling
- Example usage demonstrating all features

### data_analysis.py
Interactive draft analysis tool that helps you:
- Select from your available leagues
- View your draft position and final team
- Analyze draft results with detailed player information

Run the analysis interactively:
```bash
python data_analysis.py
```

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
