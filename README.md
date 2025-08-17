# Custom Keeper League ADP System

A comprehensive tool for calculating Average Draft Position (ADP) in keeper fantasy football leagues, where standard ADP doesn't account for keepers being off the board.

## 🎯 Core Files

- **`mock_draft_tracker.py`** - Main ADP calculation engine
- **`sleeper_mock_importer.py`** - Sleeper API integration for importing drafts
- **`import_mock_drafts.py`** - Import specific mock drafts by ID
- **`sleeper_api.py`** - Core Sleeper API wrapper
- **`data_analysis.py`** - Draft analysis tools

## 📊 Generated Data

- **`eleveners_2025_mock_adp.csv`** - Your custom ADP export
- **`mock_drafts.json`** - All imported mock draft data

## 📁 Organization

- **`docs/`** - Documentation and workflow guides
- **`scripts/experimental/`** - Various API search attempts
- **`scripts/utilities/`** - Helper and testing scripts

## 🚀 Quick Start

1. **Set up environment:**
   ```bash
   # Create .env file with:
   SLEEPER_USERNAME=your_username_here
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Import mock drafts:**
   ```bash
   python3 import_mock_drafts.py
   ```

4. **Generate ADP:**
   - System automatically calculates ADP from imported drafts
   - Exports to CSV for draft day reference

## 📈 Current Status

✅ **5 mock drafts imported** from 11:59ers league  
✅ **Custom ADP calculated** with variance analysis  
✅ **CSV export ready** for draft day  
🔄 **Web interface** - Next phase

## 🎯 Key Insights

- **Ja'Marr Chase** - ADP 1.6 (most consistent top pick)
- **Saquon Barkley** - ADP 1.8 (most common 1.01, but variable)
- **175 players tracked** across 840 total picks
- **100% draft rate** for top 20 players shows league consistency
