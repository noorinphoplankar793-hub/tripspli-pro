# --- CREATIVE TRAVEL HERO BANNER (CSS + HTML) ---
st.markdown(
    """
    <style>
    .hero-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 35px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        font-weight: 400;
        letter-spacing: 1px;
    }
    .badge-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 20px;
        flex-wrap: wrap;
    }
    .feature-badge {
        background: rgba(255, 255, 255, 0.08);
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 0.85rem;
        color: #e2e8f0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>

    <div class="hero-container">
        <div class="hero-title">✈️ TRIPSPLIT AI</div>
        <div class="hero-subtitle">THE WORLD IS WAITING — EXPLORE, SPLIT & SETTLE TOGETHER</div>
        <div class="badge-container">
            <div class="feature-badge">🗺️ AI Itinerary Planner</div>
            <div class="feature-badge">💸 Smart Expense Splitting</div>
            <div class="feature-badge">📸 OCR Receipt Scanner</div>
            <div class="feature-badge">📊 Live Budget Tracking</div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)
