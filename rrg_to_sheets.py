import yfinance as yf, pandas as pd, os, json
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# ✅ Load credentials from GitHub Actions secret
creds_data = json.loads(os.environ["GOOGLE_CREDS"])
with open("temp_creds.json", "w") as f:
    json.dump(creds_data, f)

# ✅ Authorize with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("temp_creds.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("Nifty_Sector_RRG").sheet1

# ✅ NSE Sector symbols from Yahoo Finance
symbols = {
    "NIFTY": "^NSEI",       # Benchmark
    "IT": "^CNXIT",
    "BANK": "^NSEBANK",
    "FMCG": "^CNXFMCG",
    "METAL": "^CNXMETAL",
    "AUTO": "^CNXAUTO"
}

# ✅ Download last 21 days of prices
data = {s: yf.download(symbols[s], period="21d", interval="1d", progress=False)["Close"]
        for s in symbols}
df = pd.DataFrame(data)

# ✅ Calculate RS% and Momentum
today = datetime.today().strftime("%Y-%m-%d")
benchmark = df["NIFTY"]

for sector in symbols:
    if sector == "NIFTY":
        continue
    rs = df[sector] / benchmark
    rs_pct = ((rs.iloc[-1] - rs[-20:].mean()) / rs[-20:].mean()) * 100
    momentum = rs_pct - ((rs.iloc[-2] - rs[-21:-1].mean()) / rs[-21:-1].mean()) * 100
    sheet.append_row([today, sector, round(rs_pct, 2), round(momentum, 2)])

print("✅ Uploaded to Google Sheets successfully")
