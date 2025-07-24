import streamlit as st
import pandas as pd
from datetime import datetime

# Setup
st.set_page_config(page_title="Apartment Maintenance Tracker", layout="wide")

# Flat Owners
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

# Session State
if "payments" not in st.session_state:
    st.session_state.payments = {flat: 1000 for flat in owners}
if "expenses" not in st.session_state:
    st.session_state.expenses = {
        "Watchman Salary": 3000,
        "Power Bill": 1000,
        "Water Bill": 500,
        "Plumber Charges": 0,
        "Lift Maintenance": 0,
        "Other Expenses": 0
    }
if "previous_outstanding" not in st.session_state:
    st.session_state.previous_outstanding = 0

# Sidebar: Month selection + Outstanding
st.sidebar.markdown("### 📅 Select Month")
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
current_month = datetime.now().month
selected_month = st.sidebar.selectbox("Month", months, index=current_month - 1)

st.sidebar.markdown("---")
st.session_state.previous_outstanding = st.sidebar.number_input(
    "📌 Previous Outstanding (₹)", value=0, step=100
)

# 🧭 Styled Navigation Tabs (instead of radio buttons)
tabs = {
    "Dashboard": "📊 Dashboard",
    "Payments": "💰 Add Payments",
    "Expenses": "📉 Add Expenses"
}
selected_tab = st.selectbox("📍 Navigate to:", list(tabs.keys()), format_func=lambda x: tabs[x])

st.markdown(f"## {tabs[selected_tab]}")
st.markdown(f"#### 🗓️ Month: `{selected_month}`")

st.markdown("---")

# 1️⃣ Dashboard View
if selected_tab == "Dashboard":
    total_collected = sum(st.session_state.payments.values())
    total_expenses = sum(st.session_state.expenses.values())
    balance = total_collected + st.session_state.previous_outstanding - total_expenses

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💵 Coll
