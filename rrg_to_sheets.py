import os
import json
import time
from datetime import datetime
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ----------------------------
# Authenticate with Google Sheets
# ----------------------------
creds_dict = json.loads(os.environ["GOOGLE_CREDS"])
creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)

# ----------------------------
# Sheet Info
# ----------------------------
SPREADSHEET_ID = "1KvXSbfEIgMX1il1iFVRCJQbqPXZIU7N7F1nz3TskCX0"
SHEET_NAME = "Nifty_Sector_RRG"

# ----------------------------
# Sector Symbols to Use
# ----------------------------
SECTORS = {
    "NIFTY AUTO": "CNXAUTO",
    "NIFTY BANK": "BANKNIFTY",
    "NIFTY FMCG": "CNXFMCG",
    "NIFTY IT": "CNXIT",
    "NIFTY METAL": "CNXMETAL",
    "NIFTY PHARMA": "CNXPHARMA",
    "NIFTY FINANCIAL SERVICES": "CNXFIN",
    "NIFTY PSU BANK": "CNXPSUBANK",
    "NIFTY REALTY": "CNXREALTY",
    "NIFTY MEDIA": "CNXMEDIA",
    "NIFTY ENERGY": "CNXENERGY",
    "NIFTY COMMODITIES": "CNXCOMMODITIES"
}

# ----------------------------
# Dummy Function: Replace with actual RRG logic or API
# ----------------------------
def fetch_rrg_metrics(sector):
    import random
    return {
        "RS_Ratio": round(random.uniform(95, 110), 2),
        "RS_Momentum": round(random.uniform(90, 110), 2),
        "Quadrant": random.choice(["Leading", "Weakening", "Lagging", "Improving"])
    }

# ----------------------------
# Fetch and Append RRG Data to Google Sheet
# ----------------------------
def update_rrg_sheet():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

    print(f"🟢 Starting RRG update at {timestamp}...\n")

    for name, symbol in SECTORS.items():
        try:
            data = fetch_rrg_metrics(symbol)
            row = [timestamp, name, symbol, data["RS_Ratio"], data["RS_Momentum"], data["Quadrant"]]
            sheet.append_row(row, value_input_option="USER_ENTERED")
            print(f"✅ Logged {name}: {row}")
        except Exception as e:
            print(f"❌ Failed to log {name} ({symbol}): {e}")

    print(f"\n✅ All updates attempted at {timestamp}.")

if __name__ == "__main__":
    update_rrg_sheet()
