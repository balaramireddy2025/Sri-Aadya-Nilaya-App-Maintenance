import streamlit as st
import pandas as pd

st.set_page_config(page_title="Apartment Maintenance Tracker", layout="wide")

# Owner Info
owners = {
    "Flat G1": "Shiva Shanker",
    "Flat G2": "Ashish R",
    "Flat 101": "Girish Babu C",
    "Flat 102": "Bala Krishnan",
    "Flat 201": "Srinivas",
    "Flat 202": "Kalaiselvi M",
    "Flat 301": "Girish V",
    "Flat 302": "Balaram",
    "Flat 401": "Pavan",
    "Flat 402": "Suresh"
}

st.title("🏢 Apartment Maintenance Tracker")

# Section 1: Monthly Collection
st.header("💰 Monthly Maintenance Collection")
col1, col2 = st.columns(2)

amounts = {}
with col1:
    for flat, name in owners.items():
        amt = st.number_input(f"{flat} - {name}", min_value=0, value=1000, step=100, key=flat)
        amounts[flat] = amt

total_collection = sum(amounts.values())
st.success(f"✅ Total Collected: ₹{total_collection}")

# Section 2: Expenses
st.header("📉 Monthly Expenses")
watchman = st.number_input("Watchman Salary", min_value=0, value=3000, step=500)
power = st.number_input("Electricity Bill", min_value=0, value=1000, step=100)
water = st.number_input("Water Bill", min_value=0, value=500, step=100)
others = st.number_input("Other Expenses", min_value=0, value=0, step=100)

total_expenses = watchman + power + water + others
st.warning(f"📊 Total Expenses: ₹{total_expenses}")

# Section 3: Balance
balance = total_collection - total_expenses
st.header("📈 Monthly Summary")
st.info(f"💼 Balance Leftover: ₹{balance}")

# Optional: Display Data Table
if st.checkbox("Show Full Payment Table"):
    df = pd.DataFrame({
        "Flat Number": list(owners.keys()),
        "Resident Name": list(owners.values()),
        "Amount Paid": list(amounts.values())
    })
    st.dataframe(df)
