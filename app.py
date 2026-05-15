import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(layout="wide")
st.title("🚀 My ScanX Clone (Pro Dashboard)")

# --- 1. YOUR SECRET KEYS ---
CLIENT_ID = "1100513955"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzc4ODQwMjE4LCJpYXQiOjE3Nzg3NTM4MTgsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwNTEzOTU1In0.TPkPSA880q6Pu0IG9nHQ9bDzav_30ixNlX1t2-x7PDUFUntiEHn6NiOdBRtxKIPkWBFc82_Obf0sBbXdzJPa7A"

# --- 2. THE NIFTY 50 DICTIONARY ---
NIFTY_50 = {
    2885: "RELIANCE", 11536: "TCS", 1333: "HDFCBANK", 1270: "ICICIBANK",
    10604: "BHARTIARTL", 3045: "SBIN", 1594: "INFY", 1394: "ITC",
    1348: "HINDUNILVR", 11483: "LT", 317: "BAJFINANCE", 7229: "HCLTECH",
    10999: "MARUTI", 3351: "SUNPHARMA", 3456: "TATAMOTORS", 2031: "M&M",
    1922: "KOTAKBANK", 11630: "NTPC", 5900: "AXISBANK", 3506: "TITAN",
    11532: "ULTRACEMCO", 236: "ASIANPAINT", 16675: "BAJAJFINSV", 2475: "ONGC",
    3499: "TATASTEEL", 1363: "HINDALCO", 20374: "COALINDIA", 14977: "POWERGRID",
    3787: "WIPRO", 17963: "NESTLEIND", 11723: "JSWSTEEL", 1232: "GRASIM",
    13538: "TECHM", 694: "CIPLA", 16669: "BAJAJ-AUTO", 157: "APOLLOHOSP",
    3432: "TATACONSUM", 341: "ADANIPORTS", 25: "ADANIENT", 910: "EICHERMOT",
    10940: "DIVISLAB", 881: "DRREDDY", 1343: "HEROMOTOCO", 547: "BRITANNIA",
    5258: "INDUSINDBK", 467: "HDFCLIFE", 21808: "SBILIFE", 526: "BPCL"
}

# --- 3. THE BRAIN ---
def get_scanx_data():
    url = "https://api.dhan.co/v2/marketfeed/ohlc"
    headers = {
        "access-token": ACCESS_TOKEN,
        "client-id": CLIENT_ID,
        "Content-Type": "application/json"
    }
    stock_ids = list(NIFTY_50.keys())
    payload = {"NSE_EQ": stock_ids} 
    response = requests.post(url, json=payload, headers=headers)
    return response.json() if response.status_code == 200 else None

# --- 4. THE LIVE TICKER SIDEBAR ---
st.sidebar.header("⚙️ Scanner Settings")

# I set this to True so the "Live Ticks" start automatically!
# I also lowered the timer to 3 seconds so it feels faster.
auto_refresh = st.sidebar.checkbox("🟢 Enable Live Auto-Refresh (1s)", value=True)
min_move = st.sidebar.slider("Show stocks up more than (%):", -5.0, 5.0, 0.0)

# --- 5. FETCHING AND ORGANIZING DATA ---
result = get_scanx_data()

if result and "data" in result:
    raw_data = result['data'].get('NSE_EQ', {})
    
    rows = []
    for stock_id_str, details in raw_data.items():
        stock_id = int(stock_id_str)
        
        ltp = details.get('last_price', 0)
        ohlc = details.get('ohlc', {})
        
        open_p = ohlc.get('open', 0)
        high_p = ohlc.get('high', 0)
        low_p = ohlc.get('low', 0)
        prev_close = ohlc.get('close', 0)
        
        # NOTE: Volume might show 0 depending on if Dhan includes it in this specific OHLC link.
        volume = details.get('volume', 0) 
        
        # New Math: Calculating both absolute change and percentage change
        chng = ltp - prev_close
        pct_chng = (chng / prev_close) * 100 if prev_close != 0 else 0
        
        # Renamed to perfectly match your screenshot
        rows.append({
            "SYMBOL": NIFTY_50.get(stock_id, stock_id_str),
            "OPEN": open_p,
            "HIGH": high_p,
            "LOW": low_p,
            "PREV. CLOSE": prev_close,
            "LTP": ltp,
            "CHNG": round(chng, 2),
            "%CHNG": round(pct_chng, 2),
            "VOLUME (shares)": volume
        })
    
    df = pd.DataFrame(rows)

    # Filter based on your slider
    filtered_df = df[df['%CHNG'] >= min_move]

    # --- 6. THE BEAUTY PARLOR (Formatting exactly like Excel) ---
    def color_picker(val):
        color = 'green' if val > 0 else 'red' if val < 0 else 'black'
        return f'color: {color}; font-weight: bold'

    # This forces Streamlit to add two decimal places and commas to the numbers
    format_rules = {
        "OPEN": "{:.2f}",
        "HIGH": "{:.2f}",
        "LOW": "{:.2f}",
        "PREV. CLOSE": "{:.2f}",
        "LTP": "{:.2f}",
        "CHNG": "{:.2f}",
        "%CHNG": "{:.2f}",
        "VOLUME (shares)": "{:,}" # The comma formats millions perfectly!
    }

    # Apply colors ONLY to the CHNG and %CHNG columns, and format the numbers
    styled_df = filtered_df.style.map(color_picker, subset=['CHNG', '%CHNG']).format(format_rules)
    
    # Hide the index (row numbers) to make it look exactly like your screenshot
    st.dataframe(styled_df, use_container_width=True, height=750, hide_index=True)
else:
    st.error("Could not fetch data from Dhan. Please check your Token!")

# --- 7. THE LIVE REFRESH MAGIC ---
if auto_refresh:
    time.sleep(3)
    st.rerun()
