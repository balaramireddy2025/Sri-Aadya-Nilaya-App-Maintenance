import streamlit as st
import pandas as pd
from datetime import datetime

# Page config with custom icon and wide layout
st.set_page_config(page_title="Sri Aadya Maintenance", page_icon="🏠", layout="wide")

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
def initialize_state():
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

initialize_state()

# Sidebar - Month and Outstanding
with st.sidebar:
    st.markdown("## 🗓️ Select Month")
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    current_month = datetime.now().month
    selected_month = st.selectbox("Month", months, index=current_month - 1)

    st.markdown("---")
    st.session_state.previous_outstanding = st.number_input(
        "📌 Previous Outstanding (₹)", value=0, step=100
    )

    st.markdown("---")
    st.markdown("## 📍 Navigation")
    selected_tab = st.radio("Go to", ["Dashboard", "Flat Payments", "Monthly Expenses"])

st.markdown(f"# 🏠 Sri Aadya Maintenance - {selected_tab}")
st.markdown(f"### 📅 Month: `{selected_month}`")
st.markdown("---")

# ----------------- Dashboard -------------------
if selected_tab == "Dashboard":
    total_collected = sum(st.session_state.payments.values())
    total_expenses = sum(st.session_state.expenses.values())
    balance = total_collected + st.session_state.previous_outstanding - total_expenses

    st.markdown("### 🔍 Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Collected", f"₹{total_collected}")
    col2.metric("📌 Previous Outstanding", f"₹{st.session_state.previous_outstanding}")
    col3.metric("📉 Total Expenses", f"₹{total_expenses}")
    col4.metric("💼 Remaining Balance", f"₹{balance}")

    st.markdown("### 🧾 Flat-wise Payment Status")
    df_pay = pd.DataFrame({
        "Flat Number": list(owners.keys()),
        "Resident Name": list(owners.values()),
        "Amount Paid (₹)": list(st.session_state.payments.values())
    })
    st.dataframe(df_pay, use_container_width=True, height=300)

    st.markdown("### 📊 Expense Breakdown")
    df_exp = pd.DataFrame({
        "Expense": list(st.session_state.expenses.keys()),
        "Amount (₹)": list(st.session_state.expenses.values())
    })
    st.dataframe(df_exp, use_container_width=True, height=250)

# ----------------- Payments -------------------
elif selected_tab == "Flat Payments":
    st.markdown("### 💰 Enter Amount Paid by Each Flat")
    for flat, name in owners.items():
        value = st.number_input(
            f"{flat} - {name}",
            min_value=0,
            value=st.session_state.payments.get(flat, 1000),
            step=100,
            key=f"pay_{flat}"
        )
        st.session_state.payments[flat] = value
    st.success("✅ Payments updated successfully!")

# ----------------- Expenses -------------------
elif selected_tab == "Monthly Expenses":
    st.markdown("### 🧾 Enter Monthly Expenses")
    for expense in st.session_state.expenses:
        value = st.number_input(
            f"{expense}",
            min_value=0,
            value=st.session_state.expenses[expense],
            step=100,
            key=f"exp_{expense}"
        )
        st.session_state.expenses[expense] = value
    st.success("✅ Expenses updated successfully!")
