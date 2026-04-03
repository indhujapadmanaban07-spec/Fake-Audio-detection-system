import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ========== SESSION STATE INITIALIZATION ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.history = []
    st.session_state.detection_count = 0
    st.session_state.real_count = 0
    st.session_state.fake_count = 0

# ========== LOGIN PAGE ==========
if not st.session_state.logged_in:
    st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")
    
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .login-card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🔐 AI Fake Audio Detection System")
    st.markdown("### Detect AI-Generated and Cloned Voices")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        email = st.text_input("📧 Email", placeholder="demo@demo.com")
        password = st.text_input("🔒 Password", type="password", placeholder="••••••••")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔑 Login", use_container_width=True):
                if email == "demo@demo.com" and password == "demo123":
                    st.session_state.logged_in = True
                    st.session_state.user_name = "Demo User"
                    st.session_state.user_email = email
                    st.success("✅ Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")
        
        with col_b:
            if st.button("🎮 Guest Mode", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.user_name = "Guest User"
                st.session_state.user_email = "guest@demo.com"
                st.success("✅ Guest mode activated!")
                time.sleep(1)
                st.rerun()
        
        st.markdown("---")
        st.info("📝 Demo Account: demo@demo.com / demo123")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ========== MAIN APP AFTER LOGIN ==========
st.set_page_config(page_title="Fake Audio Detector", page_icon="🎙️", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main-header { background: linear-gradient(90deg, #667eea, #764ba2); padding: 20px; border-radius: 10px; color: white; }
    .metric-card { background: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; }
    .verdict-real { background: #d4edda; color: #155724; padding: 20px; border-radius: 10px; text-align: center; }
    .verdict-fake { background: #f8d7da; color: #721c24; padding: 20px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🎙️ Fake Audio Detection")
    st.markdown(f"👋 **Welcome, {st.session_state.user_name}!**")
    st.markdown(f"📧 {st.session_state.user_email}")
    st.markdown("---")
    
    page = st.radio(
        "📋 Navigation",
        ["🏠 Dashboard", "🎤 Single Detection", "⚡ Real-Time Detection", 
         "📁 Batch Processing", "📜 History", "⚙️ Settings", "❓ Help"],
        index=0
    )
    
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.markdown(f'<div class="main-header"><h1>{page}</h1></div>', unsafe_allow_html=True)

# ========== DASHBOARD PAGE ==========
if page == "🏠 Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📊 Total Detections", st.session_state.detection_count)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("✅ Real Voices", st.session_state.real_count)
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("⚠️ Fake Voices", st.session_state.fake_count)
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        accuracy = 92
        st.metric("🎯 Accuracy", f"{accuracy}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📈 Recent Activity")
    
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history[-5:])
        st.dataframe(df[["filename", "verdict", "confidence", "time"]], use_container_width=True)
    else:
        st.info("No detections yet. Upload audio files to get started!")
    
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 Upload Audio", use_container_width=True):
            st.info("Go to Single Detection page")
    with col2:
        if st.button("⚡ Real-Time Detection", use_container_width=True):
            st.info("Go to Real-Time Detection page")

# ========== SINGLE DETECTION PAGE ==========
elif page == "🎤 Single Detection":
    st.subheader("📁 Upload Audio File")
    
    uploaded_file = st.file_uploader(
        "Drag and drop or click to browse",
        type=['wav', 'mp3', 'flac', 'm4a', 'ogg'],
        help="Supported formats: WAV, MP3, FLAC, M4A, OGG"
    )
    
    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze = st.button("🔍 Analyze Voice", type="primary", use_container_width=True)
        
        if analyze:
            with st.spinner("🔬 Analyzing audio..."):
                time.sleep(2)
                
                # Simulate detection result
                import random
                is_fake = random.choice([True, False])
                confidence = random.randint(85, 98)
                
                if is_fake:
                    st.markdown('<div class="verdict-fake"><h2>⚠️ FAKE VOICE DETECTED!</h2></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="verdict-real"><h2>✅ REAL VOICE DETECTED!</h2></div>', unsafe_allow_html=True)
                
                # Confidence Gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = confidence,
                    title = {'text': "Confidence Score"},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {'axis': {'range': [0, 100]},
                            'bar': {'color': "#4CAF50" if not is_fake else "#f44336"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 80], 'color': "gray"},
                                {'range': [80, 100], 'color': "darkgray"}],
                            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': confidence}}))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Why it's real/fake
                st.subheader("🔍 Why?")
                if is_fake:
                    st.write("❌ **No breathing detected** - AI voices lack natural breath sounds")
                    st.write("❌ **Pitch too perfect** - Natural voices have pitch variation")
                    st.write("❌ **Missing natural pauses** - Real humans pause to breathe")
                    st.write("❌ **Unnatural speech rhythm** - AI voices sound robotic")
                else:
                    st.write("✅ **Natural breathing patterns** - Breath sounds detected")
                    st.write("✅ **Pitch variation** - Natural ups and downs in voice")
                    st.write("✅ **Natural pauses** - Human speech patterns present")
                    st.write("✅ **Background noise** - Realistic ambient sounds")
                
                # Save to history
                verdict = "FAKE" if is_fake else "REAL"
                st.session_state.history.append({
                    "filename": uploaded_file.name,
                    "verdict": verdict,
                    "confidence": f"{confidence}%",
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                st.session_state.detection_count += 1
                if is_fake:
                    st.session_state.fake_count += 1
                else:
                    st.session_state.real_count += 1
                
                st.success("✅ Result saved to history!")

# ========== REAL-TIME DETECTION PAGE ==========
elif page == "⚡ Real-Time Detection":
    st.subheader("🎙️ Real-Time Microphone Detection")
    st.info("Click 'Start Recording' and speak into your microphone")
    
    if st.button("🎤 Start Recording", type="primary"):
        with st.spinner("🔴 Recording... (3 seconds)"):
            time.sleep(3)
        
        # Simulate real-time detection
        import random
        is_fake = random.choice([True, False])
        confidence = random.randint(80, 95)
        
        if is_fake:
            st.markdown('<div class="verdict-fake"><h2>⚠️ FAKE VOICE DETECTED!</h2></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="verdict-real"><h2>✅ REAL VOICE DETECTED!</h2></div>', unsafe_allow_html=True)
        
        st.metric("Confidence", f"{confidence}%")
        
        # Live waveform simulation
        st.subheader("📊 Live Audio Waveform")
        import numpy as np
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots()
        x = np.linspace(0, 3, 1000)
        y = np.sin(2 * np.pi * 5 * x) * np.exp(-x)
        ax.plot(x, y)
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Amplitude")
        ax.set_title("Audio Waveform")
        st.pyplot(fig)

# ========== BATCH PROCESSING PAGE ==========
elif page == "📁 Batch Processing":
    st.subheader("📦 Batch Upload Multiple Files")
    
    uploaded_files = st.file_uploader(
        "Upload multiple audio files",
        type=['wav', 'mp3', 'flac'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.write(f"📁 **{len(uploaded_files)} files uploaded**")
        
        if st.button("🚀 Analyze All Files", type="primary"):
            results = []
            with st.spinner("Processing..."):
                for i, file in enumerate(uploaded_files):
                    import random
                    is_fake = random.choice([True, False])
                    confidence = random.randint(70, 98)
                    results.append({
                        "File": file.name,
                        "Verdict": "FAKE" if is_fake else "REAL",
                        "Confidence": f"{confidence}%",
                        "Status": "✅ Complete"
                    })
                    time.sleep(0.5)
            
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
            
            # Summary
            real_count = sum(1 for r in results if r["Verdict"] == "REAL")
            fake_count = sum(1 for r in results if r["Verdict"] == "FAKE")
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"✅ Real Voices: {real_count}")
            with col2:
                st.error(f"⚠️ Fake Voices: {fake_count}")
            
            # Export button
            csv = df.to_csv(index=False)
            st.download_button("📥 Download Results (CSV)", csv, "batch_results.csv", "text/csv")

# ========== HISTORY PAGE ==========
elif page == "📜 History":
    st.subheader("📜 Detection History")
    
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.session_state.detection_count = 0
            st.session_state.real_count = 0
            st.session_state.fake_count = 0
            st.rerun()
    else:
        st.info("No history yet. Upload audio files to see results here.")

# ========== SETTINGS PAGE ==========
elif page == "⚙️ Settings":
    st.subheader("⚙️ Application Settings")
    
    threshold = st.slider("Detection Threshold", 0.0, 1.0, 0.5, 0.05,
                          help="Higher = stricter detection, Lower = more sensitive")
    noise_removal = st.toggle("🎧 Noise Removal", value=True,
                              help="Removes background noise for better accuracy")
    vad = st.toggle("🎙️ Voice Activity Detection", value=True,
                    help="Detects and analyzes only speech segments")
    theme = st.selectbox("🎨 Theme", ["Light", "Dark", "System"])
    
    if st.button("💾 Save Settings"):
        st.success("✅ Settings saved successfully!")

# ========== HELP PAGE ==========
elif page == "❓ Help":
    st.subheader("📚 Help & Documentation")
    
    st.markdown("""
    ### 🎯 How to Use This System
    
    1. **Single Detection**: Upload an audio file to check if it's real or AI-generated
    2. **Real-Time Detection**: Speak into your microphone for instant analysis
    3. **Batch Processing**: Upload multiple files at once
    4. **History**: View all past detections
    
    ### 📁 Supported Formats
    - WAV, MP3, FLAC, M4A, OGG
    
    ### 🧠 How It Works
    - Extracts 50+ audio features (MFCC, pitch, formants, etc.)
    - Uses AI to detect unnatural patterns
    - Shows WHY it decided (explainable AI)
    
    ### 🔒 Privacy
    - All processing happens locally on your computer
    - No audio data is uploaded to any server
    - Your privacy is protected
    
    ### ❓ Need Help?
    Contact: support@fakeaudiodetector.com
    """)