import streamlit as st
import pandas as pd
import requests

# 1. THE TITLE OF YOUR WEBSITE
st.title("📈 My Simple Stock Screener")
st.write("Fetching live data from Dhan API...")

# 2. YOUR SECRET KEYS (Put yours here)
CLIENT_ID = "YOUR_DHAN_ID"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

# 3. ASKING DHAN FOR DATA
def get_stock_data():
    url = "https://api.dhan.co/marketfeed/ltp" # This is the "phone number" for Dhan
    headers = {
        "access-token": ACCESS_TOKEN,
        "client-id": CLIENT_ID,
        "Content-Type": "application/json"
    }
    
    # We are asking for a few sample stocks (NSE symbols)
    payload = {"instruments": [{"exchangeSegment": "NSE_EQ", "securityId": "1333"}]} # 1333 is HDFC Bank
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# 4. SHOWING IT ON THE SCREEN
if st.button('Refresh Prices'):
    data = get_stock_data()
    st.write("Here is the data we got back:")
    st.json(data)
