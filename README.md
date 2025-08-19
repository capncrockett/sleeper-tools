# Custom Keeper League ADP System & Draft Tools

A comprehensive tool for calculating Average Draft Position (ADP) in keeper fantasy football leagues and providing an interactive keeper draft board.

## ✨ Features

### 1. Custom ADP Calculator
Calculates ADP in keeper leagues where standard ADP doesn't account for players being kept.

### 2. Interactive Keeper Draft Board
A web-based tool to help you prepare for your keeper league draft.
- Fetches your league's rosters from the previous season.
- Displays player details and their original draft position.
- Allows you to select which players you think will be kept.
- Generates a dynamic, editable draft board based on your selections.
- Supports drag-and-drop reordering of keepers to create your own rankings.

## 🚀 Quick Start

### For the Web Application (Keeper Tool & ADP Viewer)

1.  **Set up Backend Environment:**
    
    - **Create and activate a virtual environment (recommended):**
      ```bash
      # Create virtual environment
      python -m venv venv
      
      # Activate it (Windows)
      source venv/Scripts/activate
      
      # Activate it (macOS/Linux)
      source venv/bin/activate
      ```
    
    - **Install Python dependencies:**
      ```bash
      pip install -r requirements.txt
      ```
    
    - **Create a `.env` file** in the root directory with your Sleeper username:
      ```
      SLEEPER_USERNAME=your_username_here
      ```

2.  **Set up Frontend Environment:**
    - Navigate to the `frontend` directory:
      ```bash
      cd frontend
      ```
    - Install Node.js dependencies:
      ```bash
      npm install
      ```
    - Go back to the root directory:
      ```bash
      cd ..
      ```

3.  **Run the Application:**
    - **Start the Backend API:** Open a terminal in the root directory and run:
      ```bash
      python api.py
      ```
    - **Start the Frontend App:** Open a *second* terminal, navigate to `frontend`, and run:
      ```bash
      npm run dev
      ```
    - Open your browser to the local URL provided (usually `http://localhost:5173`).

### For the Command-Line ADP Calculator

1.  **Import mock drafts:**
    ```bash
    python3 import_mock_drafts.py
    ```

2.  **Generate ADP:**
    - The system automatically calculates ADP from imported drafts.
    - It exports to `eleveners_2025_mock_adp.csv` for your reference.

## 🎯 Core Files

- **`api.py`** - Flask backend for the web application.
- **`keeper_tool.py`** - Logic for fetching keeper data.
- **`mock_draft_tracker.py`** - Main ADP calculation engine.
- **`sleeper_mock_importer.py`** - Sleeper API integration for importing drafts.
- **`sleeper_api.py`** - Core Sleeper API wrapper.
- **`frontend/`** - Contains the React frontend application.
