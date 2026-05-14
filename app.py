import streamlit as st
import pandas as pd
import requests

# This sets the page title
st.title("📈 My Simple Stock Screener")
st.write("Fetching live data from Dhan API...")

# --- 1. YOUR SECRET KEYS ---
# Carefully paste your ID and Token inside the quotes below
CLIENT_ID = "1100513955"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzc4ODQwMjE4LCJpYXQiOjE3Nzg3NTM4MTgsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwNTEzOTU1In0.TPkPSA880q6Pu0IG9nHQ9bDzav_30ixNlX1t2-x7PDUFUntiEHn6NiOdBRtxKIPkWBFc82_Obf0sBbXdzJPa7A"

# --- 2. THE BRAIN (Asking Dhan for data) ---
def get_stock_data():
    url = "https://api.dhan.co/v2/marketfeed/ltp"
    headers = {
        "access-token": ACCESS_TOKEN,
        "client-id": CLIENT_ID,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    # These are the IDs for HDFC Bank, TCS, and Reliance
    payload = {
        "NSE_EQ": [1333, 11536, 2885] 
    } 
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "API Error", "details": response.text}

# --- 3. THE FACE (The Button and Table) ---
# --- 3. THE FACE & THE SCREENER ---
if st.button('Refresh Prices'):
    result = get_stock_data()
    
    if "error" in result:
        st.error("Connection Error. Check your Token!")
    else:
        raw_data = result['data']['NSE_EQ']
        names = {"1333": "HDFC Bank", "11536": "TCS", "2885": "Reliance"}
        
        rows = []
        for stock_id, details in raw_data.items():
            rows.append({
                "Stock Name": names.get(stock_id, stock_id),
                "Last Price": details['last_price']
            })
        
        # We put our data into the Pandas "Excel" table
        df = pd.DataFrame(rows)
        
        # --- NEW SCANNER FEATURE ---
        st.subheader("🔍 My Custom Screener")
        
        # 1. We create a slider on the website
        # It goes from 0 to 4000, and starts at 0.
        min_price = st.slider("Only show stocks with a price HIGHER than:", 0, 4000, 0)
        
        # 2. THE FILTER (This is what ScanX does!)
        # We tell the table to only keep rows where the price is bigger than our slider
        filtered_df = df[df['Last Price'] >= min_price]
        
        # 3. We show the results
        st.success(f"Found {len(filtered_df)} stocks matching your scan!")
        st.table(filtered_df)
