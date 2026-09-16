import re
import numpy as np
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="TripSplit AI - Pro Expense Manager",
    page_icon="✈️",
    layout="wide",
)

# --- SESSION STATE INITIALIZATION ---
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""
if "expenses" not in st.session_state:
  st.session_state.expenses = []
if "friends" not in st.session_state:
  st.session_state.friends = ["Rahul", "Priya", "Amit", "Neha"]

# --- STABLE LOGIN SCREEN (No complex columns blocking clicks) ---
if not st.session_state.logged_in:
  st.markdown(
      "<h1 style='text-align: center;'>✈️ TripSplit AI</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<h4 style='text-align: center; color: gray;'>Smart Travel Expense & AI"
      " Itinerary Partner</h4>",
      unsafe_allow_html=True,
  )
  st.markdown("---")

  st.markdown("### 🔐 Enter Your Name to Access Dashboard")
  name_input = st.text_input("Your Name:", placeholder="e.g., Ayan")

  if st.button("🚀 Login to Dashboard", use_container_width=True):
    if name_input.strip():
      st.session_state.logged_in = True
      st.session_state.username = name_input.strip()
      st.rerun()
    else:
      st.error("⚠️ Please enter a valid name before logging in!")

else:
  # --- SIDEBAR NAVIGATION ---
  st.sidebar.markdown(f"### 👋 Hello, {st.session_state.username}! 🌟")
  st.sidebar.markdown("---")

  page = st.sidebar.radio(
      "📍 Navigation",
      [
          "🏠 Home & Trip Setup",
          "🤖 AI Trip Planner",
          "💸 Manage Expenses (Smart Entry)",
          "⚖️ Settlement & Analytics",
      ],
  )

  st.sidebar.markdown("---")
  if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

  # --- PAGE 1: HOME & TRIP SETUP ---
  if page == "🏠 Home & Trip Setup":
    st.title("🌍 Trip Setup & Overview")
    st.markdown(
        "Set up your trip details and add members to begin smart splitting."
    )
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
      trip_name = st.text_input("Trip Name", "Goa Adventure 2026")
      destination = st.text_input("Destination", "Goa, India")

    with col2:
      friends_input = st.text_area(
          "Enter Friends' Names (comma separated)",
          ", ".join(st.session_state.friends),
      )

    friends = [f.strip() for f in friends_input.split(",") if f.strip()]
    st.session_state.friends = friends

    if friends:
      st.success(f"✨ Trip '{trip_name}' configured for: {', '.join(friends)}")

  # --- PAGE 2: AI TRIP PLANNER ---
  elif page == "🤖 AI Trip Planner":
    st.title("🤖 AI Itinerary & Destination Planner")
    st.markdown(
        "Generate custom day-by-day itineraries instantly using AI logic."
    )
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
      ai_destination = st.text_input("🌍 Enter Destination", "Goa")
    with col2:
      trip_days = st.number_input(
          "📅 Number of Days", min_value=1, max_value=15, value=3
      )

    travel_vibe = st.selectbox(
        "✨ Select Trip Vibe",
        [
            "Relaxed & Beach/Nature",
            "Party & Nightlife",
            "Adventure & Trekking",
            "Cultural & Food Exploration",
        ],
    )

    if st.button("🚀 Generate AI Plan", use_container_width=True):
      if ai_destination.strip():
        st.markdown("---")
        st.success(
            f"✨ Generated {trip_days}-Day Plan for **{ai_destination}**:"
        )
        for day in range(1, trip_days + 1):
          with st.expander(
              f"📍 Day {day}: Exploring {ai_destination}", expanded=(day == 1)
          ):
            st.markdown(f"""
                        * **Morning:** Scenic viewpoints, cafe breakfast in {ai_destination}.
                        * **Afternoon:** Sightseeing, local attractions, and group activities.
                        * **Evening:** Sunset exploration and group dinner.
                        """)
      else:
        st.error("Please enter a valid destination!")

  # --- PAGE 3: MANAGE EXPENSES (WITH NATURAL LANGUAGE ENTRY) ---
  elif page == "💸 Manage Expenses (Smart Entry)":
    st.title("💸 Smart Expense Entry")
    st.markdown(
        "Choose between **Natural Language AI Entry** (typing a sentence) or"
        " standard manual entry."
    )
    st.markdown("---")

    friends = st.session_state.friends
    tab1, tab2 = st.tabs(["✨ Natural Language Entry", "📝 Manual Form Entry"])

    with tab1:
      st.info(
          "💡 **Tip:** Type something like: *'Rahul paid 1200 for dinner with"
          f" {', '.join(friends)}'* "
      )
      nlp_input = st.text_input(
          "Type your expense in plain English:",
          placeholder=f"e.g., I paid 2000 for cab with {friends[0]}",
      )

      if st.button("✨ Parse & Add Expense"):
        if nlp_input.strip():
          text = nlp_input.strip()
          numbers = re.findall(r"\d+", text)
          amount = float(numbers[0]) if numbers else 0.0

          found_payer = friends[0]
          for f in friends:
            if f.lower() in text.lower():
              found_payer = f
              break

          title = "General Expense"
          for keyword in [
              "dinner",
              "lunch",
              "breakfast",
              "cab",
              "hotel",
              "beer",
              "ticket",
              "coffee",
          ]:
            if keyword in text.lower():
              title = keyword.capitalize()
              break

          st.session_state.expenses.append({
              "Title": title,
              "Amount": amount,
              "Paid By": found_payer,
              "Split With": friends,
          })
          st.success(
              "✅ Successfully Parsed! Added "
              + title
              + " worth ₹"
              + str(amount)
              + " paid by "
              + found_payer
              + " split among all."
          )
        else:
          st.error("Please type an expense sentence first!")

    with tab2:
      with st.form("manual_expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
          expense_title = st.text_input("Expense Title", "Dinner")
        with col2:
          amount = st.number_input("Amount (₹)", min_value=0.0, value=500.0)
        with col3:
          paid_by = st.selectbox("Paid By", friends)

        split_among = st.multiselect(
            "Split Among", friends, default=friends
        )

        submitted = st.form_submit_button("➕ Add Expense Manually")
        if submitted:
          st.session_state.expenses.append({
              "Title": expense_title,
              "Amount": amount,
              "Paid By": paid_by,
              "Split With": split_among,
          })
          st.success(f"Added '{expense_title}' of ₹{amount} successfully!")

    if st.session_state.expenses:
      st.markdown("---")
      st.subheader("📋 Recorded Expenses History")
      df = pd.DataFrame(st.session_state.expenses)
      st.dataframe(df, use_container_width=True)

  # --- PAGE 4: SETTLEMENT & ANALYTICS ---
  elif page == "⚖️ Settlement & Analytics":
    st.title("⚖️ Smart Settlement & Analytics")
    st.markdown("Optimized balances and insights for your trip.")
    st.markdown("---")

    if not st.session_state.expenses:
      st.info("ℹ️ No expenses added yet. Add some expenses first!")
    else:
      friends = st.session_state.friends
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

      col1, col2 = st.columns(2)
      with col1:
        st.subheader("💰 Net Balances")
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
            st.markdown(f"⚪ **{person}** is fully settled up.")

      with col2:
        st.subheader("📊 Analytics")
        total_spent = sum([exp["Amount"] for exp in st.session_state.expenses])
        st.metric(label="Total Trip Spending", value=f"₹{total_spent}")
        per_head = total_spent / len(friends) if friends else 0
        st.metric(label="Average Per Person", value=f"₹{round(per_head, 2)}")
