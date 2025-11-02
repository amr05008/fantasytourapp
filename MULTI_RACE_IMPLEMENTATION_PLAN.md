# Multi-Race Implementation Plan

## Overview
Converting the Fantasy TDF app to support multiple Grand Tours (Giro, Tour de France, Vuelta) with a race selector UI.

## Status: IN PROGRESS (Phase 1 Complete)

---

## ✅ Completed Tasks

### 1. Create races_config.py
**Status**: ✅ Complete

**What was done**:
- Created new `races_config.py` with multi-race structure
- Defined 4 races: tdf-2025 (complete), giro-2026, tdf-2026, vuelta-2026
- Each race includes:
  - Race metadata (name, dates, URL)
  - Leader jersey color (#FFD700 yellow, #FF69B4 pink, #DC143C red)
  - Completion status and winner info
  - Team rosters per race
- Added helper functions:
  - `get_race_config(race_id)`
  - `get_team_rosters(race_id)`
  - `get_all_races()`
  - `get_active_races()`
  - `get_upcoming_races()`
  - `get_completed_races()`

**Database-ready design**: Structure can easily migrate to PostgreSQL/SQLite for Phase 4.

### 2. Update team_config.py for Backwards Compatibility
**Status**: ✅ Complete

**What was done**:
- Converted `team_config.py` to a compatibility shim
- Imports from `races_config.py` but maintains same API
- Exports `TEAM_ROSTERS` and `RACE_CONFIG` for existing code
- Added deprecation comments guiding users to new structure

**Verified**: Backwards compatibility tested and working.

---

## 🔄 Remaining Tasks

### 3. Add Race Selector to App (app.py)
**Status**: 🟡 Pending

**Changes needed**:

#### A. Update imports (line 14)
```python
# FROM:
from team_config import TEAM_ROSTERS, RACE_CONFIG

# TO:
from races_config import (
    RACES,
    DEFAULT_RACE,
    get_race_config,
    get_team_rosters,
    get_all_races
)
```

#### B. Add session state for selected race (after st.set_page_config)
```python
# Initialize race selection in session state
if 'selected_race_id' not in st.session_state:
    st.session_state.selected_race_id = DEFAULT_RACE
```

#### C. Add sidebar race selector (in main() function, before tabs)
```python
def main():
    # Race selector in sidebar
    st.sidebar.title("🏁 Race Selection")

    all_races = get_all_races()
    race_options = {
        race['id']: f"{race['leader_jersey_emoji']} {race['short_name']}"
        + (" ✅" if race['is_complete'] else " 🔄" if is_race_active(race) else "")
        for race in all_races
    }

    selected_race_id = st.sidebar.selectbox(
        "Select Race",
        options=list(race_options.keys()),
        format_func=lambda x: race_options[x],
        index=list(race_options.keys()).index(st.session_state.selected_race_id),
        key='race_selector'
    )

    # Update session state
    if selected_race_id != st.session_state.selected_race_id:
        st.session_state.selected_race_id = selected_race_id
        st.rerun()

    # Get config for selected race
    race_config = get_race_config(selected_race_id)
    team_rosters = get_team_rosters(selected_race_id)

    # ... rest of main()
```

#### D. Helper function for active race detection
```python
def is_race_active(race):
    """Check if a race is currently in progress"""
    from datetime import datetime
    now = datetime.now().date()
    start = datetime.strptime(race['start_date'], '%Y-%m-%d').date()
    end = datetime.strptime(race['end_date'], '%Y-%m-%d').date()
    return start <= now <= end
```

---

### 4. Make COMPETITION_CONFIG Dynamic
**Status**: 🟡 Pending

**Changes needed**:

#### A. Remove static COMPETITION_CONFIG (lines 95-101)
Delete the hardcoded dictionary.

#### B. Create function to generate config from race
```python
def get_competition_config(race_config):
    """Generate competition config from race config"""
    return {
        "is_complete": race_config['is_complete'],
        "winner_name": race_config['winner'],
        "competition_name": race_config['name'],
        "total_stages": race_config['total_stages'],
        "completion_date": race_config['completion_date'],
        "show_celebration": race_config['is_complete']
    }
```

#### C. Update all references to COMPETITION_CONFIG
Locations to update:
- Line ~207: `get_competition_title()` function
- Line ~214: `create_completion_status_card()` function
- Line ~131: `create_winner_banner()` function
- Pass `race_config` as parameter to these functions

---

### 5. Update Title Generation
**Status**: 🟡 Pending

**Changes needed**:

#### A. Update page title (line 18)
Make it dynamic:
```python
# In main(), after getting race_config:
st.set_page_config(
    page_title=f"Sunshine Fantasy {race_config['short_name']}",
    page_icon=race_config['leader_jersey_emoji'],
    layout="wide"
)
```

**Note**: st.set_page_config can only be called once, so we need to reorganize to call it with dynamic values.

#### B. Update get_competition_title() (line ~207)
```python
def get_competition_title(race_config):
    """Get the appropriate title based on race and completion status"""
    base_title = f"🚴 Sunshine's Fantasy {race_config['short_name']}"

    if race_config["is_complete"]:
        return f"{base_title} - COMPLETE ✅"
    else:
        return base_title
```

---

### 6. Make Leader Card Color Dynamic
**Status**: 🟡 Pending

**Changes needed**:

#### A. Update create_standings_card() function
Find where leader card is created (search for "#FFD700" or "dark-leader-card").

**Current approach**: Hardcoded yellow color
**New approach**: Pass `leader_color` from race_config

```python
def create_standings_card(name, position, time, gap, is_leader, race_config):
    """Create a styled card for each participant with dynamic leader color"""
    leader_color = race_config['leader_color'] if is_leader else None

    # Update CSS styling to use leader_color variable
    card_style = f"""
        background: linear-gradient(135deg, {leader_color} 0%, {adjust_color(leader_color, -20)} 100%) !important;
        ...
    """ if is_leader else "..."
```

**Alternative simpler approach**:
```python
# In main(), before calling create_standings_card:
leader_color = race_config['leader_color']

# Then pass leader_color to the function or use it directly in CSS
```

#### B. Update CSS classes in get_dark_theme_css()
Lines ~768-788 have hardcoded #FFD700 colors:

```python
# Current:
.dark-leader-card {
    background-color: #FFD700 !important;
    ...
}

# Option 1: CSS variables (cleaner)
def get_dark_theme_css(leader_color="#FFD700"):
    return f"""
    <style>
    :root {{
        --leader-color: {leader_color};
    }}
    .dark-leader-card {{
        background-color: var(--leader-color) !important;
        ...
    }}
    ...
    </style>
    """

# Option 2: Direct substitution
def get_dark_theme_css(leader_color="#FFD700"):
    return f"""
    <style>
    .dark-leader-card {{
        background-color: {leader_color} !important;
        color: #000000 !important;
        ...
    }}
    ...
    </style>
    """
```

**Recommended**: Use CSS variables (Option 1) for better maintainability.

---

### 7. Update fetch_fantasy_standings() Calls
**Status**: 🟡 Pending

**Changes needed**:

Update all calls to `fetch_fantasy_standings()` to pass race-specific parameters:

```python
# Current:
fantasy_data = fetch_fantasy_standings()

# New:
fantasy_data = fetch_fantasy_standings(
    race_url=race_config['race_url']
)
```

**Locations to update**:
- In main() function where data is fetched
- Pass team_rosters from `get_team_rosters(selected_race_id)`

---

### 8. Test Race Switching
**Status**: 🟡 Pending

**Test checklist**:
- [ ] Race selector dropdown appears in sidebar
- [ ] Selecting different races updates the UI
- [ ] TDF 2025 shows yellow jersey styling
- [ ] Giro 2026 would show pink (once rosters added)
- [ ] Completed races show "✅" badge
- [ ] Session state persists race selection
- [ ] Charts update with correct race data
- [ ] Team rosters display correctly per race
- [ ] No errors when switching between races

---

### 9. Update Documentation
**Status**: 🟡 Pending

**Files to update**:

#### A. README.md
- Add multi-race support section
- Explain how to add new races
- Update screenshots if needed

#### B. CLAUDE.md
- Update "Project Overview" section
- Document new `races_config.py` structure
- Update data architecture section
- Add race selection feature docs
- Note database-ready design for Phase 4

#### C. MIGRATION_GUIDE.md (if still relevant)
- Add section on multi-race migration
- Explain races_config.py structure

---

## Implementation Order (Recommended)

1. ✅ Create races_config.py
2. ✅ Update team_config.py for backwards compatibility
3. 🔄 Add race selector UI to sidebar
4. 🔄 Make COMPETITION_CONFIG dynamic
5. 🔄 Update title generation
6. 🔄 Make leader card colors dynamic
7. 🔄 Update API call parameters
8. 🔄 Test thoroughly
9. 🔄 Update documentation
10. 🔄 Commit and push

---

## Code Locations Reference

### Key Files:
- `races_config.py` - Multi-race definitions (NEW)
- `team_config.py` - Backwards compatibility shim (MODIFIED)
- `app.py` - Main application (NEEDS UPDATES)
- `api_client.py` - No changes needed
- `CLAUDE.md` - Needs documentation update
- `README.md` - Needs documentation update

### Key Line Numbers in app.py:
- Line 14: Import statements
- Line 18: st.set_page_config (needs to be made dynamic)
- Lines 95-101: COMPETITION_CONFIG (replace with function)
- Line 207: get_competition_title() (add race_config parameter)
- Line 214: create_completion_status_card() (add race_config parameter)
- Lines 768-788: Leader card CSS (make color dynamic)
- Main function: Add race selector sidebar

---

## Phase 4 Database Migration Notes

When ready to implement Option 4 (Database + Admin Panel), this structure maps cleanly to:

```sql
CREATE TABLE races (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    short_name VARCHAR,
    race_url VARCHAR,
    leader_color VARCHAR,
    leader_jersey_emoji VARCHAR,
    start_date DATE,
    end_date DATE,
    is_complete BOOLEAN DEFAULT FALSE,
    winner_id INTEGER REFERENCES participants(id),
    completion_date DATE
);

CREATE TABLE participants (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE team_rosters (
    id SERIAL PRIMARY KEY,
    race_id VARCHAR REFERENCES races(id),
    participant_id INTEGER REFERENCES participants(id),
    rider_url VARCHAR NOT NULL,
    UNIQUE(race_id, participant_id, rider_url)
);
```

---

## Testing Strategy

### Unit Tests (Future)
- Test `get_race_config()` with valid/invalid IDs
- Test `get_team_rosters()` with empty rosters
- Test `get_active_races()` with various dates

### Integration Tests
- Test race switching updates all UI elements
- Test backwards compatibility of team_config.py
- Test dynamic color theming for different races

### Manual Testing Checklist
- [x] TDF 2025 loads with yellow theme
- [ ] Can switch to Giro 2026 (pink theme)
- [ ] Can switch to TDF 2026 (yellow theme)
- [ ] Can switch to Vuelta 2026 (red theme)
- [ ] Completed race shows winner banner
- [ ] Incomplete race doesn't show winner
- [ ] Charts render correctly for each race
- [ ] Team rosters display correctly
- [ ] Mobile responsive still works
- [ ] No console errors

---

## Rollback Plan

If issues arise, rollback to pre-multi-race state:

```bash
# Revert to commit before multi-race changes
git revert <commit-hash>

# Or restore individual files
git checkout HEAD~1 -- team_config.py app.py

# Remove races_config.py if needed
rm races_config.py
```

---

## Next Session Tasks

**Priority Order**:
1. Add race selector to sidebar (30 min)
2. Make COMPETITION_CONFIG dynamic (20 min)
3. Update leader card colors (30 min)
4. Test race switching (20 min)
5. Update documentation (20 min)

**Estimated Time**: 2 hours

**Token Estimate**: 30-40k tokens

---

## Notes
- Designed with database migration (Phase 4) in mind
- Backwards compatible with existing code
- No breaking changes to API client
- Race configs can be updated without touching code
- Easy to add new races (just update races_config.py)
