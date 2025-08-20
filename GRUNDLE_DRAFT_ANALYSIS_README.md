# Grundle Draft Positions Tool

## Overview
This tool retrieves the 2024 draft positions of all players currently on rosters in the Grundle league and provides detailed analysis of draft value and roster composition.

## Features
- Fetches current roster data from the 2025 season
- Maps players to their 2024 draft positions 
- Provides summary statistics for each team
- Shows detailed roster breakdowns with draft info
- Export data to CSV or JSON formats

## Usage
Run the script with your virtual environment activated:

```bash
python grundle_draft_positions.py
```

Make sure your `SLEEPER_USERNAME` environment variable is set in your `.env` file.

## Menu Options
1. **Show summary table** - Overview of each team's drafted vs undrafted players
2. **Show detailed rosters** - Full roster breakdown with draft positions
3. **Save to CSV** - Export data to `grundle_draft_analysis_2024.csv`
4. **Save to JSON** - Export data to `grundle_draft_analysis_2024.json` 
5. **Show both summary and details** - Display both views
6. **Exit** - Quit the program

## Output Format

### Summary Table
Shows for each team:
- Team name and owner
- Number of drafted vs undrafted players
- Earliest and latest draft picks
- Total roster size

### Detailed Rosters
For each player shows:
- Player name, position, NFL team
- Draft round, pick number, and overall pick
- Undrafted players are clearly marked

### CSV Export
Contains all player data with fields:
- team_name, owner_name, player_name, position, nfl_team
- draft_round, draft_pick, overall_pick, drafted (boolean)

## Requirements
- Python environment with `requests` and `python-dotenv` packages
- Sleeper API access (via existing `sleeper_api.py` module)
- Valid `SLEEPER_USERNAME` in environment

## Key Features
- **Smart League Detection**: Automatically finds the "Grundle" league
- **Cross-Season Analysis**: Uses 2025 rosters with 2024 draft data
- **Robust Error Handling**: Gracefully handles missing data
- **Multiple Export Formats**: CSV and JSON support
- **IDP Position Support**: Enhanced position mapping for IDP players

## Sample Output
```
================================================================================
GRUNDLE LEAGUE DRAFT ANALYSIS - 2024 DRAFT DATA
League: Grundle
Current Season: 2025
Analysis Date: 2025-08-19
================================================================================

TEAM                 DRAFTED  UNDRAFTED  EARLIEST   LATEST   TOTAL 
--------------------------------------------------------------------------------
5 Fingers 2 Ur Face  15       4          #1         #172     19    
Big Ol' TDs          10       3          #5         #173     13    
Bo Derek Henry V     11       6          #2         #181     17    
...
```

This tool provides comprehensive insight into how well teams retained their drafted players and the draft capital represented on current rosters.
