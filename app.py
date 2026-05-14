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
if st.button('Refresh Prices'):
    result = get_stock_data()
    
    if "error" in result:
        st.error("Connection Error. Check your Token!")
        st.write(result["details"])
    else:
        # Digging out the prices
        raw_data = result['data']['NSE_EQ']
        
        # Nicknames for the IDs
        names = {
            "1333": "HDFC Bank",
            "11536": "TCS",
            "2885": "Reliance"
        }
        
        # Building the list for our table
        rows = []
        for stock_id, details in raw_data.items():
            rows.append({
                "Stock Name": names.get(stock_id, stock_id),
                "Last Price": details['last_price']
            })
        
        # Putting it into a pretty table
        df = pd.DataFrame(rows)
        st.success("Screener Updated!")
        st.table(df)
