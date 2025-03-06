import streamlit as st
import random

# Title and Header
st.title("🚀 Growth Mindset Challenge")
st.header("Unlock Your Potential with a Growth Mindset")

# Introduction section with image
st.image("images\\Growth Mindset Vs Fixed Mindset.png", caption="Growth Mindset", use_column_width=True)


st.write("""
The **growth mindset** is the belief that your abilities and intelligence can be developed through hard work, perseverance, and learning from mistakes.
This app will guide you in adopting a growth mindset to unlock your full potential.
""")


# Sidebar for quick navigation
st.sidebar.title("Navigation")
st.sidebar.subheader("Jump to Section:")
st.sidebar.markdown("[What is Growth Mindset?](#what-is-growth-mindset)")
st.sidebar.markdown("[How to Practice?](#how-to-practice-growth-mindset)")
st.sidebar.markdown("[Your Goals](#your-learning-goals)")
st.sidebar.markdown("[Motivational Quotes](#motivational-quote-of-the-day)")


# What is Growth Mindset Section
st.subheader("💡 What is a Growth Mindset?")
st.write("""
A growth mindset is the belief that abilities can be developed through dedication and hard work. This contrasts with a fixed mindset, which assumes abilities are static and unchangeable.
Here’s why adopting a growth mindset can make all the difference in both personal and academic life:
""")

# Columns for a better layout
col1, col2 = st.columns(2)
with col1:
    st.write("""
    - **Embrace Challenges:** Obstacles are opportunities to learn.
    - **Learn from Mistakes:** Every mistake is a lesson for improvement.
    """)
with col2:
    st.write("""
    - **Persist Through Difficulty:** Stay determined and keep moving forward.
    - **Celebrate Effort:** Focus on your effort, not just the results.
    - **Stay Open:** Stay curious and flexible in your approach.
    """)

st.markdown("---")

# How to Practice Growth Mindset Section
st.subheader("🧠 How to Practice Growth Mindset?")
st.write("Adopt the following habits to develop a growth mindset:")

# Sliders for self-assessment
challenge_slider = st.slider("How much do you embrace challenges?", 0, 100, 50)
mistake_slider = st.slider("How well do you learn from your mistakes?", 0, 100, 50)
effort_slider = st.slider("How often do you recognize your efforts?", 0, 100, 50)

if st.button("Evaluate Yourself"):
    st.write(f"### You embrace challenges {challenge_slider}% of the time!")
    st.write(f"You learn from mistakes {mistake_slider}% of the time!")
    st.write(f"You recognize your efforts {effort_slider}% of the time!")

st.markdown("---")

# User Goals Section
st.subheader("🎯 Your Learning Goals")

st.write("""
Setting learning goals helps you stay on track in developing your growth mindset.
""")

# Goal Input
user_goal = st.text_input("What is one learning goal you want to achieve?")
if user_goal:
    st.success(f"Great! Keep working on this goal: **{user_goal}**")

# Checkboxes for self-reflection
st.write("### Reflect on your learning:")
challenge_checkbox = st.checkbox("I embrace challenges")
mistake_checkbox = st.checkbox("I learn from mistakes")
effort_checkbox = st.checkbox("I recognize and celebrate my efforts")

if challenge_checkbox and mistake_checkbox and effort_checkbox:
    st.balloons()
    st.write("Fantastic! You're embracing a full growth mindset!")

st.markdown("---")

# Motivational Quote Section
st.subheader("💬 Motivational Quote of the Day")

# Add random motivational quotes
quotes = [
    "Believe you can, and you're halfway there. - Theodore Roosevelt",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "Hardships often prepare ordinary people for an extraordinary destiny. - C.S. Lewis",
    "It’s not that I’m so smart, it’s just that I stay with problems longer. - Albert Einstein",
    "Strive for progress, not perfection.",
]

daily_quote = random.choice(quotes)
st.info(f"**{daily_quote}**")

# Closing message
st.write("**Remember:** Adopting a growth mindset is a journey, not a destination. Stay committed to continuous improvement!")

st.markdown("---")

# Footer
st.markdown("#### Built by 😊 [Syeda Hifza 🔥]")
st.markdown("#### [Connect with me on LinkedIn](https://www.linkedin.com/in/syeda-hifza-1a0b4b1b3/)")
