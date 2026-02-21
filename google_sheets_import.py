"""
Google Sheets roster import for Fantasy Grand Tours

This module loads team rosters from a published Google Sheet,
allowing easy roster management without code changes.

Setup:
1. Create Google Sheet with columns: Race ID, Participant, Rider1, Rider2, Rider3, ...
2. File → Share → Publish to web → Publish as CSV
3. Copy the sheet URL to ROSTER_SHEET_URL in races_config.py
"""

import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_rosters_from_sheet(sheet_url):
    """
    Load rosters from Google Sheet
    
    Args:
        sheet_url: Google Sheets URL (must be published to web)
        
    Returns:
        dict: Rosters organized by race_id
              Format: {race_id: {participant: [rider_urls]}}
    
    Example Sheet Format:
        Race ID    | Participant | Rider1             | Rider2             | Rider3             
        -----------|-------------|--------------------|--------------------|--------------------
        giro-2026  | Jeremy      | rider/name-surname | rider/name-surname | rider/name-surname
        giro-2026  | Leo         | rider/name-surname | rider/name-surname | rider/name-surname
    """
    try:
        # Convert Google Sheets URL to CSV export URL
        if '/edit' in sheet_url:
            sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        else:
            sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
        
        # Load CSV data
        df = pd.read_csv(csv_url)
        
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Validate required columns
        if 'Race ID' not in df.columns or 'Participant' not in df.columns:
            raise ValueError("Sheet must have 'Race ID' and 'Participant' columns")
        
        # Convert to races_config format
        rosters_by_race = {}
        
        for race_id in df['Race ID'].unique():
            # Skip empty race IDs
            if pd.isna(race_id):
                continue
            
            race_df = df[df['Race ID'] == race_id]
            rosters = {}
            
            for _, row in race_df.iterrows():
                participant = row['Participant']
                
                # Skip empty participants
                if pd.isna(participant):
                    continue
                
                # Collect all rider columns (Rider1, Rider2, Rider3, etc.)
                riders = []
                for col in df.columns:
                    if col.startswith('Rider') and pd.notna(row[col]) and row[col].strip():
                        riders.append(row[col].strip())
                
                rosters[participant] = riders
            
            if rosters:  # Only add if we have rosters
                rosters_by_race[race_id] = rosters
        
        return rosters_by_race
    
    except Exception as e:
        # Log error but don't crash the app
        st.warning(f"⚠️ Could not load rosters from Google Sheet: {e}")
        return {}


def get_sheet_status(sheet_url):
    """
    Check if Google Sheet is accessible
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        rosters = load_rosters_from_sheet(sheet_url)
        
        if not rosters:
            return False, "Sheet is accessible but contains no rosters"
        
        race_count = len(rosters)
        participant_counts = {race_id: len(r) for race_id, r in rosters.items()}
        
        return True, f"✅ Loaded {race_count} races: {participant_counts}"
    
    except Exception as e:
        return False, f"❌ Error: {e}"


# Test function for validation
if __name__ == "__main__":
    # Test with example sheet
    test_url = "https://docs.google.com/spreadsheets/d/1iRpOvAYQaJh2oCcIjZcLDLbJT0eGXqT0nZEXjttOOqI/edit"
    
    print("Testing Google Sheets import...")
    print(f"Sheet URL: {test_url}")
    print()
    
    success, message = get_sheet_status(test_url)
    print(message)
    
    if success:
        rosters = load_rosters_from_sheet(test_url)
        print("\nRosters loaded:")
        for race_id, race_rosters in rosters.items():
            print(f"\n{race_id}:")
            for participant, riders in race_rosters.items():
                print(f"  {participant}: {len(riders)} riders")
                for rider in riders:
                    print(f"    - {rider}")
