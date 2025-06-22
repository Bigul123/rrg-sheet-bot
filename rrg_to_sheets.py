import os
import json
import gspread
import yfinance as yf
import pandas as pd
from google.oauth2.service_account import Credentials

# Load credentials from GitHub Secret
creds_info = json.loads(os.environ["GOOGLE_CREDS"])
creds = Credentials.from_service_account_info(creds_info, scopes=["https://www.googleapis.com/auth/spreadsheets"])

# Connect to Google Sheet
gc = gspread.authorize(creds)
spreadsheet = gc.open("Nifty_Sector_RRG")  # Change name if your sheet is different
worksheet = spreadsheet.worksheet("Sheet1")  # or use .sheet1

# Sample data logic (replace with your real RRG logic)
symbols = ["NIFTYBEES.NS", "BANKBEES.NS"]
data = []

for symbol in symbols:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1mo")
    if not hist.empty:
        returns = hist['Close'].pct_change().fillna(0)
        momentum = returns[-5:].mean()
        rs = hist['Close'][-1] / hist['Close'][0]
        data.append([symbol, momentum, rs])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Symbol", "Momentum", "RS"])

# Update Sheet
worksheet.clear()
worksheet.update([df.columns.values.tolist()] + df.values.tolist())
