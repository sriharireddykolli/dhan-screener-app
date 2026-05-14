import streamlit as st
import pandas as pd
import requests

st.title("🚀 My ScanX Clone")
st.write("Real-time Market Scanner")

# --- 1. YOUR SECRET KEYS ---
CLIENT_ID = "1100513955"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzc4ODQwMjE4LCJpYXQiOjE3Nzg3NTM4MTgsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwNTEzOTU1In0.TPkPSA880q6Pu0IG9nHQ9bDzav_30ixNlX1t2-x7PDUFUntiEHn6NiOdBRtxKIPkWBFc82_Obf0sBbXdzJPa7A"

# --- 2. THE BRAIN ---
def get_scanx_data():
    url = "https://api.dhan.co/v2/marketfeed/ohlc"
    headers = {
        "access-token": ACCESS_TOKEN,
        "client-id": CLIENT_ID,
        "Content-Type": "application/json"
    }
    payload = {"NSE_EQ": [1333, 11536, 2885]} 
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json() if response.status_code == 200 else None

# --- 3. MEMORY ---
if 'my_data' not in st.session_state:
    st.session_state['my_data'] = None

# --- 4. REFRESH BUTTON ---
if st.button('Run Scanner'):
    result = get_scanx_data()
    if result:
        st.session_state['my_data'] = result
        st.success("Scanner Refreshed!")

# --- 5. THE SCANX TABLE ---
if st.session_state['my_data'] is not None:
    raw_data = st.session_state['my_data']['data']['NSE_EQ']
    names = {"1333": "HDFC Bank", "11536": "TCS", "2885": "Reliance"}
    
    rows = []
    for stock_id, details in raw_data.items():
        # --- THE FIX: SAFE READING ---
        # We use .get('label', fallback_value)
        ltp = details.get('last_price', 0)
        open_p = details.get('open', ltp) # If 'open' is missing, use 'ltp'
        high_p = details.get('high', ltp)
        low_p = details.get('low', ltp)
        
        # Calculate % change safely (avoid dividing by zero)
        if open_p != 0:
            change = ((ltp - open_p) / open_p) * 100
        else:
            change = 0
        
        rows.append({
            "Stock": names.get(stock_id, stock_id),
            "LTP": ltp,
            "Day High": high_p,
            "Day Low": low_p,
            "% Change": round(change, 2)
        })
    
    df = pd.DataFrame(rows)

    st.divider()
    
    # SCANX FILTER
    st.sidebar.header("Filter Settings")
    min_move = st.sidebar.slider("Show stocks up more than (%):", -5.0, 5.0, 0.0)
    
    filtered_df = df[df['% Change'] >= min_move]
    
    st.success(f"Scanning complete! Found {len(filtered_df)} matches.")
    st.table(filtered_df)
else:
    st.info("Click 'Run Scanner' to start.")
