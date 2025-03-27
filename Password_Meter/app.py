import re
import secrets
import string
import streamlit as st

# Add custom CSS for a gradient background
page_bg_gradient = '''
<style>
.stApp {
    background: linear-gradient(to right, #1f4037, #99f2c8);  /* Dark green to light green gradient */
    background-size: cover;
    background-position: center;
    color: white;
}

h1, h2, h3, h4, h5 {
    color: #f5f5f5; /* Light grey for headings */
}

p, div, label, input, .stTextInput {
    color: #ffffff !important; /* White for general text */
}

.stAlert {
    background-color: rgba(255, 255, 255, 0.1); /* Transparent white background for alerts */
    border-color: white;
}

.stButton>button {
    color: white !important;
    background-color: rgba(255, 255, 255, 0.3) !important; /* Semi-transparent button */
    border: 2px solid white;
}

.stTextInput input {
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
}

/* Footer styling */
footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    text-align: center;
    padding: 10px;
}

footer p {
    font-size: 14px;
    color: white;
}
</style>
'''

# Inject the custom CSS for the gradient background
st.markdown(page_bg_gradient, unsafe_allow_html=True)

# List of common weak passwords (blacklist)
COMMON_PASSWORDS = ["password", "123456", "123456789", "qwerty", "abc123", "password123", "letmein"]

# -------------------------
# Helper Function to Check Password Strength
# -------------------------
def check_password_strength(password):
    score = 0
    feedback = []

    # 1. Blacklist Check
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("🚫 This is a common password. Please choose a more unique one.")
        return 0, "❌ Very Weak Password", feedback

    # 2. Length Check (minimum 8 characters)
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("🔑 Password should be at least 8 characters long.")

    # Bonus: Extra point for passwords with 12 or more characters
    if len(password) >= 12:
        score += 1

    # 3. Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🔡 Include both uppercase and lowercase letters.")

    # 4. Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🔢 Add at least one number (0-9).")

    # 5. Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❗ Include at least one special character (!@#$%^&*).")

    # 6. Check for consecutive repeated characters (three or more)
    if re.search(r"(.)\1\1", password):
        feedback.append("🚫 Avoid using the same character three or more times in a row.")
        score = max(score - 1, 0)  # Optionally subtract a point

    # Determine strength rating based on the score
    if score >= 6:
        strength = "✅ Strong Password!"
    elif score >= 4:
        strength = "⚠️ Moderate Password - Consider adding more security features."
    else:
        strength = "❌ Weak Password - Improve it using the suggestions below."

    return score, strength, feedback

# -------------------------
# Helper Function to Generate Strong Password
# -------------------------
def generate_strong_password(length=12):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    # Keep generating until a strong password is found
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        score, _, _ = check_password_strength(password)
        if score >= 6:  # ensuring it's strong
            return password

# -------------------------
# Streamlit App with Gradient Background and Emojis
# -------------------------

# Title and description with emojis
st.title("🔐 Professional Password Strength Meter")
st.write("🔍 **Check how strong your password is, and get suggestions to improve it!**")

# Input area for password check
password_input = st.text_input("🔑 Enter your password:", type="password")
if st.button("🔎 Check Password Strength"):
    if password_input:
        score, strength, suggestions = check_password_strength(password_input)
        st.subheader(f"**💪 Strength Score: {score}/6**")
        st.subheader(strength)
        if suggestions:
            st.write("📋 **Suggestions to improve your password:**")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
    else:
        st.warning("Please enter a password to evaluate!")

st.write("---")
st.write("💡 **Need a strong password? Click the button below to generate one!**")

# Ensure the session state is initialized for the generated password
if "generated_password" not in st.session_state:
    st.session_state.generated_password = ""

# Password Generator Button
if st.button("⚙️ Generate Strong Password"):
    st.session_state.generated_password = generate_strong_password()
    st.success(f"🎉 Your strong password is: `{st.session_state.generated_password}`")

# Display the generated password even after re-render
if st.session_state.generated_password:
    st.write(f"Generated Password: `{st.session_state.generated_password}`")

    
# -------------------------
# Footer Section
# -------------------------

# Footer HTML using custom CSS and emojis
footer = """
<footer>
    <p>👨‍💻 Developed by <strong>[Syed Muhammad]</strong> | © 2025 All rights reserved.</p>
</footer>
"""

# Add the footer to the app
st.markdown(footer, unsafe_allow_html=True)