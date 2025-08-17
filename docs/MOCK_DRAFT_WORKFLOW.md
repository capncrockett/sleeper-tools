# Mock Draft Workflow for Keeper League ADP

## 🎯 Your Strategy
1. **Wait for keepers to be set** (3 days before real draft)
2. **Run 50+ mock drafts** manually on Sleeper
3. **Import all mock drafts** using our system
4. **Generate custom ADP** with keeper adjustments
5. **Dominate your draft** with data-driven picks

## 📱 How to Run Mock Drafts on Sleeper

### Step 1: Access Mock Drafts
- Open Sleeper app or go to sleeper.app
- Look for **"Mock Draft"** or **"Practice Draft"** option
- Usually found in the main menu or draft section

### Step 2: Mock Draft Settings
- **League Size:** Match your real league (likely 12 teams)
- **Scoring:** Match your league settings (PPR/Half-PPR/Standard)
- **Rounds:** Match your real draft (likely 15-16 rounds)
- **Draft Type:** Snake (most common)

### Step 3: Run Multiple Mocks
- **Target:** 50+ mock drafts for reliable ADP
- **Timing:** After keepers are locked in
- **Focus:** Different draft positions to see full ADP range

## 🔄 Import Workflow

Once you've run mock drafts, use our system:

### Option 1: Automatic Import
```bash
source venv/bin/activate
python3 find_mock_drafts_only.py
```

### Option 2: Manual Import by Draft ID
```bash
source venv/bin/activate
python3 sleeper_mock_importer.py
```

## 📊 What You'll Get

### ADP Analysis
- **Average Draft Position** for each player
- **Draft Percentage** (how often drafted)
- **Pick Range** (earliest to latest)
- **Standard Deviation** (consistency)
- **Keeper-Adjusted Rankings**

### Export Options
- **CSV file** for draft day reference
- **Sortable by any metric**
- **Position-specific analysis**

## 🎯 Strategic Benefits

### Value Identification
- **Consistent Early Picks** → Avoid reaches
- **High Variance Players** → Target in later rounds  
- **Keeper Impact** → See true scarcity

### Draft Day Edge
- **Custom Rankings** based on YOUR mock data
- **Keeper Adjustments** built into ADP
- **League-Specific Trends** vs generic ADP

## 📋 Mock Draft Checklist

### Before Each Mock Session
- [ ] Keepers are finalized in your league
- [ ] Mock draft settings match your real league
- [ ] You have time to run multiple mocks

### During Mock Drafts
- [ ] Try different draft positions (early, middle, late)
- [ ] Note any unusual picks or trends
- [ ] Save draft IDs if needed for manual import

### After Mock Session
- [ ] Import all completed mock drafts
- [ ] Review ADP changes as you add data
- [ ] Export updated CSV for draft prep

## 🚀 Ready to Execute

Your custom ADP system is **fully built and ready**. The moment you start running mock drafts on Sleeper, you can:

1. **Import them instantly** with our tools
2. **Calculate custom ADP** with keeper adjustments  
3. **Export rankings** for draft day
4. **Gain massive advantage** over standard ADP users

**The system is waiting for your mock draft data - go run some mocks and let's build your custom ADP!**
