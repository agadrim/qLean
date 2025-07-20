import streamlit as st

# Placeholder quoting logic
def compute_quote(market_bid, market_ask, spread=0.01):
    mid = (market_bid + market_ask) / 2
    return mid - spread / 2, mid + spread / 2

# Bloomberg API (blpapi) placeholder
try:
    import blpapi
except ImportError:
    blpapi = None

# Simulated data fetching; replace with real Bloomberg subscription
import random

def fetch_market_data(symbol):
    # This function should connect to Bloomberg and retrieve real-time data
    # For demonstration we return random bids/asks
    return random.uniform(100, 101), random.uniform(101, 102)

st.title("Bloomberg Quote Calculator")

symbol = st.text_input("Symbol", value="AAPL US Equity")

if blpapi is None:
    st.warning("blpapi not installed. Displaying mock data.")

market_bid, market_ask = fetch_market_data(symbol)
proposed_bid, proposed_ask = compute_quote(market_bid, market_ask)

st.subheader("Market Quotes")
col1, col2 = st.columns(2)
col1.metric("Bid", f"{market_bid:.2f}")
col2.metric("Ask", f"{market_ask:.2f}")

st.subheader("Proposed Quotes")
col3, col4 = st.columns(2)
col3.metric("Bid", f"{proposed_bid:.2f}")
col4.metric("Ask", f"{proposed_ask:.2f}")
