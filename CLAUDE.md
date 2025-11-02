# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fantasy Tour de France 2025 is a Streamlit web application that displays real-time fantasy cycling competition results by fetching data from the procyclingstats API. The app automatically calculates fantasy team scores based on real professional rider performance. It features a Tour de France themed interface with yellow jersey leader styling, stage-by-stage analysis charts, and comprehensive progress tracking.

## Running the Application

### Start Development Server
```bash
streamlit run app.py --server.port 5000
```

The app will be available at `http://localhost:5000`

### Auto-refresh Feature
The app automatically refreshes data every 5 minutes using Streamlit's caching mechanism with TTL (Time-To-Live).

## Data Architecture

### Procyclingstats API Integration

The app fetches real race data from procyclingstats.com using the `procyclingstats` Python package:

**How Fantasy Scoring Works:**
- Each fantasy team consists of 3-8 professional riders (configured in `team_config.py`)
- Team score = Sum of all riders' cumulative times from the General Classification (GC)
- Lower total time = Better score (like real cycling)
- Only active riders count (DNF/DNS riders are marked but excluded from totals)

### Configuration Files

1. **team_config.py**: Team roster configuration
   ```python
   TEAM_ROSTERS = {
       "Jeremy": ["rider/sepp-kuss", "rider/jhonatan-narvaez", ...],
       "Leo": ["rider/felix-gall", "rider/kevin-vauquelin", ...],
       # ... other teams
   }

   RACE_CONFIG = {
       "race_url": "race/tour-de-france/2025",
       "race_name": "Tour de France 2025",
       "total_stages": 21
   }
   ```
   - Rider URLs follow format: `"rider/firstname-lastname"`
   - Find riders on procyclingstats.com and copy URL path
   - Easy to update for different races or seasons

2. **api_client.py**: API interaction layer
   - `fetch_fantasy_standings()`: Get current standings with calculated team scores
   - `fetch_stage_by_stage_data()`: Get historical data for all stages (charts)
   - `fetch_stage_gc()`: Get General Classification for a specific stage
   - `calculate_team_time()`: Sum rider times for each fantasy team
   - All functions use Streamlit `@st.cache_data` with 5-minute TTL

### Time Conversion System

The app uses a two-way conversion system for time calculations:

- `time_str_to_seconds()` (api_client.py): Converts `H:MM:SS` or `HH:MM:SS` strings to integer seconds
- `seconds_to_time_str()` (api_client.py): Converts seconds back to human-readable format
- `calculate_time_gap()` (app.py): Computes time differences relative to the leader

This allows for accurate gap calculations and proper sorting/ranking.

### Data Flow

1. **Fetch GC Data**: For each stage, scrape General Classification from procyclingstats.com
2. **Calculate Team Scores**: Sum cumulative times for all riders on each fantasy team
3. **Sort Teams**: Rank teams by total time (ascending - lower is better)
4. **Calculate Gaps**: Compute time gaps from leader
5. **Display**: Show standings, charts, and rider details in UI
6. **Caching**: All API responses cached for 5 minutes via Streamlit decorators

## Competition Configuration

The app has a configuration-based system for toggling between active and completed competition states:

```python
COMPETITION_CONFIG = {
    "is_complete": True,          # Toggle competition completion status
    "winner_name": "Aaron",        # Name of winner (shown when complete)
    "competition_name": "Tour de France 2025",
    "total_stages": 21,
    "completion_date": "July 27, 2025",
    "show_celebration": True       # Toggle winner celebration banner
}
```

Located at app.py:89. This allows easy reuse for future competitions (e.g., Tour de France 2026) by simply updating these values.

## UI Components and Features

### Three-Tab Navigation System

1. **🏆 Current Standings**: Main leaderboard with yellow jersey styling for the leader
2. **📊 Stage Analysis**: Interactive Plotly charts showing:
   - Cumulative Time Progression (line chart)
   - Individual Stage Performance (bar chart)
   - Gap Evolution Analysis (line chart tracking gaps over time)
3. **👥 Team Riders**: Shows each participant's drafted professional riders with team-colored cards

### Dark Mode Theme

The app uses a dark-only theme (no toggle):
- Background: `#1e1e1e`
- Cards: `#2d2d2d`
- Text: White with high contrast
- Leader styling: Yellow jersey gold (`#FFD700`) optimized for dark backgrounds

All CSS is embedded in the Streamlit app using `st.markdown()` with `unsafe_allow_html=True`.

### Winner Celebration System

When `COMPETITION_CONFIG["is_complete"] = True`:
- `create_winner_banner()` function (app.py:131) displays an animated gold gradient banner
- Leader card shows "🏆 CHAMPION" instead of "LEADER"
- Page title shows "COMPLETE ✅" status
- Confetti animation and pulsing effects

### Responsive Design

The app includes comprehensive mobile responsiveness:
- CSS media queries for tablets (≤768px) and phones (≤480px)
- Touch-friendly 44px minimum touch targets
- Adaptive column layouts that stack vertically on mobile
- Disabled hover effects on touch devices
- Optimized typography and chart scaling for small screens

### Social Media Sharing

Open Graph, Twitter Cards, and Schema.org metadata are embedded in the HTML head (app.py:18-70) for rich link previews when sharing the app URL via text message or social media.

## Key Functions and Data Flow

1. **API Data Retrieval**: Fetch General Classification data from procyclingstats.com via Stage API
2. **Team Score Calculation**: Sum cumulative times for all riders on each fantasy team
3. **Time Conversion**: Convert time strings to seconds for calculations and comparisons
4. **Gap Calculation**: Calculate time differences relative to leader
5. **Display Formatting**: Convert back to human-readable format for UI display
6. **Caching**: All API responses and processed data cached for 5 minutes via Streamlit decorators
7. **Rider Details**: Show individual rider GC positions and times in Team Riders tab

## Dependencies

Core packages (listed in `requirements.txt`):
- `streamlit`: Web framework and UI components
- `pandas`: Data manipulation and analysis
- `plotly`: Interactive charting library for stage analysis
- `procyclingstats`: Python package for scraping procyclingstats.com race data

Install with:
```bash
pip install -r requirements.txt
```

Or individually:
```bash
pip install streamlit pandas plotly procyclingstats
```

## Deployment Platforms

The app is designed for easy deployment on:
- **Streamlit Cloud**: Recommended, native integration
- **Replit**: Direct Python execution (see `replit.md` for deployment history)
- **Heroku**: Container-based deployment
- **Local**: Run with `streamlit run app.py --server.port 5000`

No database required - procyclingstats.com serves as the data source via API scraping.

## File Structure

**Core Application Files:**
- `app.py`: Main Streamlit application (UI and display logic)
- `api_client.py`: API integration layer (data fetching and processing)
- `team_config.py`: Team roster and race configuration

**Configuration & Requirements:**
- `requirements.txt`: Python package dependencies
- `config.toml`: Streamlit server configuration

**Documentation:**
- `README.md`: User-facing documentation
- `CLAUDE.md`: This file - project guidance for Claude Code
- `MIGRATION_GUIDE.md`: Complete guide for Google Sheets → API migration
- `GOOGLE_SHEETS_FORMAT.md`: Legacy Google Sheets data format (deprecated)
- `BACKUP_STEPS.md`: Git backup instructions for Replit
- `replit.md`: Comprehensive development history and system architecture notes

**Testing Files:**
- `test_integration.py`: Integration test for API client
- `test_api.py`: API exploration and testing
- `test_gc_data.py`: GC data structure exploration

## Important Notes

- **Automatic Scoring**: Fantasy team scores are calculated automatically from real race data
- **No Manual Data Entry**: All race results are fetched from procyclingstats.com
- **Config-Based Teams**: Team rosters are defined in `team_config.py` (Phase 1)
- **Future Enhancement**: Phase 2 will add web UI for team roster selection
- **No Authentication**: No database or authentication required for Phase 1
- **Data Availability**: Race data only available for races that have started/completed
- **API Updates**: The `procyclingstats` package may need updates if website structure changes
- **Caching**: 5-minute cache TTL balances performance and data freshness
- **The competition tracks 5 participants across 21 stages of the Tour de France**
- **User prefers simple, everyday language (noted in replit.md:9)**

## Testing

Run integration tests to verify API connection and data fetching:

```bash
# Test API integration
python3 test_integration.py

# Expected output: Current standings with team scores
```

## Configuration Updates

### To change team rosters:
Edit `team_config.py` and update the `TEAM_ROSTERS` dictionary with rider URLs from procyclingstats.com

### To use a different race:
Edit `team_config.py` and update `RACE_CONFIG`:
```python
RACE_CONFIG = {
    "race_url": "race/giro-d-italia/2026",
    "race_name": "Giro d'Italia 2026",
    "total_stages": 21
}
```

## Migration History

**November 2025**: Migrated from Google Sheets to procyclingstats API
- Replaced manual data entry with automatic API fetching
- Added `api_client.py` for API interactions
- Created `team_config.py` for roster configuration
- Updated `app.py` to use API data structure
- See `MIGRATION_GUIDE.md` for complete migration details
