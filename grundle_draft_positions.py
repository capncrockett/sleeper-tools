#!/usr/bin/env python3
"""
Grundle Draft Positions Tool

This script retrieves the 2024 draft positions of all players currently on rosters
in the Grundle league, providing detailed analysis of draft value and roster composition.
"""

import os
import sys
import json
import csv
from datetime import datetime
from dotenv import load_dotenv
from sleeper_api import SleeperAPI

load_dotenv()

class GrundleDraftAnalyzer:
    def __init__(self, username):
        """Initialize the analyzer with a Sleeper username."""
        self.api = SleeperAPI(username)
        self.username = username
        self.season = '2025'  # Current season for roster data
        self.draft_season = '2024'  # Season we want draft data from
        self.league_data = None
        self.roster_data = None
        self.draft_data = None
        self.players_data = None
        
    def find_grundle_league(self):
        """Find the Grundle league for the current season."""
        print(f"Looking for Grundle league in {self.season}...")
        leagues = self.api.get_leagues(self.season)
        
        if not leagues:
            print(f"No leagues found for {self.username} in {self.season}")
            return None
            
        # Look for Grundle league
        grundle_league = None
        for league in leagues:
            if 'grundle' in league['name'].lower():
                grundle_league = league
                break
                
        if grundle_league:
            print(f"Found Grundle league: {grundle_league['name']}")
            return grundle_league
        else:
            print("Grundle league not found. Available leagues:")
            for i, league in enumerate(leagues, 1):
                print(f"  {i}. {league['name']}")
            return None
    
    def get_league_rosters(self, league_id):
        """Get all rosters for the league."""
        print("Fetching current rosters...")
        rosters = self.api.get_rosters(league_id)
        users = self.api.get_league_users(league_id)
        
        if not rosters or not users:
            print("Failed to retrieve roster or user data")
            return None
            
        # Create user mapping
        user_map = {user['user_id']: user for user in users}
        
        return {'rosters': rosters, 'users': user_map}
    
    def get_2024_draft_data(self):
        """Get draft data specifically from 2024."""
        print(f"Looking for {self.draft_season} draft data...")
        
        # Get all drafts from 2024
        drafts = self.api.get_all_drafts(self.draft_season)
        
        if not drafts:
            print(f"No drafts found for {self.draft_season}")
            return None
            
        print(f"Found {len(drafts)} draft(s) from {self.draft_season}")
        
        # Find drafts that are completed
        completed_drafts = [d for d in drafts if d.get('status') == 'complete']
        
        if not completed_drafts:
            print("No completed drafts found")
            return None
            
        # Use the most recent completed draft
        latest_draft = max(completed_drafts, key=lambda x: x.get('last_picked', 0))
        draft_id = latest_draft['draft_id']
        
        print(f"Using draft: {latest_draft.get('metadata', {}).get('name', 'Unknown')} (ID: {draft_id})")
        
        # Get all draft picks
        picks = self.api.get_draft_picks(draft_id)
        
        if picks:
            print(f"Retrieved {len(picks)} draft picks")
            return picks
        else:
            print("No draft picks found")
            return None
    
    def get_all_players(self):
        """Get all player data for lookups."""
        print("Loading player database...")
        players = self.api.get_players()
        
        if players:
            print(f"Loaded {len(players)} players")
            return players
        else:
            print("Failed to load player data")
            return None
    
    def analyze_rosters_with_draft_data(self):
        """Main analysis function that combines current rosters with 2024 draft data."""
        # Find Grundle league
        league = self.find_grundle_league()
        if not league:
            return None
            
        self.league_data = league
        league_id = league['league_id']
        
        # Get current roster data
        self.roster_data = self.get_league_rosters(league_id)
        if not self.roster_data:
            return None
            
        # Get 2024 draft data
        self.draft_data = self.get_2024_draft_data()
        if not self.draft_data:
            print("Warning: No draft data available. Players will show as 'Undrafted'")
            self.draft_data = []
            
        # Get player data
        self.players_data = self.get_all_players()
        if not self.players_data:
            return None
            
        # Create draft pick mapping
        draft_pick_map = {}
        for pick in self.draft_data:
            if pick.get('player_id'):
                draft_pick_map[pick['player_id']] = {
                    'round': pick.get('round', 'N/A'),
                    'pick': pick.get('pick_no', 'N/A'),
                    'overall': pick.get('pick_no', 'N/A')
                }
        
        # Analyze each roster
        analysis_results = []
        
        for roster in self.roster_data['rosters']:
            owner_id = roster.get('owner_id')
            if not owner_id:
                continue
                
            owner_info = self.roster_data['users'].get(owner_id, {})
            owner_name = owner_info.get('display_name', 'Unknown Owner')
            team_name = owner_info.get('metadata', {}).get('team_name', owner_name)
            
            players_on_roster = roster.get('players', [])
            
            roster_analysis = {
                'owner_id': owner_id,
                'owner_name': owner_name,
                'team_name': team_name,
                'players': [],
                'stats': {
                    'total_players': len(players_on_roster),
                    'drafted_players': 0,
                    'undrafted_players': 0,
                    'earliest_pick': float('inf'),
                    'latest_pick': 0,
                    'total_draft_picks': 0
                }
            }
            
            for player_id in players_on_roster:
                player_info = self.players_data.get(player_id, {})
                draft_info = draft_pick_map.get(player_id, {'round': 'N/A', 'pick': 'N/A', 'overall': 'N/A'})
                
                # Get position info
                position = player_info.get('position', 'N/A')
                if position in ['DL', 'LB', 'DB'] and 'fantasy_positions' in player_info:
                    fantasy_pos = player_info.get('fantasy_positions', [])
                    if fantasy_pos:
                        position = fantasy_pos[0]
                
                player_data = {
                    'id': player_id,
                    'name': player_info.get('full_name', 'Unknown Player'),
                    'position': position,
                    'nfl_team': player_info.get('team', 'FA'),
                    'draft_round': draft_info['round'],
                    'draft_pick': draft_info['pick'],
                    'overall_pick': draft_info['overall'],
                    'drafted': draft_info['round'] != 'N/A'
                }
                
                roster_analysis['players'].append(player_data)
                
                # Update stats
                if player_data['drafted']:
                    roster_analysis['stats']['drafted_players'] += 1
                    pick_num = int(draft_info['overall']) if draft_info['overall'] != 'N/A' else float('inf')
                    roster_analysis['stats']['earliest_pick'] = min(roster_analysis['stats']['earliest_pick'], pick_num)
                    roster_analysis['stats']['latest_pick'] = max(roster_analysis['stats']['latest_pick'], pick_num)
                    roster_analysis['stats']['total_draft_picks'] += 1
                else:
                    roster_analysis['stats']['undrafted_players'] += 1
            
            # Clean up stats
            if roster_analysis['stats']['earliest_pick'] == float('inf'):
                roster_analysis['stats']['earliest_pick'] = 'N/A'
                
            # Sort players by draft position (drafted first, then by pick number)
            roster_analysis['players'].sort(key=lambda x: (
                not x['drafted'],  # False (drafted) sorts before True (undrafted)
                float('inf') if x['overall_pick'] == 'N/A' else int(x['overall_pick']),
                x['name']
            ))
            
            analysis_results.append(roster_analysis)
        
        # Sort teams by owner name
        analysis_results.sort(key=lambda x: x['owner_name'])
        
        return {
            'league_name': league['name'],
            'season': self.season,
            'draft_season': self.draft_season,
            'analysis_date': datetime.now().isoformat(),
            'teams': analysis_results
        }

def display_summary_table(data):
    """Display a summary table of draft analysis."""
    if not data:
        print("No data to display")
        return
        
    print(f"\n{'='*80}")
    print(f"GRUNDLE LEAGUE DRAFT ANALYSIS - {data['draft_season']} DRAFT DATA")
    print(f"League: {data['league_name']}")
    print(f"Current Season: {data['season']}")
    print(f"Analysis Date: {data['analysis_date'][:10]}")
    print(f"{'='*80}")
    
    # Team summary
    print(f"\n{'TEAM':<20} {'DRAFTED':<8} {'UNDRAFTED':<10} {'EARLIEST':<10} {'LATEST':<8} {'TOTAL':<6}")
    print("-" * 80)
    
    total_drafted = 0
    total_undrafted = 0
    
    for team in data['teams']:
        stats = team['stats']
        earliest = f"#{stats['earliest_pick']}" if stats['earliest_pick'] != 'N/A' else 'N/A'
        latest = f"#{stats['latest_pick']}" if stats['latest_pick'] > 0 else 'N/A'
        
        print(f"{team['team_name'][:19]:<20} {stats['drafted_players']:<8} {stats['undrafted_players']:<10} "
              f"{earliest:<10} {latest:<8} {stats['total_players']:<6}")
        
        total_drafted += stats['drafted_players']
        total_undrafted += stats['undrafted_players']
    
    print("-" * 80)
    print(f"{'TOTALS':<20} {total_drafted:<8} {total_undrafted:<10} {'N/A':<10} {'N/A':<8} {total_drafted + total_undrafted:<6}")

def display_detailed_rosters(data):
    """Display detailed roster information with draft positions."""
    if not data:
        print("No data to display")
        return
        
    print(f"\n{'='*100}")
    print("DETAILED ROSTER ANALYSIS")
    print(f"{'='*100}")
    
    for team in data['teams']:
        print(f"\n--- {team['team_name']} ({team['owner_name']}) ---")
        print(f"{'PLAYER':<30} {'POS':<4} {'NFL':<4} {'ROUND':<6} {'PICK':<6} {'OVERALL':<8}")
        print("-" * 70)
        
        for player in team['players']:
            round_str = f"R{player['draft_round']}" if player['draft_round'] != 'N/A' else 'Undrafted'
            pick_str = f"P{player['draft_pick']}" if player['draft_pick'] != 'N/A' else ''
            overall_str = f"#{player['overall_pick']}" if player['overall_pick'] != 'N/A' else ''
            nfl_team = player['nfl_team'] if player['nfl_team'] is not None else 'FA'
            
            print(f"{player['name'][:29]:<30} {player['position']:<4} {nfl_team:<4} "
                  f"{round_str:<6} {pick_str:<6} {overall_str:<8}")

def save_to_csv(data, filename):
    """Save analysis data to CSV file."""
    if not data:
        print("No data to save")
        return False
        
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['team_name', 'owner_name', 'player_name', 'position', 'nfl_team', 
                         'draft_round', 'draft_pick', 'overall_pick', 'drafted']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for team in data['teams']:
                for player in team['players']:
                    writer.writerow({
                        'team_name': team['team_name'],
                        'owner_name': team['owner_name'],
                        'player_name': player['name'],
                        'position': player['position'],
                        'nfl_team': player['nfl_team'],
                        'draft_round': player['draft_round'],
                        'draft_pick': player['draft_pick'],
                        'overall_pick': player['overall_pick'],
                        'drafted': player['drafted']
                    })
        
        print(f"Data saved to {filename}")
        return True
        
    except Exception as e:
        print(f"Error saving CSV file: {e}")
        return False

def save_to_json(data, filename):
    """Save analysis data to JSON file."""
    if not data:
        print("No data to save")
        return False
        
    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Data saved to {filename}")
        return True
        
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return False

def main():
    """Main function to run the analysis."""
    # Check for username
    username = os.getenv('SLEEPER_USERNAME')
    if not username:
        print("Error: SLEEPER_USERNAME environment variable not set.")
        print("Please set it in your .env file or environment.")
        return
    
    print(f"Starting Grundle draft analysis for user: {username}")
    
    try:
        # Initialize analyzer
        analyzer = GrundleDraftAnalyzer(username)
        
        # Run analysis
        results = analyzer.analyze_rosters_with_draft_data()
        
        if not results:
            print("Failed to complete analysis")
            return
            
        # Display results
        while True:
            print("\n" + "="*60)
            print("GRUNDLE DRAFT ANALYSIS MENU")
            print("="*60)
            print("1. Show summary table")
            print("2. Show detailed rosters")
            print("3. Save to CSV")
            print("4. Save to JSON") 
            print("5. Show both summary and details")
            print("6. Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                display_summary_table(results)
            elif choice == '2':
                display_detailed_rosters(results)
            elif choice == '3':
                filename = f"grundle_draft_analysis_{results['draft_season']}.csv"
                save_to_csv(results, filename)
            elif choice == '4':
                filename = f"grundle_draft_analysis_{results['draft_season']}.json"
                save_to_json(results, filename)
            elif choice == '5':
                display_summary_table(results)
                display_detailed_rosters(results)
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")
                
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
