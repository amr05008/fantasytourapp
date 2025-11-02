"""
Test the API integration without running the full Streamlit app
"""

import sys
print("Testing API integration...")
print("=" * 60)

# Test imports
print("\n1. Testing imports...")
try:
    from api_client import fetch_fantasy_standings, fetch_stage_by_stage_data
    from team_config import TEAM_ROSTERS, RACE_CONFIG
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test team rosters
print("\n2. Checking team rosters...")
print(f"   Teams configured: {list(TEAM_ROSTERS.keys())}")
print(f"   Race: {RACE_CONFIG['race_name']}")
print(f"   Race URL: {RACE_CONFIG['race_url']}")

for team, riders in TEAM_ROSTERS.items():
    print(f"   {team}: {len(riders)} riders")

# Test API fetching
print("\n3. Testing fantasy standings fetch...")
try:
    fantasy_data = fetch_fantasy_standings()

    if fantasy_data is None:
        print("✗ No data returned (race may not have started yet)")
        print("   This is expected if Tour de France 2025 hasn't started")
    else:
        print("✓ Data fetched successfully!")
        print(f"   Latest stage: {fantasy_data['latest_stage']}")
        print(f"   Teams: {len(fantasy_data['standings'])}")

        print("\n   Current Standings:")
        for participant, data in fantasy_data['standings']:
            position = data['position']
            total_time = data['total_time']
            gap = data['gap']
            riders_counted = data['riders_counted']
            print(f"      {position}. {participant}: {total_time} ({gap}) - {riders_counted}/{data['total_riders']} riders")

        # Test stage-by-stage data
        print("\n4. Testing stage-by-stage data fetch...")
        stage_data = fetch_stage_by_stage_data(fantasy_data['latest_stage'])
        print(f"✓ Stage data fetched for {len(stage_data)} teams")

except Exception as e:
    print(f"✗ Error during fetch: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Integration test complete!")
