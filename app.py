import streamlit as st
import pandas as pd
import requests
import time # We need this for our timer!

st.set_page_config(layout="wide")
st.title("🚀 My ScanX Clone (Nifty 50 Edition)")
st.write("Scanning the top 50 companies in India in real-time.")

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


# --- 4. THE SCANX SIDEBAR ---
st.sidebar.header("⚙️ Scanner Settings")

# This is our new "Live TV" switch!
auto_refresh = st.sidebar.checkbox("🟢 Enable Live Auto-Refresh (1s)")
min_move = st.sidebar.slider("Show stocks up more than (%):", -5.0, 5.0, 0.0)


# --- 5. FETCHING THE DATA ---
result = get_scanx_data()

if result and "data" in result:
    raw_data = result['data'].get('NSE_EQ', {})
    
    rows = []
    for stock_id_str, details in raw_data.items():
        stock_id = int(stock_id_str)
        
        # 1. Grab the Last Traded Price
        ltp = details.get('last_price', 0)
        
        # 2. THE FIX: Open the 'ohlc' folder!
        ohlc = details.get('ohlc', {})
        
        # 3. Pull the specific prices out of that folder safely
        open_p = ohlc.get('open', 0)
        prev_close = ohlc.get('close', 0)
        high_p = ohlc.get('high', 0)
        low_p = ohlc.get('low', 0)
        
        change = ((ltp - prev_close) / prev_close) * 100 if prev_close != 0 else 0
        
        rows.append({
            "Stock": NIFTY_50.get(stock_id, stock_id_str),
            "Prev. Close": prev_close,
            "Today's Open": open_p,
            "Day High": high_p,
            "Day Low": low_p,
            "LTP (Current)": ltp,
            "Change %": round(change, 2)
        })
    
    df = pd.DataFrame(rows)

    def color_picker(val):
        color = 'green' if val > 0 else 'red' if val < 0 else 'black'
        return f'color: {color}; font-weight: bold'

    # Filter the table based on your slider
    filtered_df = df[df['Change %'] >= min_move]
    
    # Apply colors
    styled_df = filtered_df.style.map(color_picker, subset=['Change %'])
    
    # Show the table
    st.dataframe(styled_df, use_container_width=True, height=600)
else:
    st.error("Could not fetch data from Dhan. Please check your Token!")

# --- 6. THE LIVE REFRESH MAGIC ---
# If you turned the switch on, wait 5 seconds, then erase the board and run everything again automatically!
if auto_refresh:
    time.sleep(5)
    st.rerun()
