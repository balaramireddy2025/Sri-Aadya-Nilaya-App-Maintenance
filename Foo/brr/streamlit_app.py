import streamlit as st
import pandas as pd
from datetime import datetime

# Page setup
st.set_page_config(page_title="Apartment Maintenance Tracker", layout="wide")

# Owners data
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

# Month selection
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
current_month = datetime.now().month
selected_month = st.sidebar.selectbox("📅 Select Month", months, index=current_month - 1)

# Navigation
menu = st.sidebar.radio("🏠 Navigate", ["Dashboard", "Add Payments", "Add Expenses"])

# Shared session state
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

# 1️⃣ Dashboard Screen
if menu == "Dashboard":
    st.title("📊 Maintenance Dashboard")
    st.subheader(f"Month: {selected_month}")

    total_collected = sum(st.session_state.payments.values())
    total_expenses = sum(st.session_state.expenses.values())
    balance = total_collected - total_expenses

    st.metric("Total Collected", f"₹{total_collected}")
    st.metric("Total Expenses", f"₹{total_expenses}")
    st.metric("Remaining Balance", f"₹{balance}")

    st.divider()
    st.subheader("🧾 Payment Overview")
    df_pay = pd.DataFrame({
        "Flat Number": list(owners.keys()),
        "Resident Name": list(owners.values()),
        "Amount Paid (₹)": list(st.session_state.payments.values())
    })
    st.dataframe(df_pay, use_container_width=True)

    st.divider()
    st.subheader("📉 Expense Details")
    df_exp = pd.DataFrame({
        "Expense": list(st.session_state.expenses.keys()),
        "Amount (₹)": list(st.session_state.expenses.values())
    })
    st.dataframe(df_exp, use_container_width=True)

# 2️⃣ Payments Screen
elif menu == "Add Payments":
    st.title("💰 Add Maintenance Payments")
    st.subheader(f"Month: {selected_month}")
    for flat, name in owners.items():
        amt = st.number_input(f"{flat} - {name}", min_value=0, step=100,
                              value=st.session_state.payments.get(flat, 1000), key=flat)
        st.session_state.payments[flat] = amt
    st.success("✅ Payments updated!")

# 3️⃣ Expenses Screen
elif menu == "Add Expenses":
    st.title("📉 Add Monthly Expenses")
    st.subheader(f"Month: {selected_month}")
    for exp in st.session_state.expenses:
        value = st.number_input(exp, min_value=0, step=100,
                                value=st.session_state.expenses.get(exp), key=exp)
        st.session_state.expenses[exp] = value
    st.success("✅ Expenses updated!")
