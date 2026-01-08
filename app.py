import streamlit as st
import cv2
import mediapipe as mp
import psutil
import time
import subprocess
import numpy as np
import winsound
import sys

# Mediapip import setup
mp_drawing = mp.solutions.drawing_utils
mp_face = mp.solutions.face_mesh

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Project Aether | SDG AI Agent", layout="wide", page_icon="🌿")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #00d1b2 !important; font-size: 32px; }
    section[data-testid="stSidebar"] { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# GUIDs
POWER_SAVER = "a1841308-3541-4fab-bc81-f71556f20b4a"
BALANCED = "381b4222-f694-41f0-9685-ff5bb260df2e"

# --- 2.SESSION STATE INITIALIZATION ---
if 'last_presence_time' not in st.session_state:
    st.session_state.last_presence_time = time.time()
    st.session_state_eco_mode_active = False
    st.session_state.total_seconds_saved = 0
    st.session_state.last_update_time = time.time()
       
# Initialize Camera in Session State so that it persists across reruns
if 'cap' not in st.session_state or st.session_state.cap is None:
    st.session_state.cap = cv2.VideoCapture(0)
       
# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🛡️ Aether Sentinel")
   # st.caption(f"Environment: {sys.prefix.split('\\')[-1]}")
    st.divider()
    st.info("AI Agent Status: 🟢 ACTIVE")
    op_mode = st.radio("Operating Mode", ["Autonomous (AI)", "Manual Eco", "Performance"])
    privacy_toggle = st.toggle("Neural Privacy Shield", value=True)
    audio_toggle = st.toggle("Audio Feedback", value=False)
    st.divider()
    st.subheader("SDG Focus")
    st.caption("✅ SDG 13: Climate Action")
    st.info("Agent is monitoring hardware idle states to reduce carbon footprint.")
    st.caption("✅ SDG 7: Clean Energy")

# --- 4. MAIN LAYOUT ---
st.title("🌿 Project Aether: Autonomous Sustainability")
col_vision, col_stats, col_ledger = st.columns([2, 1, 1])

with col_vision:
    st.subheader("👁️ Neural Presence")
    video_placeholder = st.empty()

with col_stats:
    st.subheader("💻 Resource Load")
    cpu_bar = st.progress(0)
    ram_bar = st.progress(0)
    status_text = st.empty()  
    
with col_ledger:
    st.subheader("⛓️ Proof of Green")
    co2_metric = st.empty()
    token_metric = st.empty()
    block_hash = st.empty()

# --- 5. THE AI AGENT LOOP (Rerun-Safe Version) ---

# Start the FaceMesh Engine
# num_faces based off how many people might be in front of the camera. Tracking many faces makes it slower.
with mp_face.FaceMesh(max_num_faces=2, refine_landmarks=True) as face_mesh:
    cap = st.session_state.cap

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            # If a frame fails, just skip this iteration
            continue

        # AI Vision Processing
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        
        user_present = results.multi_face_landmarks is not None
        current_time = time.time()  
        
        # --- LOGIC: SAVINGS TRACKER ---
        elapsed_time = current_time - st.session_state.last_update_time
        st.session_state.last_update_time = current_time
        
        if st.session_state_eco_mode_active:
            st.session_state.total_seconds_saved += elapsed_time  
        
        # Solid dark background for drawing
        display_frame = np.zeros_like(frame_rgb)
        display_frame[:] = (10, 15, 10)
        
        # --- LOGIC: AUTOMATION & AUDIO ---
        if user_present:
            st.session_state.last_presence_time = current_time
            
            # Loop through detected faces
            for face_landamrks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image = display_frame,
                    landmark_list = face_landamrks,
                    connections = mp_face.FACEMESH_CONTOURS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 209, 178), thickness=1, circle_radius=1),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 209, 178), thickness=1)
                )
        video_placeholder.image(display_frame, channels="RGB", width='stretch')
            
            
        if st.session_state_eco_mode_active:
                # WAKE UP: Switch to Balanced Mode
                subprocess.run(f"powercfg /setactive {BALANCED}", shell=True)
                st.session_state_eco_mode_active = False
        else:
            # Check if user has been away for more than 30 seconds
            away_duration = current_time - st.session_state.last_presence_time
            if away_duration > 30 and not st.session_state_eco_mode_active:
                # SLEEP MODE: Switch to Power Saver
                subprocess.run(f"powercfg /setactive {POWER_SAVER}", shell=True)
                st.session_state_eco_mode_active = True
        
        # --- UI DISPLAY ---

        # 2. Metrics Calculation
        energy_saved_kwh = (st.session_state.total_seconds_saved * 15) / 3600000  # Assuming 15W savings
        co2_saved_grams = energy_saved_kwh * 400000 # Average CO2 per kWh

        # 3. Update Dashboard Columns
        if st.session_state_eco_mode_active:
            status_text.warning("🌿 **ECO MODE ACTIVE**: Power Saver Engaged")
        else:
            status_text.success("⚡ **PERFORMANCE MODE**: User Present")
        
        # Update Bars
        cpu_bar.progress(int(psutil.cpu_percent()))
        ram_bar.progress(int(psutil.virtual_memory().percent))

        co2_metric.metric("Total CO2 Saved", f"{co2_saved_grams:.2f} g", f"{energy_saved_kwh:.6f} kWh")
        token_metric.metric("Eco-Tokens Earned", f"{co2_saved_grams / 10:.1f} ET")
        block_hash.code(f"Block: 0x{int(co2_saved_grams * 999):x}")
        
        # A tiny sleep helps the CPU breathe
        time.sleep(0.01)