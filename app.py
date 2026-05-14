import streamlit as st
import pandas as pd
import requests

st.title("📈 My Simple Stock Screener")
st.write("Fetching live data from Dhan API...")

# PASTE YOUR KEYS BETWEEN THE QUOTES
CLIENT_ID = "1100513955"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzc4ODQwMjE4LCJpYXQiOjE3Nzg3NTM4MTgsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwNTEzOTU1In0.TPkPSA880q6Pu0IG9nHQ9bDzav_30ixNlX1t2-x7PDUFUntiEHn6NiOdBRtxKIPkWBFc82_Obf0sBbXdzJPa7A"

def get_stock_data():
    # 1. Notice the 'v2' added to the URL here
    url = "https://api.dhan.co/v2/marketfeed/ltp"
    
    headers = {
        "access-token": ACCESS_TOKEN,
        "client-id": CLIENT_ID,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # 2. The new, much simpler way Dhan wants us to list the stocks
    # 1333 = HDFC Bank | 11536 = TCS | 2885 = Reliance
    payload = {
        "NSE_EQ": ["1333", "11536", "2885"] 
    } 
    
    response = requests.post(url, json=payload, headers=headers)
    
    # 3. Our Safety Net: If Dhan is happy (status 200), return the data. 
    # If not, return the exact error message so we can read it.
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Dhan API Error (Status {response.status_code})", "details": response.text}

if st.button('Refresh Prices'):
    data = get_stock_data()
    
    # If our safety net caught an error, show it in red. Otherwise, show the data!
    if "error" in data:
        st.error("Oops! Something went wrong with the connection to Dhan:")
        st.write(data["error"])
        st.write(data["details"])
    else:
        st.success("Data fetched successfully!")
        st.json(data)
