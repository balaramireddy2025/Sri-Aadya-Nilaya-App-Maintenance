import streamlit as st
import pandas as pd

# ------------------ Page Setup ------------------
st.set_page_config(page_title="Sri Aadya Maintenance", page_icon="🏠", layout="centered")

# ------------------ Logo and Title ------------------
st.image("https://cdn-icons-png.flaticon.com/512/809/809957.png", width=80)  # Optional logo, replace with your image
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>Sri Aadya Apartments</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Monthly Maintenance Tracker</h4>", unsafe_allow_html=True)
st.markdown("---")

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
        st.session_state.payments = {flat: 300 for flat in owners}  # ₹300 per flat
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
st.sidebar.title("📌 Menu")
menu = ["🏠 Dashboard", "📋 Flat Status", "📊 Expenses"]
choice = st.sidebar.radio("Navigate", menu)

# ------------------ Dashboard ------------------
if choice == "🏠 Dashboard":
    st.markdown("### 📊 Monthly Summary")

    collected = sum(st.session_state.payments.values())
    expenses = sum(st.session_state.expenses.values())
    balance = collected + st.session_state.previous_outstanding - expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("🧾 Collected", f"₹{collected}")
    col2.metric("💸 Expenses", f"₹{expenses}")
    col3.metric("💰 Balance", f"₹{balance}")

    st.markdown("---")
    st.markdown("🔄 Use the sidebar to view flat-wise status or monthly expenses.")

# ------------------ Flat Status ------------------
elif choice == "📋 Flat Status":
    st.markdown("### 📋 Flat-wise Payment Status")

    df = pd.DataFrame({
        "Flat Number": list(owners.keys()),
        "Resident Name": list(owners.values()),
        "Paid Amount (₹)": list(st.session_state.payments.values())
    })

    st.dataframe(df, use_container_width=True)

# ------------------ Expenses ------------------
elif choice == "📊 Expenses":
    st.markdown("### 💼 Monthly Expenses – July 2025")

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

    total_expense = sum(exp.values())
    st.success(f"💵 **Total Expense:** ₹{total_expense}")

    st.markdown("---")
    st.info("Coming soon: Add/Edit expenses directly here!")
