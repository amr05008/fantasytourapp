# Google Sheets Roster Setup Guide

This guide explains how to set up and use Google Sheets for roster management.

---

## Quick Start

### Step 1: Set Up the Sheet

Your sheet should have these columns (in this order):

| Race ID | Participant | Rider1 | Rider2 | Rider3 | Rider4 | Rider5 | ... |
|---------|-------------|--------|--------|--------|--------|--------|-----|

**Column descriptions:**
- **Race ID**: The race identifier (e.g., `giro-2026`, `tdf-2026`, `vuelta-2026`)
- **Participant**: Name of the fantasy participant (e.g., `Jeremy`, `Leo`, `Charles`, `Aaron`, `Nate`)
- **Rider1, Rider2, Rider3, ...**: ProCyclingStats rider URLs (format: `rider/firstname-lastname`)

### Step 2: Fill in Rosters

**Example sheet data:**

```
Race ID    | Participant | Rider1                   | Rider2                   | Rider3
-----------|-------------|--------------------------|--------------------------|---------------------------
giro-2026  | Jeremy      | rider/primoz-roglic      | rider/jai-hindley        | rider/joao-almeida
giro-2026  | Leo         | rider/geraint-thomas     | rider/thymen-arensman    | rider/andreas-leknessund
giro-2026  | Charles     | rider/ben-oconnor        | rider/eddie-dunbar       | rider/einer-rubio
giro-2026  | Aaron       | rider/antonio-tiberi     | rider/mattias-skjelmose  | rider/brandon-mcnulty
giro-2026  | Nate        | rider/giulio-ciccone     | rider/lorenzo-fortunato  | rider/damiano-caruso
tdf-2026   | Jeremy      | rider/jonas-vingegaard   | rider/remco-evenepoel    | rider/juan-ayuso
tdf-2026   | Leo         | rider/tadej-pogacar      | rider/egan-bernal         | rider/sepp-kuss
...
```

**Finding rider URLs:**
1. Go to https://www.procyclingstats.com/
2. Search for a rider (e.g., "Primož Roglič")
3. Copy the URL slug from their profile page
   - Full URL: `https://www.procyclingstats.com/rider/primoz-roglic`
   - Use only: `rider/primoz-roglic`

### Step 3: Publish to Web

**Critical step — the app can't access private sheets!**

1. In Google Sheets, click **File → Share → Publish to web**
2. Under "Link", select:
   - **Entire Document** (or just the first sheet)
   - **Comma-separated values (.csv)**
3. Click **Publish**
4. Confirm the warning about making data publicly accessible
5. Copy the published link (not needed, we already have your sheet URL)

**Important**: After publishing, test that the sheet is accessible by visiting:
```
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv
```
You should see CSV data, not an error page.

### Step 4: Verify Import

Once the sheet is published, test the import:

```bash
cd fantasytourapp
python google_sheets_import.py
```

You should see output like:
```
Testing Google Sheets import...
Sheet URL: https://docs.google.com/spreadsheets/d/1iRpOvAYQaJh2oCcIjZcLDLbJT0eGXqT0nZEXjttOOqI/edit

✅ Loaded 3 races: {'giro-2026': 5, 'tdf-2026': 5, 'vuelta-2026': 5}

Rosters loaded:

giro-2026:
  Jeremy: 3 riders
    - rider/primoz-roglic
    - rider/jai-hindley
    - rider/joao-almeida
  Leo: 3 riders
    ...
```

### Step 5: Deploy

Once verified, just commit and push:

```bash
git add races_config.py google_sheets_import.py GOOGLE_SHEETS_SETUP.md
git commit -m "feat: Google Sheets roster import"
git push
```

Streamlit Cloud will auto-deploy in ~2 minutes.

---

## Workflow for Each Race

### Pre-Race (2 weeks before start)

1. **Draft rosters** offline (group chat, call, etc.)
2. **Update the Google Sheet**:
   - Add new rows with `Race ID` = `giro-2026` (or whatever race)
   - Fill in participant names and rider URLs
3. **Save** — changes are immediate (no need to re-publish)
4. **Wait up to 1 hour** for app cache to refresh (or force-refresh)

### During Race

- Rosters are locked in (sheet updates won't affect live race)
- App fetches live standings from ProCyclingStats API
- Scores update automatically every 5 minutes

### Post-Race

- Mark race as complete in `races_config.py`:
  ```python
  "giro-2026": {
      ...
      "is_complete": True,
      "winner": "Jeremy",  # Example
      "completion_date": "May 31, 2026"
  }
  ```
- Commit and push to show winner celebration UI

---

## Sheet Template

Your current sheet is already set up at:
https://docs.google.com/spreadsheets/d/1iRpOvAYQaJh2oCcIjZcLDLbJT0eGXqT0nZEXjttOOqI/edit

**Sample structure to copy:**

| Race ID | Participant | Rider1 | Rider2 | Rider3 | Rider4 | Rider5 |
|---------|-------------|--------|--------|--------|--------|--------|
| giro-2026 | Jeremy | rider/primoz-roglic | rider/jai-hindley | rider/joao-almeida | | |
| giro-2026 | Leo | rider/geraint-thomas | rider/thymen-arensman | rider/andreas-leknessund | | |
| giro-2026 | Charles | rider/ben-oconnor | rider/eddie-dunbar | rider/einer-rubio | | |
| giro-2026 | Aaron | rider/antonio-tiberi | rider/mattias-skjelmose | rider/brandon-mcnulty | | |
| giro-2026 | Nate | rider/giulio-ciccone | rider/lorenzo-fortunato | rider/damiano-caruso | | |

**Tips:**
- Leave unused rider columns empty (don't delete them)
- Can add notes columns if you want (they'll be ignored)
- Duplicate rows for different races (change `Race ID` column)
- App reads all sheets, so you can organize by tabs if you want (but stick to first tab for simplicity)

---

## Troubleshooting

### "Could not load rosters from Google Sheet"

**Cause**: Sheet is not published to web

**Fix**:
1. File → Share → Publish to web
2. Select CSV format
3. Click Publish

### "Sheet is accessible but contains no rosters"

**Cause**: Column names don't match expected format

**Fix**:
- First column must be named exactly `Race ID`
- Second column must be named exactly `Participant`
- Rider columns must be named `Rider1`, `Rider2`, `Rider3`, etc.

### App shows old rosters after sheet update

**Cause**: 1-hour cache in the app

**Fix**:
- Wait up to 1 hour for automatic refresh
- Or force-refresh in Streamlit Cloud (Manage app → Reboot app)

### Riders not showing up in Team Riders tab

**Cause**: Rider URL format is wrong

**Fix**:
- Use format `rider/firstname-lastname`
- Match exactly what's on ProCyclingStats URL
- No trailing slashes, no `https://`, just `rider/name`

---

## Advanced: Multiple Sheets

If you want to organize rosters across multiple sheets/tabs:

1. Create tabs for each race (e.g., "Giro 2026", "TDF 2026")
2. Each tab should have the same column structure
3. Update the import code to read from specific tab:
   ```python
   # In google_sheets_import.py, update csv_url:
   csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
   ```
   where `gid` is the tab ID (visible in tab URL)

**Recommended**: Stick to single sheet for simplicity — just change `Race ID` column per race.

---

## FAQ

**Q: Can I add extra columns for notes?**  
A: Yes! The app only reads columns named `Race ID`, `Participant`, and `Rider1`, `Rider2`, etc. Add whatever other columns you want.

**Q: What if I have more than 5 riders per team?**  
A: Just add more columns: `Rider6`, `Rider7`, ... up to `Rider20` (max supported).

**Q: Can I change rosters during the race?**  
A: Technically yes (sheet updates are cached for 1 hour), but not recommended. Lock rosters before race starts.

**Q: What if a rider DNS/DNF?**  
A: App automatically handles this — DNF/DNS riders are excluded from team scores.

**Q: Can I use this for non-Grand Tour races?**  
A: Yes! Just add new race configs to `races_config.py` with correct ProCyclingStats URLs.

---

## Example for Giro 2026

Here's a complete example for your group:

```csv
Race ID,Participant,Rider1,Rider2,Rider3
giro-2026,Jeremy,rider/primoz-roglic,rider/jai-hindley,rider/joao-almeida
giro-2026,Leo,rider/geraint-thomas,rider/thymen-arensman,rider/andreas-leknessund
giro-2026,Charles,rider/ben-oconnor,rider/eddie-dunbar,rider/einer-rubio
giro-2026,Aaron,rider/antonio-tiberi,rider/mattias-skjelmose,rider/brandon-mcnulty
giro-2026,Nate,rider/giulio-ciccone,rider/lorenzo-fortunato,rider/damiano-caruso
```

After draft, just paste this into your sheet, publish to web, and you're done!

---

**Need help? Check the test output:** `python google_sheets_import.py`
