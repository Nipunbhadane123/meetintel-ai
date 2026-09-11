import streamlit as st
import os
from dotenv import load_dotenv, set_key
from ui.components import section_header

ENV_FILE = ".env"

def render_settings_page():
    section_header("⚙️ Settings", "Configure application preferences and AI integrations")
    load_dotenv(ENV_FILE)
    
    with st.container():
        st.markdown(f"""
            <div class="settings-form-card-marker"></div>
            <style>
            div[data-testid="stVerticalBlock"]:has(.settings-form-card-marker):not(:has(div[data-testid="stVerticalBlock"]:has(.settings-form-card-marker))) {{
                background: var(--surface) !important;
                border-radius: 20px !important;
                padding: 2rem !important;
                box-shadow: var(--shadow-soft) !important;
                border: 1px solid #E2E8F0 !important;
                margin-bottom: 2rem !important;
            }}
            .settings-form-card-marker {{ display: none; }}
            </style>
        """, unsafe_allow_html=True)
        
        with st.form("settings_form"):
            st.markdown("<h4 style='color: var(--text-main); margin-top: 0; margin-bottom: var(--space-md);'>🤖 AI Configuration</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--text-main);'>AI Provider</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.5rem;'>Choose the provider used for meeting intelligence.</p>", unsafe_allow_html=True)
            with c2:
                ai_provider = st.selectbox("AI Provider", ["Gemini", "OpenAI"], index=["Gemini", "OpenAI"].index(os.getenv("AI_PROVIDER", "Gemini")) if os.getenv("AI_PROVIDER", "Gemini") in ["Gemini", "OpenAI"] else 0, label_visibility="collapsed")
                
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--text-main);'>Gemini API Key</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.5rem;'>Leave blank to keep existing key.</p>", unsafe_allow_html=True)
            with c2:
                gemini_key = st.text_input("Gemini API Key", placeholder="Enter new API key...", type="password", label_visibility="collapsed")

            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--text-main);'>OpenAI API Key</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0;'>Leave blank to keep existing key.</p>", unsafe_allow_html=True)
            with c2:
                openai_key = st.text_input("OpenAI API Key", placeholder="Enter new API key...", type="password", label_visibility="collapsed")
                
            st.markdown("<hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 2rem 0;'>", unsafe_allow_html=True)

            # Transcription Section
            st.markdown("<h4 style='color: var(--text-main); margin-top: 0; margin-bottom: var(--space-md);'>🎙️ Transcription & Audio</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--text-main);'>Whisper Model</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.5rem;'>Select the transcription model.</p>", unsafe_allow_html=True)
            with c2:
                whisper_model = st.selectbox("Whisper Model", ["base", "small", "medium", "large-v3"], index=["base", "small", "medium", "large-v3"].index(os.getenv("WHISPER_MODEL", "small")) if os.getenv("WHISPER_MODEL", "small") in ["base", "small", "medium", "large-v3"] else 1, label_visibility="collapsed")
                
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--text-main);'>Hugging Face Token</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0;'>Required for Pyannote speaker diarization.</p>", unsafe_allow_html=True)
            with c2:
                hf_token = st.text_input("HF Token", placeholder="Enter new token...", type="password", label_visibility="collapsed")
                
            st.markdown("<hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 2rem 0;'>", unsafe_allow_html=True)
            
            # General & Appearance Section
            st.markdown("<h4 style='color: var(--text-main); margin-top: 0; margin-bottom: var(--space-md);'>🎨 Appearance & Storage</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--text-main);'>Theme Preference</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.5rem;'>General application appearance.</p>", unsafe_allow_html=True)
            with c2:
                st.selectbox("Theme", ["Light (Default)", "Dark", "System Match"], disabled=True, label_visibility="collapsed")
                
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--text-main);'>Local Storage Path</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0;'>Where audio files and databases are stored.</p>", unsafe_allow_html=True)
            with c2:
                st.text_input("Local Storage Path", value="data/", disabled=True, label_visibility="collapsed")
                
            st.markdown("<hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 2rem 0;'>", unsafe_allow_html=True)

            st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Save All Settings", type="primary")
            st.markdown("</div>", unsafe_allow_html=True)
            
            if submitted:
                set_key(ENV_FILE, "WHISPER_MODEL", whisper_model)
                set_key(ENV_FILE, "AI_PROVIDER", ai_provider)
                if hf_token: set_key(ENV_FILE, "HUGGINGFACE_TOKEN", hf_token)
                if gemini_key: set_key(ENV_FILE, "GEMINI_API_KEY", gemini_key)
                if openai_key: set_key(ENV_FILE, "OPENAI_API_KEY", openai_key)
                st.success("Settings saved successfully! Some changes may require restarting the application.")
            
    # System Information Card
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("💻 System Information", "Current environment and dependencies")
    
    hf_status = "Available" if os.getenv("HUGGINGFACE_TOKEN") else "Missing Token"
    hf_color = "var(--success)" if os.getenv("HUGGINGFACE_TOKEN") else "var(--error)"
    
    gemini_status = "Connected" if os.getenv("GEMINI_API_KEY") else "Missing Key"
    gemini_color = "var(--success)" if os.getenv("GEMINI_API_KEY") else "var(--warning)"
    
    html = f"""
    <div class="saas-card">
        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #E2E8F0; padding-bottom: 0.75rem; margin-bottom: 0.75rem;">
            <span style="font-weight: 600; color: var(--text-main);">System Status</span>
            <span style="color: var(--success); font-weight: 600;">✓ Ready</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--text-muted);">Python</span>
            <span style="font-family: monospace; color: var(--text-main);">3.10+</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--text-muted);">FFmpeg</span>
            <span style="font-family: monospace; color: var(--text-main);">Installed</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--text-muted);">Whisper</span>
            <span style="color: var(--success);">Available</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--text-muted);">Speaker Diarization</span>
            <span style="color: {hf_color};">{hf_status}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--text-muted);">Gemini</span>
            <span style="color: {gemini_color};">{gemini_status}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--text-muted);">Database</span>
            <span style="color: var(--text-main);">SQLite</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
