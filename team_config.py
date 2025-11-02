"""
Team Roster Configuration - LEGACY FILE (Backwards Compatibility)

NOTE: This file is maintained for backwards compatibility only.
All race configurations have been moved to races_config.py

For multi-race support, import from races_config.py instead:
    from races_config import RACES, TEAM_ROSTERS, get_race_config, get_team_rosters
"""

# Import from new races_config.py for backwards compatibility
from races_config import TEAM_ROSTERS as _ALL_ROSTERS, RACES, DEFAULT_RACE

# Export TDF 2025 config as default for backwards compatibility
TEAM_ROSTERS = _ALL_ROSTERS[DEFAULT_RACE]
RACE_CONFIG = {
    "race_url": RACES[DEFAULT_RACE]["race_url"],
    "race_name": RACES[DEFAULT_RACE]["name"],
    "total_stages": RACES[DEFAULT_RACE]["total_stages"]
}

# Note: For new code, use races_config.py directly
# Example:
#   from races_config import get_race_config, get_team_rosters
#   race = get_race_config("tdf-2026")
#   rosters = get_team_rosters("tdf-2026")
