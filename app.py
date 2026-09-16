import numpy as np
import pandas as pd
import streamlit as st

# Page Configuration (Yeh teri website ka title aur tab ka icon/logo set karega!)
st.set_page_config(
    page_title="TripSplit AI - Smart Expense Sharing",
    page_icon="✈️",
    layout="centered",
)

# Custom Styling & Header
st.title("✈️ TripSplit AI")
st.subheader("Smart Trip Expense Manager & Bill Splitter")
st.markdown("---")

# Step 1: Trip Details
trip_name = st.text_input("🌍 Trip Name", "Goa Trip 2026")
friends_input = st.text_input(
    "👥 Enter Friends' Names (comma separated)", "Rahul, Priya, Amit, Neha"
)

# Process friends list
friends = [f.strip() for f in friends_input.split(",") if f.strip()]

if friends:
  st.success(f"Trip initialized for: {', '.join(friends)}")
  st.markdown("---")

  # Step 2: Add Expenses
  st.header("💸 Add an Expense")
  col1, col2, col3 = st.columns(3)

  with col1:
    expense_title = st.text_input("Expense Description", "Dinner at Beach")
  with col2:
    amount = st.number_input("Amount (₹)", min_value=0.0, value=1500.0)
  with col3:
    paid_by = st.selectbox("Paid By", friends)

  split_among = st.multiselect(
      "Split Among", friends, default=friends
  )

  if st.button("Add Expense"):
    if "expenses" not in st.session_state:
      st.session_state.expenses = []

    st.session_state.expenses.append({
        "Title": expense_title,
        "Amount": amount,
        "Paid By": paid_by,
        "Split With": split_among,
    })
    st.success(f"Added '{expense_title}' of ₹{amount} successfully!")

  # Step 3: Show Expense History & Calculations
  if "expenses" in st.session_state and st.session_state.expenses:
    st.markdown("---")
    st.header("📊 Expense History")

    df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(df, use_container_width=True)

    # Calculate Balances using NumPy/Pandas logic
    st.markdown("---")
    st.header("⚖️ Settlement Summary")

    balances = {friend: 0.0 for friend in friends}

    for exp in st.session_state.expenses:
      payer = exp["Paid By"]
      amt = exp["Amount"]
      consumers = exp["Split With"]

      if consumers:
        share = amt / len(consumers)
        balances[payer] += amt
        for consumer in consumers:
          balances[consumer] -= share

    # Display Balances
    col1, col2 = st.columns(2)
    with col1:
      st.subheader("Net Balances")
      for person, bal in balances.items():
        if bal > 0:
          st.markdown(
              f"🟢 **{person}** gets back: `₹{round(bal, 2)}`"
          )
        elif bal < 0:
          st.markdown(
              f"🔴 **{person}** owes: `₹{round(abs(bal), 2)}`"
          )
        else:
          st.markdown(f"⚪ **{person}** is settled up.")

    with col2:
      st.subheader("💡 Smart Insight")
      total_spent = sum([exp["Amount"] for exp in st.session_state.expenses])
      st.metric(label="Total Trip Spending", value=f"₹{total_spent}")
      per_head = total_spent / len(friends) if friends else 0
      st.metric(label="Average Per Person", value=f"₹{round(per_head, 2)}")
else:
  st.warning("Please enter at least one friend's name to start splitting!")
