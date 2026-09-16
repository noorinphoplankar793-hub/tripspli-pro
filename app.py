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
if "trip_budget" not in st.session_state:
  st.session_state.trip_budget = 15000.0
if "base_currency" not in st.session_state:
  st.session_state.base_currency = "INR (₹)"

# --- STABLE LOGIN SCREEN ---
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
          "🤖 AI Itinerary Planner",
          "💸 Smart Expenses & OCR",
          "⚖️ Settlement & Analytics",
      ],
  )

  st.sidebar.markdown("---")
  if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

  # --- PAGE 1: HOME & TRIP SETUP ---
  if page == "🏠 Home & Trip Setup":
    st.title("🌍 Trip Setup & Multi-Currency Overview")
    st.markdown(
        "Set up your trip details, members, base currency, and total budget."
    )
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
      trip_name = st.text_input("Trip Name", "Goa Adventure 2026")
      destination = st.text_input("Destination", "Goa, India")
      st.session_state.base_currency = st.selectbox(
          "💱 Base Currency", ["INR (₹)", "USD ($)", "EUR (€)", "JPY (¥)"]
      )
      st.session_state.trip_budget = st.number_input(
          f"💰 Total Trip Budget ({st.session_state.base_currency.split()[1]})",
          min_value=1000.0,
          value=st.session_state.trip_budget,
          step=1000.0,
      )

    with col2:
      friends_input = st.text_area(
          "Enter Friends' Names (comma separated)",
          ", ".join(st.session_state.friends),
      )

    friends = [f.strip() for f in friends_input.split(",") if f.strip()]
    st.session_state.friends = friends

    if friends:
      st.success(
          f"✨ Trip '{trip_name}' configured for: {', '.join(friends)} with"
          f" Currency {st.session_state.base_currency}"
      )

  # --- PAGE 2: AI ITINERARY PLANNER (WITH INTERESTS) ---
  elif page == "🤖 AI Itinerary Planner":
    st.title("🤖 AI Itinerary Recommendation Engine")
    st.markdown(
        "Generate custom day-by-day itineraries based on destination and group"
        " interests."
    )
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
      ai_destination = st.text_input("🌍 Enter Destination", "Goa")
    with col2:
      trip_days = st.number_input(
          "📅 Number of Days", min_value=1, max_value=15, value=3
      )

    group_interests = st.multiselect(
        "🎯 Select Group Interests",
        [
            "Adventure & Trekking",
            "Food & Culinary",
            "Culture & Heritage",
            "Relaxation & Beaches",
            "Nightlife & Parties",
        ],
        default=["Food & Culinary", "Relaxation & Beaches"],
    )

    if st.button("🚀 Generate AI Itinerary", use_container_width=True):
      if ai_destination.strip():
        st.markdown("---")
        st.success(
            f"✨ Generated {trip_days}-Day Custom Plan for **{ai_destination}**"
            f" tailored for: {', '.join(group_interests)}"
        )
        for day in range(1, trip_days + 1):
          with st.expander(
              f"📍 Day {day}: Exploring {ai_destination}", expanded=(day == 1)
          ):
            st.markdown(f"""
                        * **Morning:** Scenic spots matching **{group_interests[0] if group_interests else 'Sightseeing'}**.
                        * **Afternoon:** Local popular food spots and group activities.
                        * **Evening:** Relaxed sunset view and group dinner.
                        """)
      else:
        st.error("Please enter a valid destination!")

  # --- PAGE 3: SMART EXPENSES & OCR ---
  elif page == "💸 Smart Expenses & OCR":
    st.title("💸 Smart Expense Entry & Receipt Scanner")
    st.markdown(
        "Use **AI Natural Language Entry**, **OCR Receipt Scanning**, or"
        " standard manual entry."
    )
    st.markdown("---")

    friends = st.session_state.friends
    tab1, tab2, tab3 = st.tabs([
        "✨ Natural Language Entry",
        "📸 OCR Receipt Scanner",
        "📝 Manual Entry",
    ])

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
              f"✅ Successfully Parsed! Added **{title}** worth **₹{amount}**"
              f" paid by **{found_payer}**."
          )
        else:
          st.error("Please type an expense sentence first!")

    with tab3:
      with st.form("manual_expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
          expense_title = st.text_input("Expense Title", "Dinner")
        with col2:
          amount = st.number_input("Amount", min_value=0.0, value=500.0)
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
          st.success(f"Added '{expense_title}' successfully!")

    with tab2:
      st.markdown(
          "### 📸 Upload Receipt Photo (OCR + LLM Extraction Simulation)"
      )
      uploaded_file = st.file_uploader(
          "Choose a receipt image (PNG, JPG)", type=["png", "jpg", "jpeg"]
      )
      if uploaded_file is not None:
        st.image(
            uploaded_file,
            caption="Uploaded Receipt Preview",
            use_column_width=True,
        )
        if st.button("🔍 Extract Data using OCR & Add"):
          # Simulated OCR Extraction result
          extracted_amount = 1250.0
          extracted_title = "Restaurant Bill (OCR)"
          st.success(
              f"✨ OCR Extracted Successfully! Merchant: Cafe | Amount:"
              f" ₹{extracted_amount}"
          )
          st.session_state.expenses.append({
              "Title": extracted_title,
              "Amount": extracted_amount,
              "Paid By": friends[0],
              "Split With": friends,
          })

    if st.session_state.expenses:
      st.markdown("---")
      st.subheader("📋 Recorded Expenses History")
      df = pd.DataFrame(st.session_state.expenses)
      st.dataframe(df, use_container_width=True)

  # --- PAGE 4: SETTLEMENT & ANALYTICS ---
  elif page == "⚖️ Settlement & Analytics":
    st.title("⚖️ Smart Settlement & Budget Analytics")
    st.markdown(
        "Optimized payment paths, budget forecasting, and CSV report export."
    )
    st.markdown("---")

    total_spent = sum([exp["Amount"] for exp in st.session_state.expenses])
    budget = st.session_state.trip_budget
    curr_symbol = st.session_state.base_currency.split()[1]

    col_b1, col_b2, col_b3 = st.columns(3)
    col_b1.metric("🎯 Total Budget", f"{curr_symbol}{budget}")
    col_b2.metric("💸 Total Spent", f"{curr_symbol}{total_spent}")
    remaining = budget - total_spent
    col_b3.metric(
        "📌 Remaining Balance",
        f"{curr_symbol}{remaining}",
        delta=(
            f"-{curr_symbol}{abs(remaining)}"
            if remaining < 0
            else f"+{curr_symbol}{remaining}"
        ),
        delta_color="inverse" if remaining < 0 else "normal",
    )

    if total_spent > budget:
      st.error(
          f"🚨 **Budget Alert!** Exceeded budget of {curr_symbol}{budget} by"
          f" {curr_symbol}{abs(remaining)}!"
      )
    else:
      st.success(
          f"✅ Within budget! {curr_symbol}{remaining} remaining for the trip."
      )

    st.markdown("---")

    if not st.session_state.expenses:
      st.info("ℹ️ No expenses added yet. Add some expenses to see balances!")
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
        st.subheader("💰 Simplified Debt Settlement")
        for person, bal in balances.items():
          if bal > 0:
            st.markdown(
                f"🟢 **{person}** gets back: `{curr_symbol}{round(bal, 2)}`"
            )
          elif bal < 0:
            st.markdown(
                f"🔴 **{person}** owes: `{curr_symbol}{round(abs(bal), 2)}`"
            )
          else:
            st.markdown(f"⚪ **{person}** is fully settled up.")

      with col2:
        st.subheader("📊 Spending Analytics")
        per_head = total_spent / len(friends) if friends else 0
        st.metric(
            label="Average Spending Per Person",
            value=f"{curr_symbol}{round(per_head, 2)}",
        )

      # --- CSV EXPORT BUTTON ---
      st.markdown("---")
      st.subheader("📥 Export Trip Summary")
      df_export = pd.DataFrame(st.session_state.expenses)
      csv_data = df_export.to_csv(index=False).encode("utf-8")

      st.download_button(
          label="📥 Download Expense Report as CSV",
          data=csv_data,
          file_name="tripsplit_report.csv",
          mime="text/csv",
          use_container_width=True,
      )
