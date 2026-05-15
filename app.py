import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("🚀 My ScanX Clone (Nifty 50 Edition)")
st.write("Scanning the top 50 companies in India in real-time.")

# --- 1. YOUR SECRET KEYS ---
CLIENT_ID = "1100513955"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzc4ODQwMjE4LCJpYXQiOjE3Nzg3NTM4MTgsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwNTEzOTU1In0.TPkPSA880q6Pu0IG9nHQ9bDzav_30ixNlX1t2-x7PDUFUntiEHn6NiOdBRtxKIPkWBFc82_Obf0sBbXdzJPa7A"

# --- 2. THE NIFTY 50 DICTIONARY ---
# These are the official NSE Token IDs for the Nifty 50 stocks
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
    
    # THE MAGIC TRICK: We tell Python to just grab all the ID numbers from our dictionary!
    # No more typing them out one by one.
    stock_ids = list(NIFTY_50.keys())
    payload = {"NSE_EQ": stock_ids} 
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json() if response.status_code == 200 else None

# --- 4. MEMORY ---
if 'my_data' not in st.session_state:
    st.session_state['my_data'] = None

# --- 5. REFRESH BUTTON ---
if st.button('Run Nifty 50 Scanner'):
    result = get_scanx_data()
    if result:
        st.session_state['my_data'] = result
        st.success("All 50 Stocks Updated!")

# --- 6. THE SCANX TABLE ---
if st.session_state['my_data'] is not None:
    raw_data = st.session_state['my_data']['data']['NSE_EQ']
    
    rows = []
    # We loop through all the data Dhan sent back
    for stock_id_str, details in raw_data.items():
        stock_id = int(stock_id_str) # Convert string back to number
        
        # Safely grab the exact prices you asked for
        ltp = details.get('last_price', 0)
        open_p = details.get('open', 0)
        prev_close = details.get('close', 0) # In the OHLC feed, 'close' means Yesterday's Close
        
        # Professional standard: Calculate % change based on Yesterday's Close
        change = ((ltp - prev_close) / prev_close) * 100 if prev_close != 0 else 0
        
        rows.append({
            "Stock": NIFTY_50.get(stock_id, stock_id_str), # Get the name from our dictionary
            "Prev. Close": prev_close,
            "Today's Open": open_p,
            "LTP (Current)": ltp,
            "Change %": round(change, 2)
        })
    
    df = pd.DataFrame(rows)

    # --- 7. COLOR LOGIC ---
    def color_picker(val):
        color = 'green' if val > 0 else 'red' if val < 0 else 'black'
        return f'color: {color}; font-weight: bold'

    styled_df = df.style.applymap(color_picker, subset=['Change %'])

    st.divider()
    
    # SCANX SIDEBAR FILTERS
    st.sidebar.header("Filter Settings")
    min_move = st.sidebar.slider("Show stocks up more than (%):", -5.0, 5.0, 0.0)
    
    # Apply the filter
    filtered_df = df[df['Change %'] >= min_move]
    
    st.success(f"Scanning complete! Showing {len(filtered_df)} stocks.")
    st.dataframe(styled_df, use_container_width=True, height=600)
    
else:
    st.info("Click 'Run Nifty 50 Scanner' to load the market data.")
