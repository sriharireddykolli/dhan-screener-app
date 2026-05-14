import streamlit as st
import pandas as pd
import requests

st.title("🚀 My ScanX Clone")
st.write("Real-time Market Scanner")

# --- 1. YOUR SECRET KEYS ---
CLIENT_ID = "1100513955"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzc4ODQwMjE4LCJpYXQiOjE3Nzg3NTM4MTgsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwNTEzOTU1In0.TPkPSA880q6Pu0IG9nHQ9bDzav_30ixNlX1t2-x7PDUFUntiEHn6NiOdBRtxKIPkWBFc82_Obf0sBbXdzJPa7A"

# --- 2. THE BRAIN (Now asking for OHLC) ---
def get_scanx_data():
    # We changed the link to /ohlc
    url = "https://api.dhan.co/v2/marketfeed/ohlc"
    headers = {
        "access-token": ACCESS_TOKEN,
        "client-id": CLIENT_ID,
        "Content-Type": "application/json"
    }
    # Asking for HDFC Bank, TCS, and Reliance
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
        ltp = details['last_price']
        open_p = details['open']
        
        # BABY MATH: (Current Price - Opening Price) / Opening Price * 100
        change = ((ltp - open_p) / open_p) * 100
        
        rows.append({
            "Stock": names.get(stock_id, stock_id),
            "LTP": ltp,
            "Day High": details['high'],
            "Day Low": details['low'],
            "% Change": round(change, 2)
        })
    
    df = pd.DataFrame(rows)

    st.divider()
    
    # SCANX FILTER: Percentage Filter
    st.subheader("🎯 Percentage Mover Filter")
    min_move = st.sidebar.slider("Show stocks up more than (%):", -5.0, 5.0, 0.0)
    
    filtered_df = df[df['% Change'] >= min_move]
    
    # Display the table
    st.dataframe(filtered_df.style.highlight_max(axis=0, subset=['% Change'], color='#90ee90'))
else:
    st.info("Click 'Run Scanner' to start.")
