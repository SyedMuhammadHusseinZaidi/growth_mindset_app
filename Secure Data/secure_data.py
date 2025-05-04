import streamlit as st
import hashlib
import json
import datetime
from cryptography.fernet import Fernet, InvalidToken
import time

# Set page configurationexit

st.set_page_config(page_title="Secure Data Encryption System", page_icon="🔒", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f7f6;
        color: #333;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        padding: 10px;
        border: 2px solid #ddd;
    }
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        padding: 10px;
        border: 2px solid #ddd;
    }
    .stAlert {
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 20px;
    }
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 20px;
    }
    .stText {
        line-height: 1.6;
    }
    .sidebar .sidebar-content {
        background-color: #e9ecef;
        padding: 10px;
        border-radius: 8px;
    }
    .sidebar .sidebar-header {
        text-align: center;
        font-size: 24px;
        color: #007bff;
    }
    </style>
""", unsafe_allow_html=True)

# Load data function
def load_data():
    try:
        with open("database.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}, "data": {}}

# Save data function
def save_data(data):
    with open("database.json", "w") as f:
        json.dump(data, f)

# Ensure admin user exists
def ensure_admin_user(data):
    if "admin" not in data["users"]:
        admin_password = "admin123"  # Default admin password
        data["users"]["admin"] = {"passkey": hash_passkey(admin_password)}
        save_data(data)
    return data

# Function to hash passkey using SHA-256
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Encrypt data function
def encrypt_data(text, passkey):
    return cipher.encrypt(text.encode()).decode()

# Decrypt data function with expiration and view limit checks
def decrypt_data(encrypted_text, passkey):
    try:
        username = st.session_state.current_user
        if not username or username not in stored_data["data"]:
            return None

        user_records = stored_data["data"].get(username, {})
        record = user_records.get(encrypted_text)

        if not record:
            st.session_state.failed_attempts += 1
            return None

        # Check expiration
        timestamp = datetime.datetime.fromisoformat(record["timestamp"])
        minutes_passed = (datetime.datetime.now() - timestamp).total_seconds() / 60
        if minutes_passed > record["expire_after_minutes"]:
            st.error("⏰ This record has expired.")
            return None

        # Check view limit
        if record["views_left"] <= 0:
            st.error("🚫 This record has reached its maximum view limit.")
            return None

        # Validate passkey
        if hash_passkey(passkey) == record["passkey"]:
            record["views_left"] -= 1
            save_data(stored_data)
            try:
                return cipher.decrypt(encrypted_text.encode()).decode()
            except InvalidToken:
                st.error("❌ The provided passkey or encrypted data is invalid.")
                return None
        else:
            st.session_state.failed_attempts += 1
            return None
    except Exception as e:
        st.error(f"❌ An error occurred during decryption: {str(e)}")
        return None

# Set up session state
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = 0
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Load data and ensure admin exists
stored_data = ensure_admin_user(load_data())

# Generate encryption key
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# Streamlit UI
st.title("🔒 Secure Data Encryption System")

# Sidebar navigation
menu = ["Home", "Store Data", "Retrieve Data", "Login", "Register"]
if st.session_state.current_user == "admin":
    menu.append("Admin Dashboard")
choice = st.sidebar.selectbox("Navigation", menu)

# Home Page
if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")

# Register Page
elif choice == "Register":
    st.subheader("🔐 Register New User")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if username and password:
            if password == confirm_password:
                if username not in stored_data["users"]:
                    stored_data["users"][username] = {"passkey": hash_passkey(password)}
                    save_data(stored_data)
                    st.success(f"✅ User '{username}' registered successfully!")
                else:
                    st.error("❌ Username already exists.")
            else:
                st.error("❌ Passwords do not match.")
        else:
            st.error("⚠️ Please fill in both username and password.")

# Login Page
elif choice == "Login":
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in stored_data["users"] and hash_passkey(password) == stored_data["users"][username]["passkey"]:
            st.session_state.current_user = username
            st.success(f"✅ Logged in as {username}")
            st.rerun()
        else:
            st.error("❌ Invalid credentials.")

# Store Data Page
elif choice == "Store Data":
    if st.session_state.current_user:
        st.subheader("📦 Store Encrypted Data")
        user_data = st.text_area("Enter data to encrypt:")
        passkey = st.text_input("Set a passkey:", type="password")
        expire_minutes = st.number_input("Expire After (minutes)", min_value=1, max_value=1440, value=60)
        max_views = st.number_input("Max Views Allowed", min_value=1, max_value=100, value=5)

        if st.button("Encrypt & Store"):
            if user_data and passkey:
                encrypted = encrypt_data(user_data, passkey)
                record = {
                    "encrypted_text": encrypted,
                    "passkey": hash_passkey(passkey),
                    "timestamp": datetime.datetime.now().isoformat(),
                    "expire_after_minutes": expire_minutes,
                    "views_left": max_views
                }
                if st.session_state.current_user not in stored_data["data"]:
                    stored_data["data"][st.session_state.current_user] = {}
                stored_data["data"][st.session_state.current_user][encrypted] = record
                save_data(stored_data)
                st.success("✅ Data encrypted and stored!")
            else:
                st.error("⚠️ Fill in all fields.")
    else:
        st.warning("🔐 Please log in to store data.")

# Retrieve Data Page
elif choice == "Retrieve Data":
    if st.session_state.current_user:
        st.subheader("🔍 Retrieve Your Data")
        encrypted_input = st.text_area("Paste your encrypted data:")
        passkey_input = st.text_input("Enter your passkey:", type="password")

        if st.button("Decrypt"):
            if encrypted_input and passkey_input:
                decrypted = decrypt_data(encrypted_input, passkey_input)
                if decrypted:
                    st.success("✅ Decryption successful!")
                    st.code(decrypted, language="text")
                else:
                    st.error("❌ Incorrect passkey or expired/invalid record.")
            else:
                st.error("⚠️ Please fill both fields.")
    else:
        st.warning("🔐 Please log in to retrieve your data.")

# Admin Dashboard
elif choice == "Admin Dashboard":
    if st.session_state.current_user == "admin":
        st.subheader("🛠️ Admin Dashboard")
        st.markdown("### 👥 Registered Users")
        for user in stored_data["users"]:
            if user != "admin":
                st.write(f"🔹 {user}")
                if st.button(f"Delete User '{user}'", key=f"del_user_{user}"):
                    del stored_data["users"][user]
                    stored_data["data"].pop(user, None)
                    save_data(stored_data)
                    st.success(f"🗑️ User '{user}' deleted")
                    st.rerun()

        st.markdown("### 📦 Encrypted Data")
        for user, records in stored_data.get("data", {}).items():
            st.write(f"#### 🔐 Data for {user}")
            for enc, value in records.items():
                st.code(enc, language="text")
                if st.button(f"Delete Entry for {user}", key=f"{user}_{enc[:5]}"):
                    del stored_data["data"][user][enc]
                    save_data(stored_data)
                    st.success("🗑️ Record deleted")
                    st.rerun()