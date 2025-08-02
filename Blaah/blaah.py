import streamlit as st
import time
import random
import datetime
import os

# --- Configuration ---
# File path for the audio file. Update this to your file's location.
# This path is relative to where you run the script.
# For example, if you put WakeMeNot.mp3 in the same folder as this script, 
# the path is simply "WakeMeNot.mp3".
AUDIO_FILE = r".venv\Blaah\WakeMeNot.mp3"

# List of encouraging messages
MESSAGES = [
    "🌙 It's okay to rest. You deserve it.",
    "😴 Sleep is self-care. Close your eyes and breathe.",
    "🛌 Let the world wait. You need peace.",
    "💤 Great dreams need sleep to grow.",
    "🧸 Be gentle to yourself. Sleep well.",
    "📵 Forget the screens. Find your calm.",
]

# --- Streamlit UI Setup ---
st.set_page_config(
    page_title="Sleep Encouragement Alarm",
    page_icon="💤",
    layout="centered"
)

st.title("💤 Sleep Encouragement Alarm")
st.markdown("Set a time, and a gentle message will appear to remind you to rest.")

# Initialize Streamlit session state for managing the alarm
if 'alarm_active' not in st.session_state:
    st.session_state.alarm_active = False

if 'alarm_time' not in st.session_state:
    st.session_state.alarm_time = "22:00"

# --- Main Interface ---
time_input = st.text_input(
    "Set your alarm time (HH:MM, 24-hour format):",
    value=st.session_state.alarm_time
)

# Start/Stop buttons in a horizontal layout
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Alarm", use_container_width=True, disabled=st.session_state.alarm_active):
        try:
            # Validate the time format
            datetime.datetime.strptime(time_input, "%H:%M")
            st.session_state.alarm_time = time_input
            st.session_state.alarm_active = True
            st.success(f"Alarm set for {st.session_state.alarm_time}! Waiting...")
            st.balloons()
        except ValueError:
            st.error("Invalid time format. Please use HH:MM.")

with col2:
    if st.button("Stop Alarm", use_container_width=True, disabled=not st.session_state.alarm_active):
        st.session_state.alarm_active = False
        st.warning("Alarm stopped.")

# --- Alarm Logic and Display ---
if st.session_state.alarm_active:
    status_placeholder = st.empty()
    status_placeholder.info(f"⏳ Waiting for {st.session_state.alarm_time}... Close your eyes and relax.")

    while st.session_state.alarm_active:
        current_time = datetime.datetime.now().strftime("%H:%M")

        if current_time == st.session_state.alarm_time:
            # Alarm triggered
            status_placeholder.empty()
            st.success("💤 It's time to rest!")
            st.write(random.choice(MESSAGES))
            st.snow()

            # Check if the audio file exists and play it
            if os.path.exists(AUDIO_FILE):
                st.write("🎵 Playing sound...")
                try:
                    # Read the audio file into memory and play it
                    with open(AUDIO_FILE, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format="audio/mp3")

                    st.balloons()
                except Exception as e:
                    st.error(f"⚠ Error playing sound: {e}")
            else:
                st.warning(f"🔕 (No sound file found at '{AUDIO_FILE}'. Please check the path.)")

            # Deactivate the alarm to prevent it from re-triggering
            st.session_state.alarm_active = False

        time.sleep(1) # Check the time every second
