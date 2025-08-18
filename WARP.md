# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Overview

This is a Python/React fantasy football toolkit that calculates custom Average Draft Position (ADP) for keeper leagues and provides an interactive keeper draft board. The system integrates with the Sleeper fantasy platform API to import mock draft data and analyze league rosters.

## Core Architecture

### Backend Structure
- **Flask API (`api.py`)**: RESTful backend serving two main endpoints
  - `/api/adp` - Returns calculated ADP data from CSV
  - `/api/keeper-data` - Returns league roster data from Sleeper API
- **Sleeper API Integration (`sleeper_api.py`)**: Unified wrapper class for all Sleeper API calls
- **Mock Draft System** (`mock_draft_tracker.py`): Core ADP calculation engine with statistical analysis
- **Data Import Pipeline** (`sleeper_mock_importer.py`): Automated import from Sleeper API to local data structures

### Frontend Structure
- **React/Vite Application**: Two-view SPA with view toggle
  - ADP View: Sortable table with search functionality
  - Keeper Tool: Interactive roster selection with drag-and-drop draft board generation
- **Component Architecture**: 
  - `App.jsx` - Main container with view routing
  - `KeeperTool.jsx` - Roster selection interface
  - `DraftBoard.jsx` - Generated draft board with drag-and-drop

### Data Flow
1. Mock drafts → Sleeper API → Import scripts → JSON storage → ADP calculation → CSV export
2. League rosters → Sleeper API → Flask backend → React frontend → Interactive selection

## Development Commands

### Environment Setup
```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies  
cd frontend && npm install && cd ..

# Environment configuration
# Create .env file with: SLEEPER_USERNAME=your_username_here
```

### Running the Application
```bash
# Start Flask backend (Terminal 1)
python api.py

# Start React frontend (Terminal 2) 
cd frontend && npm run dev
```

### Mock Draft Data Management
```bash
# Import specific mock drafts (for 11:59ers league)
python import_mock_drafts.py

# Interactive mock draft import from Sleeper
python sleeper_mock_importer.py

# Manual mock draft entry and ADP calculation
python mock_draft_tracker.py

# Analyze existing league draft results
python data_analysis.py
```

### Frontend Development
```bash
cd frontend

# Development server with hot reload
npm run dev

# Production build
npm build

# Linting
npm run lint

# Preview production build
npm run preview
```

### Testing
```bash
cd frontend

# Run Playwright end-to-end tests
npx playwright test

# Check system readiness
python scripts/utilities/test_system_ready.py

# Inspect draft data
python scripts/utilities/inspect_draft_data.py
```

## Key Implementation Details

### ADP Calculation Engine
The `MockDraftTracker` class implements statistical analysis across multiple draft scenarios:
- Uses dataclass structures (`DraftPick`, `MockDraft`) for type safety
- Calculates mean, median, standard deviation, and draft percentage
- JSON persistence with datetime serialization
- Configurable minimum draft requirements for reliability

### Sleeper API Integration
The `SleeperAPI` class provides a stateful wrapper around the Sleeper REST API:
- Automatic user ID resolution from username
- Error handling with graceful degradation
- Support for multi-season data retrieval
- Player data caching and normalization

### Keeper League Logic
The system handles keeper league complexities:
- Draft position adjustment for kept players
- Multi-season roster data retrieval
- Flexible keeper selection interface
- Dynamic draft board generation accounting for removed players

### React State Management
Frontend uses React hooks for state management:
- `useState` for component state (search, sorting, keeper selection)
- `useEffect` for API data fetching
- `useMemo` for performance optimization of filtered/sorted data
- Drag-and-drop state management via react-beautiful-dnd

## File Organization

### Core Application Files
- `api.py` - Flask backend server
- `keeper_tool.py` - Keeper data fetching logic
- `mock_draft_tracker.py` - ADP calculation engine
- `sleeper_api.py` - Sleeper API wrapper
- `sleeper_mock_importer.py` - Automated draft import
- `import_mock_drafts.py` - Specific league import script

### Frontend Application
- `frontend/src/App.jsx` - Main application component
- `frontend/src/KeeperTool.jsx` - Keeper selection interface  
- `frontend/src/DraftBoard.jsx` - Draft board generation
- `frontend/package.json` - Dependencies and scripts

### Utility Scripts
- `scripts/utilities/` - System testing and data inspection tools
- `scripts/experimental/` - Draft discovery and API exploration scripts
- `data_analysis.py` - League draft analysis tools

### Documentation
- `docs/KEEPER_ADP_README.md` - Detailed system documentation
- `docs/MOCK_DRAFT_WORKFLOW.md` - Usage workflow guide

## Configuration Notes

- Environment variables in `.env` file (required: `SLEEPER_USERNAME`)
- Flask backend runs on port 5001 by default
- Vite dev server typically runs on port 5173
- CORS configured for local development
- Mock draft data stored in `mock_drafts.json`
- ADP exports to `eleveners_2025_mock_adp.csv`

## Common Development Patterns

- API error handling follows try/catch with user-friendly messages
- React components use functional components with hooks
- Data fetching uses modern fetch API with async/await
- CSV export includes rank calculation and percentage formatting
- Draft data uses 1-indexed pick numbers consistently
- Player names normalized as "FirstName LastName" format

