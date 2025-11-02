# Migration Guide: Google Sheets → Procyclingstats API

## Overview

The app has been successfully migrated from Google Sheets to the procyclingstats API. This means:

- ✅ **Automatic scoring**: Fantasy team scores are now calculated automatically from real race data
- ✅ **Real-time updates**: Data is fetched directly from procyclingstats.com
- ✅ **No manual data entry**: Stage results update automatically as the race progresses
- ✅ **Config-based rosters**: Team rosters are defined in a Python config file

## What Changed

### Before (Google Sheets)
- Manual time entry for each participant in Google Sheets
- CSV export fetched via HTTP requests
- Participant names and times directly in spreadsheet

### After (Procyclingstats API)
- Automatic fetching of real rider times from procyclingstats.com
- Fantasy scores calculated as sum of all riders' cumulative times
- Team rosters defined in `team_config.py`

## New Files

### 1. `team_config.py`
**Purpose**: Define which professional riders are on each fantasy team

**Structure**:
```python
TEAM_ROSTERS = {
    "Jeremy": [
        "rider/tadej-pogacar",
        "rider/jonas-vingegaard",
        # ... more riders
    ],
    "Leo": [ ... ],
    # ... other teams
}

RACE_CONFIG = {
    "race_url": "race/tour-de-france/2025",
    "race_name": "Tour de France 2025",
    "total_stages": 21
}
```

**How to update rosters**:
1. Go to procyclingstats.com
2. Search for a rider (e.g., "Tadej Pogačar")
3. Copy the URL path: `rider/tadej-pogacar`
4. Add to your team's list in `team_config.py`

### 2. `api_client.py`
**Purpose**: Handle all API interactions with procyclingstats

**Key functions**:
- `fetch_fantasy_standings()` - Get current standings with team scores
- `fetch_stage_by_stage_data()` - Get historical data for charts
- `fetch_stage_gc()` - Get General Classification for a specific stage
- `calculate_team_time()` - Sum rider times for each team

### 3. `test_integration.py`
**Purpose**: Test the API integration without running the full app

**Usage**:
```bash
python3 test_integration.py
```

## How Fantasy Scoring Works

### Scoring Formula
Each fantasy participant's score = **Sum of all their riders' cumulative times**

- Lower total time = Better score (like real cycling)
- Only riders who are still in the race (not DNF/DNS) are counted
- Times are cumulative (total time after each stage)

### Example
If Jeremy's team has:
- Tadej Pogačar: 85:20:15
- Jonas Vingegaard: 85:45:30
- Primož Roglič: 86:10:00

Jeremy's total: **257:15:45**

## Configuration Guide

### Updating Team Rosters

Edit `team_config.py`:

```python
TEAM_ROSTERS = {
    "YourName": [
        "rider/first-rider",
        "rider/second-rider",
        # Add more riders
    ]
}
```

### Changing the Race

For a different race, update `RACE_CONFIG`:

```python
RACE_CONFIG = {
    "race_url": "race/giro-d-italia/2025",  # Or "race/vuelta-a-espana/2025"
    "race_name": "Giro d'Italia 2025",
    "total_stages": 21
}
```

### Finding Race URLs

1. Go to procyclingstats.com
2. Navigate to the race
3. URL format: `procyclingstats.com/race/RACE-NAME/YEAR`
4. Use path: `race/RACE-NAME/YEAR`

## Running the App

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py --server.port 5000
```

### Testing

```bash
# Test API integration
python3 test_integration.py

# Test specific API calls
python3 test_api.py
python3 test_gc_data.py
```

## Data Caching

The app uses Streamlit's caching with a 5-minute TTL (Time To Live):
- API responses are cached for 5 minutes
- Click "🔄 Refresh" button to clear cache and fetch latest data
- Automatic refresh every 5 minutes during the race

## Important Notes

### Race Availability
- Procyclingstats data is only available for races that have started
- TDF 2025 data is accessible (all 21 stages complete as of test date)
- If a race hasn't started, the app will show an error

### Rider Availability
- Only riders who actually participated in the race will have data
- If a rider DNF (Did Not Finish) or DNS (Did Not Start), they'll be marked as such
- Team scores only count active riders

### Data Accuracy
- Data comes directly from procyclingstats.com scraping
- The `procyclingstats` package may need updates if website structure changes
- Run `pip install procyclingstats --upgrade` to get latest version

## Phase 2 Planning

Future enhancement: Web interface for team roster selection

**Planned features**:
- User authentication
- Web UI for selecting riders
- Database for storing team rosters
- Lock-in deadline before race starts
- Draft/auction system

**Not implemented yet** - Phase 1 uses config file only.

## Troubleshooting

### Error: "Unable to load standings data"
- Check if the race has started
- Verify `RACE_CONFIG["race_url"]` is correct
- Test with `python3 test_integration.py`

### Error: "No module named procyclingstats"
```bash
pip install procyclingstats
```

### Error: "No riders counted for team"
- Check if rider URLs in `team_config.py` are correct
- Verify riders actually participated in this race
- Some riders may have DNF/DNS

### Slow loading
- First load scrapes data from procyclingstats.com (can take 10-30 seconds)
- Subsequent loads use cache (5-minute TTL)
- Consider increasing cache TTL in production

## Dependencies

New dependency added:
```
procyclingstats>=0.2.7
```

This package provides:
- `Race` - Race-level data
- `Stage` - Stage-level data and GC standings
- `Rider` - Rider biographical data

## Backup/Rollback

To rollback to Google Sheets version:
```bash
git checkout <previous-commit-hash> app.py
```

The Google Sheets URLs are still in git history if needed.

## Support

For issues with:
- **Procyclingstats package**: https://github.com/themm1/procyclingstats/issues
- **Procyclingstats.com data**: Contact website owners
- **This app**: Check logs and test files

## Testing Checklist

Before deploying:
- [ ] Test `test_integration.py` passes
- [ ] Verify all team rosters are configured
- [ ] Check race URL is correct
- [ ] Confirm race has started (or will start soon)
- [ ] Test refresh button works
- [ ] Verify charts display correctly
- [ ] Check mobile responsiveness
- [ ] Test with multiple stages completed

## Example Team Roster

Here's a sample roster configuration for Tour de France:

```python
TEAM_ROSTERS = {
    "GC Contenders": [
        "rider/tadej-pogacar",
        "rider/jonas-vingegaard",
        "rider/remco-evenepoel",
        "rider/primoz-roglic",
        "rider/geraint-thomas",
        "rider/adam-yates",
        "rider/simon-yates",
        "rider/enric-mas"
    ],
    "Sprinters": [
        "rider/jasper-philipsen",
        "rider/mark-cavendish",
        "rider/biniam-girmay",
        "rider/wout-van-aert",
        "rider/mathieu-van-der-poel",
        "rider/mads-pedersen",
        "rider/dylan-groenewegen",
        "rider/arnaud-de-lie"
    ]
}
```

## Migration Complete! 🎉

Your app is now powered by real race data from procyclingstats. No more manual data entry required!
