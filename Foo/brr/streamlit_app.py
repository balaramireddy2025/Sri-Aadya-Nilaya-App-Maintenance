import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(page_title="Apartment Maintenance Tracker", layout="wide")

# Owners dictionary
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

# Previous outstanding input in sidebar
st.sidebar.markdown("---")
previous_outstanding = st.sidebar.number_input("📌 Previous Outstanding (if any)", value=0, step=100)

# Sidebar navigation
menu = st.sidebar.radio("🏠 Navigate", ["Dashboard", "Add Payments", "Add Expenses"])

# Session State Initialization
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

# 1️⃣ Dashboard
if menu == "Dashboard":
    st.title("🏢 Maintenance Dashboard")
    st.subheader(f"📆 Month: {selected_month}")

    total_collected = sum(st.session_state.payments.values())
    total_expenses = sum(st.session_state.expenses.values())
    balance = total_collected + previous_outstanding - total_expenses

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Collected", f"₹{total_collected}")
    col2.metric("Previous Outstanding", f"₹{previous_outstanding}")
    col3.metric("Total Expenses", f"₹{total_expenses}")
    col4.metric("Remaining Balance", f"₹{balance}")

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

# 2️⃣ Add Payments
elif menu == "Add Payments":
    st.title("💰 Add Maintenance Payments")
    st.subheader(f"📆 Month: {selected_month}")

    for flat, name in owners.items():
        amt = st.number_input(
            f"{flat} - {name}",
            min_value=0,
            step=100,
            value=st.session_state.payments.get(flat, 1000),
            key=f"payment_{flat}"
        )
        st.session_state.payments[flat] = amt

    st.success("✅ Payments updated successfully!")

# 3️⃣ Add Expenses
elif menu == "Add Expenses":
    st.title("📉 Add Monthly Expenses")
    st.subheader(f"📆 Month: {selected_month}")

    for expense in st.session_state.expenses.keys():
        amt = st.number_input(
            f"{expense}",
            min_value=0,
            step=100,
            value=st.session_state.expenses[expense],
            key=f"expense_{expense}"
        )
        st.session_state.expenses[expense] = amt

    st.success("✅ Expenses updated successfully!")
