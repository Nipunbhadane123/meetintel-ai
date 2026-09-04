import streamlit as st
import os
from dotenv import set_key

ENV_FILE = ".env"

def render_settings_page():
    st.title("Settings")
    st.markdown("### Application Configuration")
    
    # Check if .env exists
    if not os.path.exists(ENV_FILE):
        open(ENV_FILE, 'a').close()
    
    # Forms for settings
    with st.form("settings_form"):
        st.subheader("Transcription Preferences")
        whisper_model = st.selectbox(
            "Whisper Model",
            ["base", "small", "medium", "large-v3"],
            index=["base", "small", "medium", "large-v3"].index(os.getenv("WHISPER_MODEL", "base"))
        )
        
        st.subheader("AI Preferences")
        ai_provider = st.selectbox(
            "AI Provider",
            ["Gemini", "OpenAI"],
            index=["Gemini", "OpenAI"].index(os.getenv("AI_PROVIDER", "Gemini"))
        )
        
        st.subheader("API Keys")
        hf_token = st.text_input("Hugging Face Token (for Pyannote)", value=os.getenv("HUGGINGFACE_TOKEN", ""), type="password")
        gemini_key = st.text_input("Gemini API Key", value=os.getenv("GEMINI_API_KEY", ""), type="password")
        openai_key = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
        
        submitted = st.form_submit_button("Save Settings")
        
        if submitted:
            set_key(ENV_FILE, "WHISPER_MODEL", whisper_model)
            set_key(ENV_FILE, "AI_PROVIDER", ai_provider)
            set_key(ENV_FILE, "HUGGINGFACE_TOKEN", hf_token)
            set_key(ENV_FILE, "GEMINI_API_KEY", gemini_key)
            set_key(ENV_FILE, "OPENAI_API_KEY", openai_key)
            st.success("Settings saved successfully! Some changes may require restarting the application.")
            
    st.markdown("---")
    st.subheader("API Status")
    
    if os.getenv("HUGGINGFACE_TOKEN"):
        st.success("Hugging Face Token: Configured")
    else:
        st.error("Hugging Face Token: Not Configured (Required for Diarization)")
        
    if os.getenv("GEMINI_API_KEY"):
        st.success("Gemini API Key: Configured")
    else:
        st.warning("Gemini API Key: Not Configured")
        
    if os.getenv("OPENAI_API_KEY"):
        st.success("OpenAI API Key: Configured")
    else:
        st.info("OpenAI API Key: Not Configured")
