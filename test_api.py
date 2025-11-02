"""
Test script to explore procyclingstats API capabilities
"""

from procyclingstats import Race, Stage, Rider

# Test fetching Tour de France 2025 data
print("Testing procyclingstats API...")
print("=" * 60)

# Try to fetch Tour de France 2025
try:
    print("\n1. Fetching Tour de France 2025 race data...")
    race = Race("race/tour-de-france/2025")
    race_data = race.parse()
    print(f"Race data keys: {race_data.keys() if race_data else 'No data'}")
    if race_data:
        print(f"Race name: {race_data.get('name', 'N/A')}")
        print(f"Available fields: {list(race_data.keys())}")
except Exception as e:
    print(f"Error fetching race: {e}")
    print("Note: Tour de France 2025 may not be available yet")
    print("Trying 2024 data instead...")

    try:
        race = Race("race/tour-de-france/2024")
        race_data = race.parse()
        print(f"2024 Race data keys: {race_data.keys() if race_data else 'No data'}")
        if race_data:
            print(f"Race name: {race_data.get('name', 'N/A')}")
            print(f"Available fields: {list(race_data.keys())}")
    except Exception as e2:
        print(f"Error with 2024 data: {e2}")

# Test fetching a stage
print("\n2. Testing Stage data...")
try:
    # Try stage 1 of Tour de France 2024
    stage = Stage("race/tour-de-france/2024/stage-1")
    stage_data = stage.parse()
    print(f"Stage data keys: {stage_data.keys() if stage_data else 'No data'}")
    if stage_data:
        print(f"Available fields: {list(stage_data.keys())[:10]}...")  # First 10 fields
except Exception as e:
    print(f"Error fetching stage: {e}")

# Test fetching a rider
print("\n3. Testing Rider data...")
try:
    # Test with Tadej Pogačar
    rider = Rider("rider/tadej-pogacar")
    print(f"Rider name: {rider.name()}")
    print(f"Rider birthdate: {rider.birthdate()}")

    rider_data = rider.parse()
    print(f"Rider data keys: {rider_data.keys() if rider_data else 'No data'}")
    if rider_data:
        print(f"Available fields: {list(rider_data.keys())[:10]}...")
except Exception as e:
    print(f"Error fetching rider: {e}")

print("\n" + "=" * 60)
print("API exploration complete!")
