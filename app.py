import numpy as np
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="TripSplit AI - Pro Expense Manager",
    page_icon="✈️",
    layout="wide",
)

# --- SESSION STATE FOR LOGIN ---
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
  st.markdown(
      "<h1 style='text-align: center;'>✈️ Welcome to TripSplit AI</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<h4 style='text-align: center; color: gray;'>Your Smart Travel Expense"
      " & AI Planner Partner</h4>",
      unsafe_allow_html=True,
  )

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.markdown("### 🔐 Get Started")
    name_input = st.text_input("Enter your name to login:")
    if st.button("Login to Dashboard", use_container_width=True):
      if name_input.strip():
        st.session_state.logged_in = True
        st.session_state.username = name_input.strip()
        st.rerun()
      else:
        st.warning("Please enter a valid name!")
else:
  # --- SIDEBAR NAVIGATION ---
  st.sidebar.markdown(f"### 👋 Hello, {st.session_state.username}! 🌟")
  st.sidebar.markdown("---")

  page = st.sidebar.radio(
      "📍 Navigation",
      [
          "🏠 Home & Trip Setup",
          "🤖 AI Trip Planner",
          "💸 Manage Expenses",
          "⚖️ Settlement & Analytics",
      ],
  )

  st.sidebar.markdown("---")
  if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.expenses = []
    st.rerun()

  # Initialize session expenses if not exists
  if "expenses" not in st.session_state:
    st.session_state.expenses = []

  # --- PAGE 1: HOME & TRIP SETUP ---
  if page == "🏠 Home & Trip Setup":
    st.title("🌍 Trip Setup & Overview")
    st.markdown(
        "Welcome to your personal expense splitter hub. Set up your trip"
        " details below to get started!"
    )
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
      trip_name = st.text_input("Trip Name", "Goa Adventure 2026")
      destination = st.text_input("Destination", "Goa, India")

    with col2:
      friends_input = st.text_area(
          "Enter Friends' Names (comma separated)",
          "Rahul, Priya, Amit, Neha",
          help="Type names separated by commas",
      )

    friends = [f.strip() for f in friends_input.split(",") if f.strip()]
    st.session_state.friends = friends

    if friends:
      st.success(
          f"✨ Trip '{trip_name}' successfully configured for:"
          f" {', '.join(friends)}"
      )

      st.markdown("### 📌 Quick Stats")
      m1, m2, m3 = st.columns(3)
      m1.metric("Trip Name", trip_name)
      m2.metric("Total Members", len(friends))
      m3.metric("Total Expenses Logged", len(st.session_state.expenses))

  # --- PAGE 2: AI TRIP PLANNER ---
  elif page == "🤖 AI Trip Planner":
    st.title("🤖 AI Itinerary & Destination Planner")
    st.markdown(
        "Enter a destination and duration below, and let AI generate a"
        " customized travel plan for you!"
    )
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
      ai_destination = st.text_input(
          "🌍 Enter Destination", "Goa", placeholder="e.g., Manali, Kerala, Dubai"
      )
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
            f"✨ Here is your customized {trip_days}-Day Plan for"
            f" **{ai_destination}** ({travel_vibe} style):"
        )

        # Generating dynamic sample itinerary based on user input
        for day in range(1, trip_days + 1):
          with st.expander(f"📍 Day {day}: Exploring {ai_destination}", expanded=(day == 1)):
            if travel_vibe == "Party & Nightlife":
              st.markdown(f"""
              * **Morning:** Sleep in late, heavy beachside brunch at a popular cafe in {ai_destination}.
              * **Afternoon:** Water sports, chilling by the beach club pool, and relaxing photoshoots.
              * **Evening:** Sunset cruise / Beach shack hopping.
              * **Night:** Famous club / DJ night party experience!
              """)
            elif travel_vibe == "Adventure & Trekking":
              st.markdown(f"""
              * **Morning:** Early morning sunrise trek / Off-road trail biking around {ai_destination}.
              * **Afternoon:** Local sightseeing, valley views, and adventure sports (ziplining/rafting).
              * **Evening:** Bonfire setup, stargazing, and local street food tour.
              """)
            else:
              st.markdown(f"""
              * **Morning:** Visit top historical landmarks, scenic viewpoints, and local breakfast spots in {ai_destination}.
              * **Afternoon:** Guided cultural tour, local shopping markets, and cafe hopping.
              * **Evening:** Scenic sunset view point visit.
              * **Night:** Fine dining experience exploring authentic local cuisine.
              """)
        st.info("💡 Tip: You can copy these spots or add expenses directly once you book them!")
      else:
        st.error("Please enter a valid destination name!")

  # --- PAGE 3: MANAGE EXPENSES ---
  elif page == "💸 Manage Expenses":
    st.title("💸 Add & Track Expenses")
    st.markdown(
        "Record who paid what, and choose who will share the expense."
    )
    st.markdown("---")

    if "friends" not in st.session_state or not st.session_state.friends:
      st.warning(
          "⚠️ Please go to the 'Home & Trip Setup' page first and add your"
          " friends' names!"
      )
    else:
      friends = st.session_state.friends

      with st.form("expense_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
          expense_title = st.text_input(
              "Expense Title", placeholder="e.g., Hotel Booking"
          )
        with col2:
          amount = st.number_input(
              "Amount (₹)", min_value=0.0, value=1000.0, step=100.0
          )
        with col3:
          paid_by = st.selectbox("Paid By", friends)

        split_among = st.multiselect(
            "Split Among", friends, default=friends
        )

        submitted = st.form_submit_button(
            "➕ Add Expense", use_container_width=True
        )
        if submitted:
          if expense_title.strip() and amount > 0 and split_among:
            st.session_state.expenses.append({
                "Title": expense_title,
                "Amount": amount,
                "Paid By": paid_by,
                "Split With": split_among,
            })
            st.success(
                f"✅ Added '{expense_title}' worth ₹{amount} paid by {paid_by}!"
            )
          else:
            st.error(
                "Please fill in all details correctly and select at least one"
                " person to split with."
            )

      # Show Expense History Table
      if st.session_state.expenses:
        st.markdown("---")
        st.subheader("📋 Recorded Expenses History")
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df, use_container_width=True)

  # --- PAGE 4: SETTLEMENT & ANALYTICS ---
  elif page == "⚖️ Settlement & Analytics":
    st.title("⚖️ Smart Settlement & Analytics")
    st.markdown("See who owes whom and check overall expense breakdowns.")
    st.markdown("---")

    if "friends" not in st.session_state or not st.session_state.friends:
      st.warning("⚠️ Please set up your trip and friends on the Home page first!")
    elif not st.session_state.expenses:
      st.info("ℹ️ No expenses added yet. Go to 'Manage Expenses' to add some!")
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
        st.subheader("💰 Net Balances Breakdown")
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
        st.subheader("📊 Trip Analytics")
        total_spent = sum([exp["Amount"] for exp in st.session_state.expenses])
        st.metric(label="Total Trip Expenses", value=f"₹{total_spent}")
        per_head = total_spent / len(friends) if friends else 0
        st.metric(
            label="Average Spending Per Person", value=f"₹{round(per_head, 2)}"
        )
