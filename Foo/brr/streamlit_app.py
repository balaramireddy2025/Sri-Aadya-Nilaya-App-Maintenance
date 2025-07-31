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
    if "payments" not in st.session_state:
        st.session_state.payments = {}  # { "YYYY-MM": {flat: amount} }

    if "expenses" not in st.session_state:
        st.session_state.expenses = {}  # { "YYYY-MM": {"label": amount} }

initialize_state()

# ------------------ Helpers ------------------
def get_current_month():
    return datetime.now().strftime("%Y-%m")

def ensure_month_data(month):
    if month not in st.session_state.payments:
        st.session_state.payments[month] = {flat: 3000 for flat in owners}
    if month not in st.session_state.expenses:
        st.session_state.expenses[month] = {
            "Watchman Salary": 4000,
            "Electricity Bill": 1500,
            "Water Bill": 1000
        }

current_month = get_current_month()
ensure_month_data(current_month)

# ------------------ Sidebar ------------------
menu = ["🏠 Dashboard", "📋 Flat Status", "📊 Expenses"]
choice = st.sidebar.radio("Navigation", menu)
month_selected = st.sidebar.selectbox("Select Month", options=sorted(st.session_state.payments.keys()), index=len(st.session_state.payments) - 1)

# ------------------ Dashboard ------------------
if choice == "🏠 Dashboard":
    st.markdown("## 🏠 Sri Aadya Maintenance Dashboard")

    collected = sum(st.session_state.payments[month_selected].values())
    expenses = sum(st.session_state.expenses[month_selected].values())
    balance = collected - expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Collected", f"₹{collected}")
    col2.metric("💸 Total Expenses", f"₹{expenses}")
    col3.metric("📦 Balance", f"₹{balance}")

    st.markdown("---")
    st.markdown(f"### 🔄 Summary for {month_selected}")
    st.write("Collection and expense summary for the selected month.")

# ------------------ Flat-wise Payment ------------------
elif choice == "📋 Flat Status":
    st.markdown(f"## 📋 Maintenance Collection - {month_selected}")

    df = pd.DataFrame({
        "Flat Number": list(owners.keys()),
        "Resident Name": list(owners.values()),
        "Paid (₹)": list(st.session_state.payments[month_selected].values())
    })

    st.dataframe(df, use_container_width=True)

# ------------------ Expenses ------------------
elif choice == "📊 Expenses":
    st.markdown(f"## 📊 Monthly Expenses - {month_selected}")
    month_exp = st.session_state.expenses[month_selected]

    total = sum(month_exp.values())
    for label, amount in month_exp.items():
        st.write(f"**{label}**: ₹{amount}")

    st.success(f"💵 Total Monthly Expense: ₹{total}")

    with st.expander("➕ Add or Update Expense"):
        new_label = st.text_input("Expense Name")
        new_amount = st.number_input("Amount (₹)", min_value=0, step=100)

        if st.button("Add/Update Expense"):
            if new_label:
                month_exp[new_label] = new_amount
                st.success(f"✅ Expense '{new_label}' updated for {month_selected}")
