# Giro 2026 Readiness Review
**Date**: 2026-02-21  
**Reviewer**: King Ziti  
**Target**: Giro d'Italia 2026 (May 9-31, 2026)  
**Goal**: Make app reusable across all 2026 Grand Tours (Giro, TDF, Vuelta)

---

## Executive Summary

✅ **Good News**: The multi-race infrastructure is ~85% complete. The app already supports race switching, dynamic theming, and has a clean config-based architecture.

⚠️ **Key Gaps**:
1. Giro 2026 team rosters are empty placeholders
2. No data validation or error handling for upcoming races
3. Missing admin workflow for roster management
4. No pre-race testing/preview mode

🎯 **Recommendation**: Focus on roster management workflow and pre-race validation before Giro starts in May.

---

## Current Status Assessment

### ✅ Completed Features (Phase 1-3)

| Feature | Status | Notes |
|---------|--------|-------|
| Multi-race config structure | ✅ Complete | `races_config.py` with 4 races defined |
| Race selector UI | ✅ Complete | Horizontal mobile-friendly dropdown |
| Dynamic leader colors | ✅ Complete | Yellow/Pink/Red themes working |
| URL-based race selection | ✅ Complete | `?race=giro-2026` works |
| Backwards compatibility | ✅ Complete | `team_config.py` shim layer |
| Completion status handling | ✅ Complete | Winner banners, celebration UI |
| Stage-by-stage charts | ✅ Complete | Plotly visualizations |
| API caching (5min TTL) | ✅ Complete | Streamlit `@st.cache_data` |
| Dark mode theme | ✅ Complete | #1e1e1e background |

### 🟡 Partial / Needs Work

| Feature | Status | Issue |
|---------|--------|-------|
| Giro 2026 rosters | 🟡 Empty | All participants have empty rider arrays |
| TDF 2026 rosters | 🟡 Empty | Same issue |
| Vuelta 2026 rosters | 🟡 Empty | Same issue |
| Pre-race testing | 🟡 Missing | No way to preview UI before race starts |
| Roster management | 🟡 Manual | Requires code edits in `races_config.py` |
| Error handling | 🟡 Minimal | No validation for missing rosters |
| Data source validation | 🟡 None | Assumes procyclingstats URLs exist |

### ❌ Missing Features

| Feature | Priority | Impact |
|---------|----------|--------|
| Admin roster entry UI | High | Currently requires Python editing |
| Pre-race data validation | High | Prevents launch-day failures |
| Roster import from CSV/Google Sheets | Medium | Easier participant onboarding |
| Race preview mode | Medium | Test UI before race starts |
| Automated roster reminders | Low | Notify participants of draft deadline |
| Historical race archiving | Low | Clean up old completed races |

---

## Code Quality Review

### Strengths

1. **Clean separation of concerns**:
   - `races_config.py` = data
   - `api_client.py` = data fetching
   - `app.py` = UI/presentation
   
2. **Database-ready design**:
   ```python
   # races_config.py is structured for easy PostgreSQL migration
   RACES = {...}  # → races table
   TEAM_ROSTERS = {...}  # → team_rosters table
   ```

3. **Good caching strategy**:
   - 5-minute TTL balances freshness vs API load
   - Proper use of Streamlit's built-in caching

4. **Responsive mobile design**:
   - Horizontal race selector
   - Card-based layout
   - Touch-friendly buttons

### Areas for Improvement

1. **Error handling**:
   ```python
   # Current: No validation
   team_rosters = get_team_rosters(selected_race_id)
   
   # Recommended: Add validation
   team_rosters = get_team_rosters(selected_race_id)
   if not team_rosters or all(len(r) == 0 for r in team_rosters.values()):
       st.warning("⚠️ Team rosters not configured for this race yet.")
       return
   ```

2. **Configuration validation**:
   ```python
   # Add to races_config.py
   def validate_race_config(race_id):
       """Validate race configuration completeness"""
       race = RACES.get(race_id)
       if not race:
           return False, "Race not found"
       
       # Check required fields
       required = ['id', 'name', 'race_url', 'start_date', 'end_date']
       for field in required:
           if not race.get(field):
               return False, f"Missing required field: {field}"
       
       # Check rosters
       rosters = TEAM_ROSTERS.get(race_id, {})
       if not rosters or all(len(r) == 0 for r in rosters.values()):
           return False, "No team rosters configured"
       
       return True, "OK"
   ```

3. **Data source verification**:
   ```python
   # Add pre-flight check for API URLs
   def verify_race_data_available(race_url):
       """Check if procyclingstats has data for this race"""
       try:
           # Attempt to fetch stage 1 GC
           test_fetch = fetch_stage_gc(race_url, stage=1)
           return test_fetch is not None
       except:
           return False
   ```

---

## Giro 2026 Preparation Roadmap

### Phase A: Roster Collection (March 2026)

**Tasks**:
1. Decide on roster size (3 riders like TDF 2025, or expand to 5-8?)
2. Share rider selection guidelines with participants
3. Set roster submission deadline (suggest: April 25, 2 weeks before race)
4. Create roster submission form (Google Form → Sheet, or direct edit)

**Implementation**:
```python
# Option 1: Manual update in races_config.py
TEAM_ROSTERS = {
    "giro-2026": {
        "Jeremy": [
            "rider/name-surname",  # Participant picks from ProCyclingStats
            "rider/name-surname",
            "rider/name-surname"
        ],
        # ... other participants
    }
}

# Option 2: Import from CSV
# Create giro-2026-rosters.csv:
# Participant,Rider1,Rider2,Rider3
# Jeremy,rider/name-surname,rider/name-surname,rider/name-surname
# ...
```

**Recommendation**: Use Option 2 (CSV import) for easier participant management. Create a simple script:

```python
# scripts/import_rosters.py
import csv
import json

def import_rosters_from_csv(csv_path, race_id):
    """Import team rosters from CSV into races_config.py format"""
    rosters = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            participant = row['Participant']
            riders = [
                row[f'Rider{i}'] 
                for i in range(1, 9) 
                if row.get(f'Rider{i}')
            ]
            rosters[participant] = riders
    
    print(f"# Update races_config.py TEAM_ROSTERS:")
    print(f'"{race_id}": {json.dumps(rosters, indent=4)}')

# Usage:
import_rosters_from_csv('giro-2026-rosters.csv', 'giro-2026')
```

### Phase B: Pre-Race Validation (Late April 2026)

**Tasks**:
1. Verify all rider URLs exist on ProCyclingStats
2. Test API connectivity for `race/giro-d-italia/2026`
3. Preview UI in "test mode" before May 9
4. Confirm participant email/notification setup

**Implementation**:
```python
# scripts/validate_race.py
from api_client import fetch_stage_gc
from races_config import RACES, TEAM_ROSTERS

def validate_giro_2026():
    """Pre-flight validation for Giro 2026"""
    race_id = "giro-2026"
    race = RACES[race_id]
    rosters = TEAM_ROSTERS[race_id]
    
    # Check 1: All participants have rosters
    for participant, riders in rosters.items():
        if len(riders) == 0:
            print(f"❌ {participant} has no riders")
        else:
            print(f"✅ {participant}: {len(riders)} riders")
    
    # Check 2: Verify rider URLs (sample check)
    print("\nChecking sample rider URLs...")
    # (Implement actual URL validation here)
    
    # Check 3: API connectivity
    print(f"\nTesting API for {race['race_url']}...")
    try:
        # Note: This will fail until race starts
        data = fetch_stage_gc(race['race_url'], stage=1)
        print("✅ API reachable")
    except:
        print("⚠️ API not available yet (expected before race start)")
    
    print("\n=== Validation Complete ===")

if __name__ == "__main__":
    validate_giro_2026()
```

### Phase C: Launch Day (May 9, 2026)

**Tasks**:
1. Monitor app at race start (stage 1 should populate immediately)
2. Verify all team scores calculate correctly
3. Check for DNF/DNS handling
4. Confirm mobile responsiveness
5. Share race-specific URL: `https://fantasytour.streamlit.app/?race=giro-2026`

**Monitoring checklist**:
- [ ] Stage 1 data loads within 5 minutes of GC publication
- [ ] All participants' riders appear in Team Riders tab
- [ ] Leader card shows pink jersey styling
- [ ] Charts render correctly
- [ ] No console errors
- [ ] Mobile layout works on iOS/Android

### Phase D: Post-Race Review (June 1, 2026)

**Tasks**:
1. Mark race as complete in `races_config.py`:
   ```python
   "giro-2026": {
       ...
       "is_complete": True,
       "winner": "<winner_name>",
       "completion_date": "May 31, 2026"
   }
   ```
2. Test winner celebration UI
3. Archive lessons learned for TDF 2026
4. Update documentation

---

## Recommended Improvements for Reusability

### 1. Roster Management Script (High Priority)

**Create**: `scripts/roster_manager.py`

```python
"""
Interactive roster management for Fantasy Grand Tours
Usage: python scripts/roster_manager.py giro-2026
"""

import sys
from races_config import RACES, TEAM_ROSTERS

def manage_rosters(race_id):
    """Interactive CLI for roster management"""
    if race_id not in RACES:
        print(f"❌ Race '{race_id}' not found")
        return
    
    race = RACES[race_id]
    rosters = TEAM_ROSTERS.get(race_id, {})
    
    print(f"\n=== {race['name']} Roster Manager ===\n")
    print(f"Participants: {', '.join(rosters.keys())}")
    
    while True:
        print("\nCommands:")
        print("  1) View all rosters")
        print("  2) Edit participant roster")
        print("  3) Import from CSV")
        print("  4) Export to CSV")
        print("  5) Validate rosters")
        print("  q) Quit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            show_rosters(rosters)
        elif choice == "2":
            edit_roster(rosters)
        elif choice == "3":
            import_csv(race_id)
        elif choice == "4":
            export_csv(race_id, rosters)
        elif choice == "5":
            validate_rosters(rosters)
        elif choice.lower() == "q":
            break

def show_rosters(rosters):
    """Display all rosters"""
    for participant, riders in rosters.items():
        print(f"\n{participant}:")
        for i, rider in enumerate(riders, 1):
            print(f"  {i}. {rider}")

def edit_roster(rosters):
    """Edit a participant's roster"""
    participant = input("Participant name: ").strip()
    if participant not in rosters:
        print(f"❌ Participant '{participant}' not found")
        return
    
    print(f"\nCurrent roster for {participant}:")
    for i, rider in enumerate(rosters[participant], 1):
        print(f"  {i}. {rider}")
    
    print("\nEnter new riders (one per line, format: rider/firstname-lastname)")
    print("Press Enter twice when done:")
    
    new_riders = []
    while True:
        rider = input("Rider URL: ").strip()
        if not rider:
            break
        new_riders.append(rider)
    
    rosters[participant] = new_riders
    print(f"✅ Updated {participant}'s roster")

# ... implement other functions

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python roster_manager.py <race-id>")
        sys.exit(1)
    
    manage_rosters(sys.argv[1])
```

### 2. Pre-Race Testing Mode (Medium Priority)

**Add to `app.py`**:

```python
# Enable test mode via ?test=true query parameter
query_params = st.query_params
test_mode = query_params.get("test", "false").lower() == "true"

if test_mode:
    st.warning("⚠️ TEST MODE ACTIVE - Using mock data")
    
    # Override API calls with mock data
    @st.cache_data
    def fetch_fantasy_standings_test(race_url, team_rosters):
        """Mock standings for testing UI"""
        import random
        mock_data = []
        for participant, riders in team_rosters.items():
            mock_data.append({
                'Participant': participant,
                'Total Time (s)': random.randint(80*3600, 90*3600),  # 80-90 hours
                'Riders': riders
            })
        return pd.DataFrame(mock_data).sort_values('Total Time (s)')
    
    fetch_fantasy_standings = fetch_fantasy_standings_test
```

**Usage**: `https://fantasytour.streamlit.app/?race=giro-2026&test=true`

### 3. Configuration Validation (High Priority)

**Add to `races_config.py`**:

```python
def validate_all_races():
    """Validate all race configurations"""
    errors = []
    warnings = []
    
    for race_id, race in RACES.items():
        # Required fields
        required = ['id', 'name', 'race_url', 'start_date', 'end_date', 'total_stages']
        for field in required:
            if not race.get(field):
                errors.append(f"{race_id}: Missing required field '{field}'")
        
        # Roster check
        rosters = TEAM_ROSTERS.get(race_id, {})
        if not rosters:
            warnings.append(f"{race_id}: No rosters defined")
        else:
            empty_rosters = [p for p, r in rosters.items() if len(r) == 0]
            if empty_rosters:
                warnings.append(f"{race_id}: Empty rosters for {', '.join(empty_rosters)}")
        
        # Date validation
        try:
            from datetime import datetime
            start = datetime.strptime(race['start_date'], '%Y-%m-%d')
            end = datetime.strptime(race['end_date'], '%Y-%m-%d')
            if end < start:
                errors.append(f"{race_id}: End date before start date")
        except ValueError as e:
            errors.append(f"{race_id}: Invalid date format - {e}")
    
    return errors, warnings

# Run validation at module load
if __name__ == "__main__":
    errors, warnings = validate_all_races()
    
    if errors:
        print("❌ ERRORS:")
        for e in errors:
            print(f"  - {e}")
    
    if warnings:
        print("\n⚠️ WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
    
    if not errors and not warnings:
        print("✅ All race configurations valid")
```

**Usage**: `python races_config.py` (run before deployments)

### 4. Participant Notification System (Low Priority)

**Create**: `scripts/notify_participants.py`

```python
"""
Send race start/completion notifications to participants
Requires email addresses in participant_contacts.json
"""

import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from races_config import RACES

# Load contacts
# participant_contacts.json:
# {
#   "Jeremy": "jeremy@example.com",
#   "Leo": "leo@example.com",
#   ...
# }

def send_race_start_reminder(race_id):
    """Send email 1 week before race starts"""
    race = RACES[race_id]
    start = datetime.strptime(race['start_date'], '%Y-%m-%d')
    
    subject = f"{race['name']} starts in 1 week!"
    body = f"""
    The {race['name']} begins on {race['start_date']}.
    
    Track live standings at:
    https://fantasytour.streamlit.app/?race={race_id}
    
    Good luck!
    """
    
    # Send emails...
    # (Implementation depends on email provider)

# Could be scheduled via cron or GitHub Actions
```

---

## Technical Debt & Future Enhancements

### Short-Term (Before Giro 2026)

1. ✅ **Add roster validation** - Prevent empty rosters from breaking UI
2. ✅ **Create roster import script** - CSV → races_config.py
3. ✅ **Add test mode** - Preview UI with mock data
4. ⚠️ **Improve error messages** - Better feedback when API fails

### Medium-Term (After Giro, Before TDF 2026)

1. **Admin panel** - Web UI for roster management (Streamlit multipage app)
2. **Historical comparison** - Compare participant performance across races
3. **Stage predictions** - Let participants predict stage winners
4. **Mobile app** - Progressive Web App (PWA) with offline support
5. **Push notifications** - Alert on leader changes

### Long-Term (2027+)

1. **Database migration** - Move from Python dicts to PostgreSQL
2. **Multi-league support** - Multiple friend groups, private leagues
3. **Rider stats integration** - Show rider form, team info
4. **Live stage updates** - Real-time tracking during race
5. **Prize/achievement system** - Gamification badges

---

## Deployment Checklist for Giro 2026

### 2 Weeks Before (April 25)

- [ ] All rosters submitted by participants
- [ ] Rosters imported into `races_config.py`
- [ ] Run `python races_config.py` validation
- [ ] Test race selector shows "🟣 Giro 2026 🔄" status
- [ ] Verify pink leader jersey color (`#FF69B4`)
- [ ] Push updated code to GitHub
- [ ] Streamlit Cloud auto-deploys

### 1 Week Before (May 2)

- [ ] Share race URL with participants: `?race=giro-2026`
- [ ] Test mobile layout on iOS/Android
- [ ] Verify API connectivity (if race data available early)
- [ ] Prepare monitoring dashboard (Streamlit Cloud metrics)

### Launch Day (May 9)

- [ ] Monitor first stage data load (usually ~2 hours after stage finish)
- [ ] Verify all charts render
- [ ] Check for errors in Streamlit Cloud logs
- [ ] Post standings snapshot to group chat

### During Race (May 9-31)

- [ ] Daily check for API errors
- [ ] Monitor cache performance (5-min TTL sufficient?)
- [ ] Engage participants with standings updates
- [ ] Track any bugs/issues for post-race review

### Post-Race (June 1)

- [ ] Mark race complete in config
- [ ] Update winner name
- [ ] Test celebration UI
- [ ] Archive lessons learned
- [ ] Prepare for TDF 2026 (July 4-26)

---

## Summary & Next Steps

### What's Working

✅ Solid technical foundation  
✅ Clean architecture ready for scale  
✅ Mobile-friendly responsive design  
✅ Multi-race switching implemented  
✅ Dynamic theming works great  

### What Needs Work

⚠️ Empty rosters for all 2026 races  
⚠️ No pre-race validation workflow  
⚠️ Manual roster management (requires code edits)  
⚠️ Limited error handling for missing data  

### Recommended Priority Actions

**Before March 1**:
1. Create `scripts/roster_manager.py` for easier participant management
2. Add roster validation to `races_config.py`
3. Document roster submission process

**Before April 1**:
1. Collect Giro 2026 rosters from participants
2. Import rosters into config
3. Run validation suite

**Before May 1**:
1. Deploy updated config to Streamlit Cloud
2. Test preview mode with mock data
3. Share race URL with participants

**Launch Day (May 9)**:
1. Monitor first stage load
2. Verify standings calculate correctly
3. Engage participants

### Long-Term Vision

This app is well-positioned to become the standard fantasy platform for your cycling group. With minor improvements to roster management and error handling, it's ready for prime time.

**2026 Grand Tour Schedule**:
- ✅ Giro d'Italia: May 9-31
- ✅ Tour de France: July 4-26
- ✅ Vuelta a España: August 22 - September 13

By race 3 (Vuelta), you'll have a smooth repeatable workflow.

---

**Questions or concerns? Let me know and I can dive deeper into any section.**
