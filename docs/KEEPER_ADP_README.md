# Custom Keeper League ADP System

A comprehensive tool for calculating Average Draft Position (ADP) in keeper fantasy football leagues, where standard ADP doesn't account for keepers being off the board.

## 🎯 Purpose

In keeper leagues, players are kept at the round they were drafted the previous year, causing most players to get bumped up ~1-2 rounds. This makes standard ADP unreliable. This system lets you run 50+ mock drafts after keepers are set and calculate your own custom ADP data.

## 📁 Files Overview

### Core System Files
- **`mock_draft_tracker.py`** - Main ADP calculation engine
- **`sleeper_mock_importer.py`** - Import drafts from Sleeper API
- **`demo_adp_system.py`** - Demo showing system capabilities

### Existing Integration
- **`sleeper_api.py`** - Your existing Sleeper API wrapper
- **`data_analysis.py`** - Your existing draft analysis tools

## 🚀 Quick Start

### Method 1: Manual Draft Entry
```bash
python3 mock_draft_tracker.py
```
- Choose option 1 to add new mock draft
- Enter draft details and picks manually
- Export ADP to CSV when ready

### Method 2: Import from Sleeper
```bash
python3 sleeper_mock_importer.py
```
- Import completed mock drafts by Draft ID
- Or find recent drafts by username
- Automatically processes player data

### Method 3: See Demo
```bash
python3 demo_adp_system.py
```
- Shows sample data and analysis
- Creates demo CSV export
- Demonstrates all features

## 📊 Key Features

### ADP Calculation
- **Average Draft Position** - Mean pick across all drafts
- **Draft Percentage** - How often player is drafted
- **Pick Range** - Earliest to latest pick
- **Standard Deviation** - Consistency of draft position
- **Median Pick** - Middle value for skewed data

### Data Export
- CSV format with rankings
- Sortable by any metric
- Perfect for draft day reference

### Keeper Integration
- Track which players are keepers (off the board)
- Calculate ADP with keepers removed
- See true positional scarcity

## 📈 Workflow for Your League

### Phase 1: Data Collection (3 days before draft)
1. **Set Keepers** - Wait for league keepers to be locked
2. **Run Mock Drafts** - Manually run 50+ mocks on Sleeper
3. **Import Data** - Use `sleeper_mock_importer.py` to import results
4. **Export ADP** - Generate CSV for draft day

### Phase 2: Draft Preparation
1. **Analyze Trends** - Look for consistent early/late picks
2. **Identify Value** - Find players with high variance
3. **Plan Strategy** - Target undervalued players
4. **Reference Sheet** - Use CSV during actual draft

## 🔧 Advanced Usage

### Custom Analysis
```python
from mock_draft_tracker import MockDraftTracker

tracker = MockDraftTracker()
adp_data = tracker.calculate_adp()

# Find players drafted in rounds 3-5
mid_round_players = {
    name: data for name, data in adp_data.items()
    if 25 <= data['average_pick'] <= 60
}
```

### Player-Specific Analysis
```python
# Analyze specific player
analysis = tracker.get_player_analysis("Ja'Marr Chase")
print(f"ADP: {analysis['average_pick']}")
print(f"Range: {analysis['earliest_pick']}-{analysis['latest_pick']}")
```

## 📋 Data Structure

### Mock Draft Format
```json
{
  "draft_id": "mock_20240814_1430",
  "draft_date": "2024-08-14T14:30:00",
  "league_size": 12,
  "rounds": 16,
  "keepers": ["Christian McCaffrey", "Josh Allen"],
  "picks": [
    {
      "player_name": "Ja'Marr Chase",
      "position": "WR",
      "team": "CIN",
      "round_num": 1,
      "pick_num": 1,
      "overall_pick": 1,
      "drafted_by_team": "Team1"
    }
  ]
}
```

### ADP Output Format
```csv
rank,player_name,times_drafted,draft_percentage,average_pick,median_pick,earliest_pick,latest_pick,std_dev
1,Ja'Marr Chase,50,100.0%,1.2,1,1,3,0.6
2,Austin Ekeler,48,96.0%,2.1,2,1,4,0.8
```

## 🎯 Strategic Benefits

### Value Identification
- **Consistent Early Picks** - Avoid reaches
- **High Variance Players** - Target in later rounds
- **Position Scarcity** - See true availability after keepers

### Draft Day Advantages
- **Custom Rankings** - Based on YOUR league's tendencies
- **Keeper Adjustments** - Account for players off the board
- **Variance Data** - Know when to reach vs. wait

## 🔮 Next Steps (Planned)

### Phase 2: Web Interface
- Vite-based web application
- Interactive data visualization
- Real-time ADP updates
- Mobile-friendly design

### Phase 3: Advanced Analytics
- Position-based ADP
- Tier analysis
- Value over replacement
- Draft simulation

## 💡 Tips for Success

1. **Run Many Mocks** - 50+ drafts for reliable data
2. **Consistent Settings** - Same scoring, roster size
3. **Recent Data** - Focus on drafts close to your real draft
4. **Track Variance** - High std dev = opportunity for value
5. **Update Regularly** - Re-run analysis as you add more mocks

## 🛠 Technical Details

### Requirements
- Python 3.7+
- requests
- python-dotenv
- statistics (built-in)

### File Storage
- JSON format for draft data
- Automatic backup on each save
- Human-readable structure

### Error Handling
- Graceful API failures
- Data validation
- Recovery from corrupted files

---

## 🏆 Ready to Dominate Your Keeper League!

Your custom ADP system gives you a massive advantage by accounting for the unique dynamics of keeper leagues. Standard ADP can't compete with data tailored specifically to your league's keeper selections and draft tendencies.

**Start collecting mock draft data now and watch your draft day performance improve!**
