import streamlit as st
import pandas as pd
import requests

st.title("📈 My Simple Stock Screener")
st.write("Fetching live data from Dhan API...")

# --- 1. YOUR SECRET KEYS ---
CLIENT_ID = "1100513955"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzc4ODQwMjE4LCJpYXQiOjE3Nzg3NTM4MTgsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwNTEzOTU1In0.TPkPSA880q6Pu0IG9nHQ9bDzav_30ixNlX1t2-x7PDUFUntiEHn6NiOdBRtxKIPkWBFc82_Obf0sBbXdzJPa7A"

# --- 2. THE BRAIN ---
def get_stock_data():
    url = "https://api.dhan.co/v2/marketfeed/ltp"
    headers = {
        "access-token": ACCESS_TOKEN,
        "client-id": CLIENT_ID,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"NSE_EQ": [1333, 11536, 2885]} 
    response = requests.post(url, json=payload, headers=headers)
    return response.json() if response.status_code == 200 else None

# --- 3. THE POST-IT NOTE (Memory) ---
# This check says: "If we don't have a post-it note named 'my_data' yet, create an empty one."
if 'my_data' not in st.session_state:
    st.session_state['my_data'] = None

# --- 4. THE BUTTON ---
if st.button('Refresh Prices'):
    result = get_stock_data()
    if result:
        # We save the data onto our Post-it Note!
        st.session_state['my_data'] = result
        st.success("Data Updated!")

# --- 5. THE SCREENER (Always visible if we have data) ---
# If the Post-it Note is NOT empty, show the table
if st.session_state['my_data'] is not None:
    raw_data = st.session_state['my_data']['data']['NSE_EQ']
    names = {"1333": "HDFC Bank", "11536": "TCS", "2885": "Reliance"}
    
    rows = []
    for stock_id, details in raw_data.items():
        rows.append({
            "Stock Name": names.get(stock_id, stock_id),
            "Last Price": details['last_price']
        })
    
    df = pd.DataFrame(rows)

    st.divider() # Adds a nice line
    st.subheader("🔍 ScanX Style Filters")
    
    # Now when you move this slider, the table won't disappear!
    min_price = st.slider("Show stocks with price higher than:", 0, 4000, 0)
    
    filtered_df = df[df['Last Price'] >= min_price]
    st.table(filtered_df)
else:
    st.info("Click the button above to load the stock prices for the first time.")
