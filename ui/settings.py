import streamlit as st
import os
from dotenv import load_dotenv, set_key
from ui.components import section_header

ENV_FILE = ".env"

def render_settings_page():
    st.markdown("""
        <div class="page-title-container" style="margin-bottom: var(--mt-space-xl);">
            <h2 class="page-title" style="color: var(--mt-text); font-weight: 750; font-size: 2.2rem; margin: 0 0 8px 0; letter-spacing: -0.02em;"><span style="color: var(--mt-primary);">⏣</span> Settings</h2>
            <p class="page-subtitle" style="color: var(--mt-text-secondary); font-size: 1.1rem; margin: 0;">Configure application preferences and AI integrations.</p>
        </div>
    """, unsafe_allow_html=True)
    load_dotenv(ENV_FILE)
    
    with st.container():
        st.markdown(f"""
            <div class="settings-form-card-marker"></div>
            <style>
            div[data-testid="stVerticalBlock"]:has(.settings-form-card-marker):not(:has(div[data-testid="stVerticalBlock"]:has(.settings-form-card-marker))) {{
                background: var(--mt-surface) !important;
                border-radius: var(--mt-radius-xl) !important;
                padding: var(--mt-space-2xl) !important;
                box-shadow: var(--mt-shadow-soft) !important;
                border: 1px solid var(--mt-border) !important;
                margin-bottom: var(--mt-space-2xl) !important;
            }}
            .settings-form-card-marker {{ display: none; }}
            </style>
        """, unsafe_allow_html=True)
        
        with st.form("settings_form"):
            st.markdown("<h4 style='color: var(--mt-text); margin-top: 0; margin-bottom: var(--mt-space-lg); font-weight: 650; font-size: 1.25rem;'>🤖 AI Configuration</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 1rem; font-weight: 600; margin: 0; color: var(--mt-text);'>AI Provider</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.9rem; color: var(--mt-text-secondary); margin-bottom: 1.5rem;'>Choose the provider used for meeting intelligence.</p>", unsafe_allow_html=True)
            with c2:
                ai_provider = st.selectbox("AI Provider", ["Gemini", "OpenAI"], index=["Gemini", "OpenAI"].index(os.getenv("AI_PROVIDER", "Gemini")) if os.getenv("AI_PROVIDER", "Gemini") in ["Gemini", "OpenAI"] else 0, label_visibility="collapsed")
                
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 1rem; font-weight: 600; margin: 0; color: var(--mt-text);'>Gemini API Key</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.9rem; color: var(--mt-text-secondary); margin-bottom: 1.5rem;'>Leave blank to keep existing key.</p>", unsafe_allow_html=True)
            with c2:
                gemini_key = st.text_input("Gemini API Key", placeholder="Enter new API key...", type="password", label_visibility="collapsed")

            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 1rem; font-weight: 600; margin: 0; color: var(--mt-text);'>OpenAI API Key</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.9rem; color: var(--mt-text-secondary); margin-bottom: 0;'>Leave blank to keep existing key.</p>", unsafe_allow_html=True)
            with c2:
                openai_key = st.text_input("OpenAI API Key", placeholder="Enter new API key...", type="password", label_visibility="collapsed")
                
            st.markdown("<hr style='border: 0; border-top: 1px solid var(--mt-border); margin: 2rem 0;'>", unsafe_allow_html=True)

            # Transcription Section
            st.markdown("<h4 style='color: var(--mt-text); margin-top: 0; margin-bottom: var(--mt-space-lg); font-weight: 650; font-size: 1.25rem;'>🎙️ Transcription & Audio</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 1rem; font-weight: 600; margin: 0; color: var(--mt-text);'>Whisper Model</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.9rem; color: var(--mt-text-secondary); margin-bottom: 1.5rem;'>Select the transcription model.</p>", unsafe_allow_html=True)
            with c2:
                whisper_model = st.selectbox("Whisper Model", ["base", "small", "medium", "large-v3"], index=["base", "small", "medium", "large-v3"].index(os.getenv("WHISPER_MODEL", "small")) if os.getenv("WHISPER_MODEL", "small") in ["base", "small", "medium", "large-v3"] else 1, label_visibility="collapsed")
                
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 1rem; font-weight: 600; margin: 0; color: var(--mt-text);'>Hugging Face Token</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.9rem; color: var(--mt-text-secondary); margin-bottom: 0;'>Required for Pyannote speaker diarization.</p>", unsafe_allow_html=True)
            with c2:
                hf_token = st.text_input("HF Token", placeholder="Enter new token...", type="password", label_visibility="collapsed")
                
            st.markdown("<hr style='border: 0; border-top: 1px solid var(--mt-border); margin: 2rem 0;'>", unsafe_allow_html=True)
            
            # General & Appearance Section
            st.markdown("<h4 style='color: var(--mt-text); margin-top: 0; margin-bottom: var(--mt-space-lg); font-weight: 650; font-size: 1.25rem;'>🎨 Appearance & Storage</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 1rem; font-weight: 600; margin: 0; color: var(--mt-text);'>Theme Preference</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.9rem; color: var(--mt-text-secondary); margin-bottom: 1.5rem;'>General application appearance.</p>", unsafe_allow_html=True)
            with c2:
                st.selectbox("Theme", ["Light (Default)", "Dark", "System Match"], disabled=True, label_visibility="collapsed")
                
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 1rem; font-weight: 600; margin: 0; color: var(--mt-text);'>Local Storage Path</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.9rem; color: var(--mt-text-secondary); margin-bottom: 0;'>Where audio files and databases are stored.</p>", unsafe_allow_html=True)
            with c2:
                st.text_input("Local Storage Path", value="data/", disabled=True, label_visibility="collapsed")
                
            st.markdown("<hr style='border: 0; border-top: 1px solid var(--mt-border); margin: 2rem 0;'>", unsafe_allow_html=True)

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
    st.markdown("""
        <div class="page-title-container" style="border-bottom: none; margin-bottom: var(--mt-space-md);">
            <h3 class="page-title" style="font-size: 1.5rem; color: var(--mt-text); font-weight: 700;">💻 System Information</h3>
            <p class="page-subtitle" style="color: var(--mt-text-secondary);">Current environment and dependencies.</p>
        </div>
    """, unsafe_allow_html=True)
    
    hf_status = "Available" if os.getenv("HUGGINGFACE_TOKEN") else "Missing Token"
    hf_color = "var(--mt-success)" if os.getenv("HUGGINGFACE_TOKEN") else "var(--mt-error)"
    
    gemini_status = "Connected" if os.getenv("GEMINI_API_KEY") else "Missing Key"
    gemini_color = "var(--mt-success)" if os.getenv("GEMINI_API_KEY") else "var(--mt-warning)"
    
    html = f"""
    <div class="saas-card" style="padding: var(--mt-space-xl);">
        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--mt-border); padding-bottom: 1rem; margin-bottom: 1rem;">
            <span style="font-weight: 650; color: var(--mt-text); font-size: 1.1rem;">System Status</span>
            <span style="color: var(--mt-success); font-weight: 650; background: rgba(16, 185, 129, 0.1); padding: 4px 12px; border-radius: 20px; font-size: 0.9rem;">✓ Ready</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--mt-text-secondary); font-weight: 500;">Python</span>
            <span style="font-family: monospace; color: var(--mt-text); font-weight: 500; background: var(--mt-surface-soft); padding: 2px 8px; border-radius: 4px; border: 1px solid var(--mt-border);">3.10+</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--mt-text-secondary); font-weight: 500;">FFmpeg</span>
            <span style="font-family: monospace; color: var(--mt-text); font-weight: 500; background: var(--mt-surface-soft); padding: 2px 8px; border-radius: 4px; border: 1px solid var(--mt-border);">Installed</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--mt-text-secondary); font-weight: 500;">Whisper</span>
            <span style="color: var(--mt-success); font-weight: 500;">Available</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--mt-text-secondary); font-weight: 500;">Speaker Diarization</span>
            <span style="color: {hf_color}; font-weight: 500;">{hf_status}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--mt-text-secondary); font-weight: 500;">Gemini</span>
            <span style="color: {gemini_color}; font-weight: 500;">{gemini_status}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="color: var(--mt-text-secondary); font-weight: 500;">Database</span>
            <span style="color: var(--mt-text); font-weight: 500;">SQLite</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
