import streamlit as st
import pandas as pd
import requests

st.title("📈 My Simple Stock Screener")
st.write("Fetching live data from Dhan API...")

# 1. YOUR KEYS GO HERE AT THE TOP
CLIENT_ID = "1100513955"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzc4ODQwMjE4LCJpYXQiOjE3Nzg3NTM4MTgsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwNTEzOTU1In0.TPkPSA880q6Pu0IG9nHQ9bDzav_30ixNlX1t2-x7PDUFUntiEHn6NiOdBRtxKIPkWBFc82_Obf0sBbXdzJPa7A"

def get_stock_data():
    url = "https://api.dhan.co/v2/marketfeed/ltp"
    
    # 2. THE HEADERS ARE FIXED (Do not change anything in this box!)
    headers = {
        "access-token": ACCESS_TOKEN,
        "client-id": CLIENT_ID,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "NSE_EQ": [1333, 11536, 2885] 
    } 
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Dhan API Error (Status {response.status_code})", "details": response.text}

if st.button('Refresh Prices'):
    data = get_stock_data()
    
    if "error" in data:
        st.error("Oops! Something went wrong with the connection to Dhan:")
        st.write(data["error"])
        st.write(data["details"])
    else:
        st.success("Data fetched successfully!")
        st.json(data)
