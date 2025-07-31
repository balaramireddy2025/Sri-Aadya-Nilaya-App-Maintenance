import streamlit as st
import pandas as pd
from datetime import datetime

# ------------------ Page Setup ------------------
st.set_page_config(page_title="Sri Aadya Maintenance", page_icon="🏠", layout="centered")

# ------------------ Flat Owners ------------------
owners = {
    "G1": "Siva Shankar",
    "G2": "Ashish R",
    "101": "Girish Babu C",
    "102": "Bala Krishnan",
    "201": "Srinivas",
    "202": "Kalaiselvi M",
    "301": "Girish V",
    "302": "Balarami Reddy",
    "401": "Pavan",
    "402": "Suresh"
}

# ------------------ App State ------------------
def initialize_state():
    if "payments" not in st.session_state:
        st.session_state.payments = {flat: 3000 for flat in owners}
    if "expenses" not in st.session_state:
        st.session_state.expenses = {
            "Watchman Salary": 4000,
            "Electricity Bill": 1500,
            "Water Bill": 1000
        }
    if "previous_outstanding" not in st.session_state:
        st.session_state.previous_outstanding = 0

initialize_state()

# ------------------ Sidebar ------------------
menu = ["🏠 Dashboard", "📋 Flat Status", "📊 Expenses"]
choice = st.sidebar.radio("Navigation", menu)

# ------------------ Dashboard Screen ------------------
if choice == "🏠 Dashboard":
    st.markdown("## 🏠 Sri Aadya\n### Maintenance Dashboard")

    collected = sum(st.session_state.payments.values())
    expenses = sum(st.session_state.expenses.values())
    balance = collected + st.session_state.previous_outstanding - expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("🧾 Total Maintenance Collected", f"₹{collected}")
    col2.metric("💸 Monthly Expenses", f"₹{expenses}")
    col3.metric("💰 Balance", f"₹{balance}")

    st.markdown("---")
    st.button("➡️ View Flat Details", use_container_width=True)

# ------------------ Flat-wise Payment Status ------------------
elif choice == "📋 Flat Status":
    st.markdown("## 📋 Flat-wise Payment Status")
    df = pd.DataFrame({
        "Flat No": list(owners.keys()),
        "Owner": list(owners.values()),
        "Paid": ["✅" if v >= 1000 else "❌" for v in st.session_state.payments.values()]
    })
    st.table(df)
    st.button("⬅️ Back to Dashboard", use_container_width=True)

# ------------------ Monthly Expenses ------------------
elif choice == "📊 Expenses":
    st.markdown("## 📊 Monthly Expenses (July 2025)")
    exp = st.session_state.expenses

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("👮 Watchman Salary")
        st.metric(label="", value=f"₹{exp['Watchman Salary']}")

    with col2:
        st.write("💡 Electricity Bill")
        st.metric(label="", value=f"₹{exp['Electricity Bill']}")

    with col3:
        st.write("🚰 Water Bill")
        st.metric(label="", value=f"₹{exp['Water Bill']}")

    st.success(f"💵 Total Expense: ₹{sum(exp.values())}")
    st.button("➕ Add Expense", use_container_width=True)
