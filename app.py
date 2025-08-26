import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from datetime import datetime

# ---------------- Page Config ----------------
st.set_page_config(page_title="MathCraft: Linear Equations Quest", layout="wide")

# ---------------- Session State ----------------
if "xp" not in st.session_state:
    st.session_state.xp = 0
    st.session_state.level = 1
    st.session_state.correct = 0
    st.session_state.answered = 0
    st.session_state.streak = 0
    st.session_state.best_streak = 0
    st.session_state.achievements = []

def award_xp(points, note=""):
    st.session_state.xp += points
    old_level = st.session_state.level
    st.session_state.level = min(10, st.session_state.xp // 100 + 1)
    if st.session_state.level > old_level:
        st.balloons()
        st.success(f"🎉 Level Up! You’re now Level {st.session_state.level}!")
    if note:
        st.info(f"+{points} XP • {note}")

# ---------------- Title & Story ----------------
st.title("📈 MathCraft: Linear Equations Quest")

st.header("🌟 Story Mode: The City of Lines")
st.write(
    "Welcome to Mathopolis, a city built on the power of linear equations! "
    "Architects, engineers, and scientists depend on you to guide the streets, "
    "design bridges, predict business growth, and even plan marathons. "
    "Master slopes, intercepts, parallels, and intersections to unlock the secrets of the city."
)

# ---------------- Tabs ----------------
tabs = st.tabs(["🏠 Home", "🧪 Labs", "📚 Quiz Arena", "🌍 Real World", "📊 Progress"])

# ---------------- HOME ----------------
with tabs[0]:
    st.subheader("📖 Your Journey")
    st.write(f"**XP:** {st.session_state.xp} | **Level:** {st.session_state.level}")
    st.write(f"**Accuracy:** {(st.session_state.correct/max(1,st.session_state.answered))*100:.1f}%")
    st.write(f"**Best Streak:** {st.session_state.best_streak}")

    st.markdown("### 🎯 Achievements")
    if "first_correct" in st.session_state.achievements:
        st.success("🥳 First Steps: Answered your first question correctly!")
    else:
        st.info("🔒 Answer your first question to unlock achievements!")

# ---------------- LABS ----------------
with tabs[1]:
    st.header("🧪 Line Laboratories")
    lab_tabs = st.tabs(["🔧 Transformer", "📐 Parallel & Perpendicular", "🔍 Intersection"])

    # Transformer
    with lab_tabs[0]:
        st.subheader("🔧 Line Transformer")
        m = st.slider("Slope (m)", -5.0, 5.0, 1.0)
        b = st.slider("Y-intercept (b)", -10.0, 10.0, 0.0)
        x = np.linspace(-10, 10, 200)
        y = m*x + b
        fig, ax = plt.subplots()
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.plot(x, y, "r", label=f"y = {m}x + {b}")
        ax.legend()
        st.pyplot(fig)

    # Parallel & Perpendicular
    with lab_tabs[1]:
        st.subheader("📐 Parallel & Perpendicular Lines")
        m1 = st.slider("Slope of Line 1", -5.0, 5.0, 1.0)
        b1 = st.slider("Intercept of Line 1", -10.0, 10.0, 0.0)
        m2 = st.slider("Slope of Line 2", -5.0, 5.0, -1.0)
        b2 = st.slider("Intercept of Line 2", -10.0, 10.0, 2.0)

        x = np.linspace(-10, 10, 200)
        fig, ax = plt.subplots()
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.plot(x, m1*x+b1, "r-", label=f"y={m1}x+{b1}")
        ax.plot(x, m2*x+b2, "b-", label=f"y={m2}x+{b2}")
        ax.legend()
        st.pyplot(fig)

        if abs(m1 - m2) < 1e-6:
            st.success("✅ Lines are parallel!")
        elif abs(m1*m2 + 1) < 1e-6:
            st.success("✅ Lines are perpendicular!")
        else:
            st.info("ℹ️ Lines intersect but are neither parallel nor perpendicular.")

    # Intersection
    with lab_tabs[2]:
        st.subheader("🔍 Intersection Finder")
        if abs(m1 - m2) < 1e-6:
            st.warning("⚠️ No intersection (parallel lines).")
        else:
            xi = (b2 - b1)/(m1 - m2)
            yi = m1*xi + b1
            st.success(f"Intersection at ({xi:.2f}, {yi:.2f})")

# ---------------- QUIZ ----------------
with tabs[2]:
    st.header("📚 Quiz Arena")

    q_types = [
        ("What is the slope of y = 3x + 2?", "3"),
        ("What is the y-intercept of y = -2x + 5?", "5"),
        ("Which slope makes a line parallel to y = 4x + 1?", "4"),
        ("If two lines are perpendicular, what is true about their slopes?", "Their product is -1"),
    ]
    q, a = random.choice(q_types)
    st.write(f"**Question:** {q}")
    user = st.text_input("Your answer:")
    if st.button("Check Answer"):
        st.session_state.answered += 1
        if user.strip() == a:
            st.success("✅ Correct!")
            award_xp(10, "Correct quiz answer")
            st.session_state.correct += 1
            st.session_state.streak += 1
            st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
            if st.session_state.correct == 1:
                st.session_state.achievements.append("first_correct")
        else:
            st.error(f"❌ Incorrect. Correct answer: {a}")
            st.session_state.streak = 0

# ---------------- REAL WORLD ----------------
with tabs[3]:
    st.header("🌍 Real-World Labs")
    rw_tabs = st.tabs(["🏗️ City Planning", "💰 Business", "🌡️ Science", "🏃 Sports"])

    # City
    with rw_tabs[0]:
        st.subheader("🏗️ Street Grid Design")
        main_slope = st.slider("Main Street slope", -2.0, 2.0, 1.0)
        cross_slope = -1/main_slope if abs(main_slope) > 0.01 else 0
        st.info(f"Cross streets will have slope {cross_slope:.2f} to stay perpendicular.")

    # Business
    with rw_tabs[1]:
        st.subheader("💰 Business Growth")
        growth = st.slider("Monthly Growth ($)", 1000, 10000, 3000, 500)
        start = st.slider("Starting Revenue ($)", 5000, 50000, 20000, 1000)
        months = np.arange(0, 13)
        revenue = start + growth*months
        fig, ax = plt.subplots()
        ax.plot(months, revenue, "g-o")
        ax.set_title(f"Revenue = {growth}x + {start}")
        st.pyplot(fig)

    # Science
    with rw_tabs[2]:
        st.subheader("🌡️ Temperature Conversion")
        c = st.slider("Temp (°C)", -40, 100, 20)
        f = 9/5*c + 32
        st.write(f"{c}°C = {f:.1f}°F")

    # Sports
    with rw_tabs[3]:
        st.subheader("🏃 Marathon Pace")
        pace = st.slider("Pace (min/km)", 3.0, 8.0, 5.0, 0.1)
        marathon_time = pace*42.195
        hours = int(marathon_time//60)
        mins = int(marathon_time%60)
        st.write(f"Marathon time ≈ {hours}h {mins}m")

# ---------------- PROGRESS ----------------
with tabs[4]:
    st.header("📊 Progress Tracker")
    st.metric("XP", st.session_state.xp)
    st.metric("Level", st.session_state.level)
    st.metric("Accuracy", f"{(st.session_state.correct/max(1,st.session_state.answered))*100:.1f}%")
    st.metric("Best Streak", st.session_state.best_streak)

# ---------------- Footer ----------------
st.markdown("---")
st.caption("Built by Xavier Honablue M.Ed for CognitiveCloud.ai")
