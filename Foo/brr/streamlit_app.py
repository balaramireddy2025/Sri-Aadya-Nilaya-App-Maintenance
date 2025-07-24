# 1️⃣ Dashboard Screen
if menu == "Dashboard":
    st.title("🏢 Maintenance Dashboard")
    st.subheader(f"Month: {selected_month}")

    total_collected = sum(st.session_state.payments.values())
    total_expenses = sum(st.session_state.expenses.values())
    prev_due = st.session_state.previous_outstanding
    balance = total_collected + prev_due - total_expenses

    colA, colB, colC, colD = st.columns(4)
    colA.metric("Total Collected", f"₹{total_collected}")
    colB.metric("Previous Outstanding", f"₹{prev_due}")
    colC.metric("Total Expenses", f"₹{total_expenses}")
    colD.metric("Remaining Balance", f"₹{balance}")

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
