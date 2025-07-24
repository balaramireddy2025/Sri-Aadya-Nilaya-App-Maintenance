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
    col1.metric("💵 Collected", f"₹{total_collected}")
    col2.metric("📌 Prev. Outstanding", f"₹{st.session_state.previous_outstanding}")
    col3.metric("📉 Expenses", f"₹{total_expenses}")
    col4.metric("💼 Balance", f"₹{balance}")

    st.markdown("### 🧾 Maintenance Payments")
    df_pay = pd.DataFrame({
        "Flat Number": list(owners.keys()),
        "Resident Name": list(owners.values()),
        "Amount Paid (₹)": list(st.session_state.payments.values())
    })
    st.dataframe(df_pay, use_container_width=True)

    st.markdown("### 🧮 Expense Breakdown")
    df_exp = pd.DataFrame({
        "Expense": list(st.session_state.expenses.keys()),
        "Amount (₹)": list(st.session_state.expenses.values())
    })
    st.dataframe(df_exp, use_container_width=True)

# 2️⃣ Add Payments View
elif selected_tab == "Payments":
    st.markdown("Enter amount paid by each flat:")
    for flat, name in owners.items():
        value = st.number_input(
            f"{flat} - {name}",
            min_value=0,
            value=st.session_state.payments.get(flat, 1000),
            step=100,
            key=f"pay_{flat}"
        )
        st.session_state.payments[flat] = value

    st.success("✅ Payments saved successfully!")

# 3️⃣ Add Expenses View
elif selected_tab == "Expenses":
    st.markdown("Enter detailed monthly expenses:")
    for expense_name in st.session_state.expenses:
        value = st.number_input(
            expense_name,
            min_value=0,
            value=st.session_state.expenses[expense_name],
            step=100,
            key=f"exp_{expense_name}"
        )
        st.session_state.expenses[expense_name] = value

    st.success("✅ Expenses saved successfully!")
