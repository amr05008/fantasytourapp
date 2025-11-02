"""
Test script to explore GC (General Classification) data structure
"""

from procyclingstats import Stage
import json

print("Testing GC data structure...")
print("=" * 60)

try:
    # Fetch a stage from Tour de France 2024 (known complete data)
    print("\nFetching Stage 5 of Tour de France 2024...")
    stage = Stage("race/tour-de-france/2024/stage-5")
    stage_data = stage.parse()

    if stage_data and 'gc' in stage_data:
        gc_data = stage_data['gc']
        print(f"\nGC data type: {type(gc_data)}")

        if isinstance(gc_data, list) and len(gc_data) > 0:
            print(f"\nNumber of riders in GC: {len(gc_data)}")
            print(f"\nFirst GC entry structure:")
            print(json.dumps(gc_data[0], indent=2, default=str))

            print(f"\nSecond GC entry structure:")
            print(json.dumps(gc_data[1], indent=2, default=str))

            print(f"\nThird GC entry structure:")
            print(json.dumps(gc_data[2], indent=2, default=str))

        elif isinstance(gc_data, dict):
            print(f"\nGC data is a dict with keys: {gc_data.keys()}")
            print(json.dumps(gc_data, indent=2, default=str))
        else:
            print(f"\nGC data: {gc_data}")

    # Also check results data
    if stage_data and 'results' in stage_data:
        results_data = stage_data['results']
        print(f"\n\nResults data type: {type(results_data)}")

        if isinstance(results_data, list) and len(results_data) > 0:
            print(f"\nNumber of results: {len(results_data)}")
            print(f"\nFirst result entry structure:")
            print(json.dumps(results_data[0], indent=2, default=str))
        else:
            print(f"\nResults data: {results_data}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
