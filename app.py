import streamlit as st
from database.db import init_db
from ui.auth import render_auth_page
from ui.dashboard import render_dashboard
from sensors.esp32_handler import start_receiver_thread

# Configure Streamlit Page
st.set_page_config(
    page_title="Rider Safety System",
    page_icon="🛡️",
    layout="wide"
)

# Initialize SQLite database schema
init_db()

# Start Flask ESP32 Receiver Thread
if "receiver_started" not in st.session_state:
    start_receiver_thread()
    st.session_state["receiver_started"] = True

# Main Application Routing Logic
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    # Force reset session state if it still points to the old hidden page
    if st.session_state.get("Navigation Menu") == "Ride History":
        st.session_state["Navigation Menu"] = "Home & Profile"
        
    render_dashboard()
else:
    render_auth_page()