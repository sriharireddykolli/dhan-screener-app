import streamlit as st
import pandas as pd
import requests

st.title("📈 My Simple Stock Screener")
st.write("Fetching live data from Dhan API...")

# 1. YOUR KEYS GO HERE AT THE TOP
CLIENT_ID = "1100513955"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzc4ODQwMjE4LCJpYXQiOjE3Nzg3NTM4MTgsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwNTEzOTU1In0.TPkPSA880q6Pu0IG9nHQ9bDzav_30ixNlX1t2-x7PDUFUntiEHn6NiOdBRtxKIPkWBFc82_Obf0sBbXdzJPa7A"

def get_stock_data():
    if st.button('Refresh Prices'):
    result = get_stock_data()
    
    if "error" in result:
        st.error("Connection Error")
        st.write(result["details"])
    else:
        # 1. We dig into the data to find the prices
        raw_data = result['data']['NSE_EQ']
        
        # 2. We create a 'Nickname' list so we know which ID belongs to which company
        names = {
            "1333": "HDFC Bank",
            "11536": "TCS",
            "2885": "Reliance"
        }
        
        # 3. We organize the data into a clean list
        rows = []
        for stock_id, details in raw_data.items():
            rows.append({
                "Stock Name": names.get(stock_id, stock_id),
                "Last Price": details['last_price']
            })
        
        # 4. We turn that list into a beautiful table
        df = pd.DataFrame(rows)
        
        st.success("Screener Updated!")
        
        # This makes the table look clean and professional
        st.table(df)
