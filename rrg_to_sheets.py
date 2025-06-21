import yfinance as yf
import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with Google Sheets
creds_json = json.loads(os.environ["GOOGLE_CREDS"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# Open your sheet
sheet = client.open("Nifty_Sector_RRG").sheet1

# Define symbols
symbols = [
    "NIFTY 50", "NIFTY BANK", "NIFTY IT", "NIFTY AUTO", "NIFTY FMCG",
    "NIFTY PHARMA", "NIFTY REALTY", "NIFTY PSU BANK", "NIFTY PVT BANK",
    "NIFTY ENERGY", "NIFTY COMMODITIES", "NIFTY CONSUMPTION"
]

# Start data list
rows = []

for s in range(len(symbols)):
    try:
        # Download Close price
        data = yf.download(symbols[s], period="21d", interval="1d", progress=False)["Close"]

        # Skip if empty or None
        if data is None or data.empty:
            print(f"[SKIPPED] No data for {symbols[s]}")
            continue

        # Compute relative strength (example logic: latest close / average close)
        latest = data[-1]
        avg = data.mean()
        rs = round((latest / avg) * 100, 2)
        mom = round((latest - data[-5]) / data[-5] * 100, 2) if len(data) >= 5 else 0

        rows.append([symbols[s], rs, mom])

    except Exception as e:
        print(f"[ERROR] Symbol {symbols[s]} failed → {str(e)}")
        continue

# Write header + data
sheet.clear()
sheet.append_row(["Sector", "RS %", "Momentum"])
sheet.append_rows(rows)
print("✅ Sheet Updated Successfully")
