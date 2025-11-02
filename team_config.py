"""
Team Roster Configuration for Fantasy Tour de France 2025

This file defines which professional riders are on each fantasy participant's team.
Update this file to change team rosters.

Format:
- Keys are fantasy participant names (Jeremy, Leo, Charles, Aaron, Nate)
- Values are lists of rider URLs from procyclingstats.com
- Rider URLs should be in format: "rider/firstname-lastname"

Example: "rider/tadej-pogacar" for Tadej Pogačar

To find a rider's URL:
1. Go to procyclingstats.com
2. Search for the rider
3. Copy the last part of the URL (e.g., "rider/jonas-vingegaard")
"""

TEAM_ROSTERS = {
    "Jeremy": [
        "rider/sepp-kuss",
        "rider/jhonatan-narvaez",
        "rider/ben-healy"
    ],
    "Leo": [
        "rider/felix-gall",
        "rider/kevin-vauquelin",
        "rider/guillaume-martin"
    ],
    "Charles": [
        "rider/jordan-jegat",
        "rider/tobias-halland-johannessen",
        "rider/aleksandr-vlasov"
    ],
    "Aaron": [
        "rider/florian-lipowitz",
        "rider/oscar-onley",
        "rider/ben-o-connor"
    ],
    "Nate": [
        "rider/primoz-roglic",
        "rider/valentin-paret-peintre",
        "rider/geraint-thomas"
    ]
}

# Race configuration
RACE_CONFIG = {
    # The URL path for the race on procyclingstats.com
    # Format: "race/race-name/YEAR"
    # Example: "race/tour-de-france/2025"
    "race_url": "race/tour-de-france/2025",

    # Race name for display
    "race_name": "Tour de France 2025",

    # Total number of stages
    "total_stages": 21,
}
