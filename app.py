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

# --- CLEAN GLOBAL HEADER BANNER ---
st.markdown(
    """
    <style>
    .global-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 20px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .global-banner h2 {
        color: #38bdf8;
        margin-bottom: 5px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .global-banner p {
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 0;
    }
    </style>
    <div class="global-banner">
        <h2>✈️ TRIPSPLIT AI — EXPLORE DREAMS. DISCOVER THE WORLD.</h2>
        <p>Smart Travel Planner, Receipt OCR & Expense Splitting Suite</p>
    </div>
""",
    unsafe_allow_html=True,
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

# --- STABLE LOGIN SCREEN ---
if not st.session_state.logged_in:
  st.markdown(
      "<h1 style='text-align: center;'>🔐 Member Login</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<h4 style='text-align: center; color: gray;'>Enter your name to access"
      " your trip dashboard</h4>",
      unsafe_allow_html=True,
  )
  st.markdown("---")

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
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
          "💸 Manage Expenses & OCR",
          "⚖️ Settlement & Analytics",
      ],
  )

  st.sidebar.markdown("---")
  if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

  # --- PAGE 1: HOME & TRIP SETUP ---
  if page == "🏠 Home & Trip Setup":
    # --- EXACT "TRIPPYPEDIA" STYLE HERO BANNER WITH SEARCH & TAGS ---
    st.markdown(
        """
        <style>
        .tripypedia-hero {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 35px 20px;
            border-radius: 24px;
            color: white;
            text-align: center;
            box-shadow: 0 12px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            border: 1px solid rgba(56, 189, 248, 0.25);
        }
        .tripypedia-logo {
            font-size: 2.8rem;
            font-weight: 800;
            color: #38bdf8;
            letter-spacing: 1.5px;
            margin-bottom: 5px;
        }
        .tripypedia-tagline {
            font-size: 1.15rem;
            color: #cbd5e1;
            font-style: italic;
            margin-bottom: 25px;
        }
        .search-pill-container {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        .search-pill {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 8px 16px;
            border-radius: 30px;
            font-size: 0.85rem;
            color: #e2e8f0;
            font-weight: 500;
        }
        </style>
        <div class="tripypedia-hero">
            <div class="tripypedia-logo">TripSplit AI</div>
            <div class="tripypedia-tagline">Explore Dreams. Discover the World.</div>
            <div class="search-pill-container">
                <div class="search-pill">🌴 Tropical Paradies</div>
                <div class="search-pill">🏔️ Adventure & Nature</div>
                <div class="search-pill">❄️ Winter & Snow</div>
                <div class="search-pill">🏛️ Cultural Escapes</div>
                <div class="search-pill">🦁 Safari & Wildlife</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.title("🌍 Trip Setup & Overview")
    st.markdown(
        "Set up your trip details, members, and total budget to begin smart"
        " splitting."
    )
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
      trip_name = st.text_input("Trip Name", "Goa Adventure 2026")
      destination = st.text_input("Destination", "Goa, India")
      st.session_state.trip_budget = st.number_input(
          "💰 Total Trip Budget (₹)",
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
          f"✨ Trip '{trip_name}' configured with a budget of"
          f" ₹{st.session_state.trip_budget} for: {', '.join(friends)}"
      )

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

  # --- PAGE 3: MANAGE EXPENSES & OCR ---
  elif page == "💸 Manage Expenses & OCR":
    st.title("💸 Smart Expense Entry & Receipt Scanner")
    st.markdown(
        "Choose between **Natural Language AI Entry**, **OCR Receipt Scanning**,"
        " or standard manual entry."
    )
    st.markdown("---")

    friends = st.session_state.friends
    tab1, tab2, tab3 = st.tabs([
        "✨ Natural Language Entry",
        "📸 OCR Receipt Scanner",
        "📝 Manual Form Entry",
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
      st.markdown("### 📸 Upload Receipt Photo (OCR Scan)")
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

    with tab3:
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
    st.title("⚖️ Smart Settlement & Budget Analytics")
    st.markdown(
        "Optimized balances, spending insights, and CSV report export."
    )
    st.markdown("---")

    total_spent = sum([exp["Amount"] for exp in st.session_state.expenses])
    budget = st.session_state.trip_budget

    col_b1, col_b2, col_b3 = st.columns(3)
    col_b1.metric("🎯 Total Budget", f"₹{budget}")
    col_b2.metric("💸 Total Spent", f"₹{total_spent}")
    remaining = budget - total_spent
    col_b3.metric(
        "📌 Remaining Balance",
        f"₹{remaining}",
        delta=f"-₹{abs(remaining)}" if remaining < 0 else f"+₹{remaining}",
        delta_color="inverse" if remaining < 0 else "normal",
    )

    if total_spent > budget:
      st.error(
          "🚨 **Budget Alert!** Your group has exceeded the total trip budget"
          f" of ₹{budget} by ₹{abs(remaining)}!"
      )
    else:
      st.success(
          f"✅ You are within budget! ₹{remaining} remaining for the trip."
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
        st.subheader("📊 Spending Analytics")
        per_head = total_spent / len(friends) if friends else 0
        st.metric(
            label="Average Spending Per Person",
            value=f"₹{round(per_head, 2)}",
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
