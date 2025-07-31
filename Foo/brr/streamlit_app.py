import streamlit as st
import pandas as pd
from datetime import datetime

# ------------------ Page Setup ------------------
st.set_page_config(page_title="Sri Aadya Maintenance", page_icon="🏠", layout="centered")

# ------------------ Flat Owners ------------------
owners = {
    "Flat G1 #": "Shiva Shanker",
    "Flat G2 #": "Ashish R",
    "Flat 101 #": "Girish Babu C",
    "Flat 102 #": "Bala Krishnan",
    "Flat 201 #": "Srinivas",
    "Flat 202 #": "Kalaiselvi M",
    "Flat 301 #": "Girish V",
    "Flat 302 #": "Balaram",
    "Flat 401 #": "Pavan",
    "Flat 402 #": "Suresh"
}

# ------------------ App State ------------------
def initialize_state():
    if "monthly_data" not in st.session_state:
        # Sample data for 2 months: July and August 2025
        st.session_state.monthly_data = {
            "July 2025": {
                "payments": {flat: 300 for flat in owners},
                "expenses": {
                    "Watchman Salary": 4000,
                    "Electricity Bill": 1500,
                    "Water Bill": 1000
                }
            },
            "August 2025": {
                "payments": {flat: 300 for flat in owners},
                "expenses": {
                    "Watchman Salary": 4000,
                    "Electricity Bill": 1600,
                    "Water Bill": 1200
                }
            }
        }

initialize_state()

# ------------------ Sidebar ------------------
st.sidebar.title("📌 Menu")
menu = ["🏠 Monthly Summary", "📋 Flat Collection", "📊 Expense Details"]
choice = st.sidebar.radio("Navigate", menu)

# ------------------ Select Month ------------------
months = list(st.session_state.monthly_data.keys())
selected_month = st.sidebar.selectbox("📅 Select Month", months)

# Get data for selected month
month_data = st.session_state.monthly_data[selected_month]
payments = month_data["payments"]
expenses = month_data["expenses"]

# ------------------ Dashboard ------------------
if choice == "🏠 Monthly Summary":
    st.markdown(f"### 📊 Summary – {selected_month}")

    total_collected = sum(payments.values())
    total_expenses = sum(expenses.values())
    balance = total_collected - total_expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("🧾 Collected", f"₹{total_collected}")
    col2.metric("💸 Expenses", f"₹{total_expenses}")
    col3.metric("💰 Balance", f"₹{balance}")

    st.markdown("---")
    st.markdown("✔ Use the sidebar to view flat-wise collection or full expense breakdown.")

# ------------------ Flat Collection ------------------
elif choice == "📋 Flat Collection":
    st.markdown(f"### 📋 Flat-wise Payment – {selected_month}")

    df = pd.DataFrame({
        "Flat Number": list(owners.keys()),
        "Resident Name": list(owners.values()),
        "Paid Amount (₹)": list(payments.values())
    })

    st.dataframe(df, use_container_width=True)

# ------------------ Expense Details ------------------
elif choice == "📊 Expense Details":
    st.markdown(f"### 💼 Expenses – {selected_month}")

    col1, col2, col3 = st.columns(3)
    expense_names = list(expenses.keys())

    for i, expense in enumerate(expense_names):
        with [col1, col2, col3][i % 3]:
            st.write(f"🔹 {expense}")
            st.metric(label="", value=f"₹{expenses[expense]}")

    total_exp = sum(expenses.values())
    st.success(f"💵 **Total Expense:** ₹{total_exp}")
