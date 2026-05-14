import streamlit as st
import pandas as pd
import requests

st.title("📈 My Simple Stock Screener")
st.write("Fetching live data from Dhan API...")

# Look closely here! See the quotation marks? You MUST keep them.
# PASTE YOUR KEYS BETWEEN THE QUOTES
CLIENT_ID = "PASTE_ID_HERE"
ACCESS_TOKEN = "PASTE_TOKEN_HERE"

def get_stock_data():
    url = "https://api.dhan.co/marketfeed/ltp"
    headers = {
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzc4ODE2MzQwLCJpYXQiOjE3Nzg3Mjk5NDAsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwNTEzOTU1In0.snVapdkFsnefdng8tjc3e8eUtRggm0eyJsj60eZyQj6rkal7ZN7RIgJVwuDXxM-tYzt2GFG6QvOuFWjidngK1w": ACCESS_TOKEN,
        "1100513955": CLIENT_ID,
        "Content-Type": "application/json"
    }
    
    # Let's ask for HDFC Bank (1333), TCS (11536), and Reliance (2885)
    payload = {
        "instruments": [
            {"exchangeSegment": "NSE_EQ", "securityId": "1333"},
            {"exchangeSegment": "NSE_EQ", "securityId": "11536"},
            {"exchangeSegment": "NSE_EQ", "securityId": "2885"}
        ]
    } 
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if st.button('Refresh Prices'):
    data = get_stock_data()
    st.success("Data fetched successfully!")
    st.json(data)
