import streamlit as st
from collections import defaultdict

# Static flat data
flat_owners = {
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

monthly_maintenance = 3000  # per flat

# In-memory expense data storage
if "expenses" not in st.session_state:
    st.session_state.expenses = defaultdict(list)

# Utility functions
def get_total_collected():
    return len(flat_owners) * monthly_maintenance

def get_total_expenses(month):
    return sum(entry["amount"] for entry in st.session_state.expenses[month])

def get_balance(month):
    return get_total_collected() - get_total_expenses(month)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(" ", ["🏠 Dashboard", "📋 Flat Status", "📊 Expenses"])

selected_month = st.sidebar.selectbox("Select Month", [f"{y}-{m:02}" for y in range(2024, 2026) for m in range(1, 13)])

# Dashboard
if page == "🏠 Dashboard":
    st.title("🏠 Sri Aadya Maintenance Dashboard")

    total_collected = get_total_collected()
    total_expenses = get_total_expenses(selected_month)
    balance = get_balance(selected_month)

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Collected", f"₹{total_collected}")
    col2.metric("🪙 Total Expenses", f"₹{total_expenses}")
    col3.metric("📦 Balance", f"₹{balance}")

    st.divider()
    st.subheader(f"🔄 Summary for {selected_month}")
    st.write("Collection and expense summary for the selected month.")

# Flat Status Page
elif page == "📋 Flat Status":
    st.title("📋 Flat Wise Monthly Status")
    st.write(f"**Monthly Collection: ₹{monthly_maintenance} per flat**")

    st.markdown("### Collection Status")
    for flat, owner in flat_owners.items():
        st.success(f"{flat} - {owner}: ₹{monthly_maintenance} paid for {selected_month}")

# Expenses Page
elif page == "📊 Expenses":
    st.title("📊 Add Monthly Expenses")
    st.write(f"Add expenses for **{selected_month}**")

    with st.form("expense_form"):
        description = st.text_input("Expense Description")
        amount = st.number_input("Amount (₹)", min_value=0, step=100)
        submitted = st.form_submit_button("Add Expense")
        if submitted and description and amount > 0:
            st.session_state.expenses[selected_month].append({"description": description, "amount": amount})
            st.success("Expense added!")

    st.divider()
    st.subheader(f"📄 Expense List for {selected_month}")
    expense_list = st.session_state.expenses[selected_month]
    if expense_list:
        for idx, entry in enumerate(expense_list, start=1):
            st.write(f"**{idx}. {entry['description']}** — ₹{entry['amount']}")
    else:
        st.info("No expenses added yet.")
