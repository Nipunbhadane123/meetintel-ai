import streamlit as st
import os
from dotenv import load_dotenv, set_key
from ui.components import page_header, render_status_badge, get_icon_svg
from storage.database import SessionLocal
from storage.models import User
from storage import repository
from ui.demo_seeder import seed_enterprise_demo_data

ENV_FILE = ".env"

def render_settings_page():
    page_header(
        title="Settings & System Administration",
        subtitle="Configure platform AI providers, multi-user role profiles, and examiner demonstration controls.",
        category="Administration & System",
        badge_text="System Control",
        badge_type="accent",
        icon="settings"
    )
    load_dotenv(ENV_FILE)
    
    db = SessionLocal()
    try:
        # Fast Role Switcher for Examiner Demonstration
        with st.container(border=True):
            col_rs1, col_rs2 = st.columns([3, 1])
            with col_rs1:
                st.markdown("<h3 style='color: var(--mt-text); margin: 0; font-size: 1.15rem; font-weight: 700;'>🎭 Fast Role & Identity Switcher</h3>", unsafe_allow_html=True)
                st.markdown("<p style='color: var(--mt-text-secondary); margin: 2px 0 8px 0; font-size: 0.88rem;'>Instantly switch identities to demonstrate role-based permissions and task isolation.</p>", unsafe_allow_html=True)
            with col_rs2:
                st.markdown(f"<div style='text-align: right;'>{render_status_badge('Examiner Tool', 'demo')}</div>", unsafe_allow_html=True)

            org_users = db.query(User).all()
            user_choices = {f"{u.full_name or u.username} ({u.role})": u for u in org_users}
            current_uid = st.session_state.get('user_id')
            curr_u = repository.get_user_by_id(db, current_uid) if current_uid else None
            curr_label = f"{curr_u.full_name or curr_u.username} ({curr_u.role})" if curr_u and f"{curr_u.full_name or curr_u.username} ({curr_u.role})" in user_choices else (list(user_choices.keys())[0] if user_choices else "Default")

            if user_choices:
                c_role1, c_role2 = st.columns([3, 1])
                with c_role1:
                    selected_role_label = st.selectbox("Active Profile", list(user_choices.keys()), index=list(user_choices.keys()).index(curr_label), label_visibility="collapsed")
                with c_role2:
                    if st.button("Switch Identity", type="primary", use_container_width=True):
                        chosen = user_choices[selected_role_label]
                        st.session_state['user_id'] = chosen.id
                        st.session_state['username'] = chosen.username
                        st.session_state['current_page'] = "Dashboard"
                        st.toast(f"Switched identity to {chosen.full_name or chosen.username} ({chosen.role})!")
                        st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # 1-Click Demo Seeder
        with st.container(border=True):
            st.markdown("<h3 style='color: var(--mt-text); margin: 0; font-size: 1.15rem; font-weight: 700;'>🚀 Seed Examiner Demonstration Scenario</h3>", unsafe_allow_html=True)
            st.markdown("""
            <p style="color: var(--mt-text-secondary); margin: 2px 0 12px 0; font-size: 0.88rem;">
                Populate cohesive Acme Global enterprise data: meetings, verified action items with evidence, approved decisions, calendar sync, and absent employee follow-up drafts.
            </p>
            """, unsafe_allow_html=True)
            
            if st.button("✦ Seed Enterprise Demonstration Scenario", type="primary"):
                with st.spinner("Seeding verified meeting intelligence scenario..."):
                    res = seed_enterprise_demo_data(db)
                    st.success(f"Successfully seeded enterprise demonstration data! Meeting #{res['meeting_id']} created with {res['tasks_seeded']} action items and {res['decisions_seeded']} decision records.")
                    st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        # Settings Form
        with st.form("settings_form"):
            st.markdown("<h4 style='color: var(--mt-text); margin-top: 0; margin-bottom: 16px; font-weight: 700; font-size: 1.15rem;'>🤖 AI Provider Configuration</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--mt-text);'>Primary AI Provider</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--mt-text-secondary); margin-bottom: 1.2rem;'>Choose the provider used for meeting intelligence.</p>", unsafe_allow_html=True)
            with c2:
                providers = ["Gemini", "OpenAI", "Demo (Local Offline)"]
                current_p = os.getenv("AI_PRIMARY_PROVIDER", os.getenv("AI_PROVIDER", "Gemini")).capitalize()
                curr_idx = 0
                for i, p in enumerate(providers):
                    if current_p.lower() in p.lower():
                        curr_idx = i
                ai_provider = st.selectbox("AI Provider", providers, index=curr_idx, label_visibility="collapsed")
                
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--mt-text);'>Gemini API Key</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--mt-text-secondary); margin-bottom: 1.2rem;'>Used for AI meeting intelligence. Keep this key private.</p>", unsafe_allow_html=True)
            with c2:
                gemini_key = st.text_input("Gemini API Key", placeholder="Enter new API key... 👁", type="password", label_visibility="collapsed")

            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--mt-text);'>OpenAI API Key</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--mt-text-secondary); margin-bottom: 1.2rem;'>Used automatically as a fallback when the primary AI provider is unavailable.</p>", unsafe_allow_html=True)
            with c2:
                openai_key = st.text_input("OpenAI API Key", placeholder="Enter new API key... 👁", type="password", label_visibility="collapsed")
                
            st.markdown("<hr style='border: 0; border-top: 1px solid var(--mt-border); margin: 1.5rem 0;'>", unsafe_allow_html=True)

            # Transcription Section
            st.markdown("<h4 style='color: var(--mt-text); margin-top: 0; margin-bottom: 16px; font-weight: 700; font-size: 1.15rem;'>🎙️ Transcription & Audio</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--mt-text);'>Whisper Model</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--mt-text-secondary); margin-bottom: 1.2rem;'>Select the local transcription model.</p>", unsafe_allow_html=True)
            with c2:
                whisper_model = st.selectbox("Whisper Model", ["base", "small", "medium", "large-v3"], index=["base", "small", "medium", "large-v3"].index(os.getenv("WHISPER_MODEL", "small")) if os.getenv("WHISPER_MODEL", "small") in ["base", "small", "medium", "large-v3"] else 1, label_visibility="collapsed")
                
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--mt-text);'>Hugging Face Token</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--mt-text-secondary); margin-bottom: 0;'>Required for Pyannote speaker diarization.</p>", unsafe_allow_html=True)
            with c2:
                hf_token = st.text_input("HF Token", placeholder="Enter new token...", type="password", label_visibility="collapsed")
                
            st.markdown("<hr style='border: 0; border-top: 1px solid var(--mt-border); margin: 1.5rem 0;'>", unsafe_allow_html=True)
            
            # General & Appearance Section
            st.markdown("<h4 style='color: var(--mt-text); margin-top: 0; margin-bottom: 16px; font-weight: 700; font-size: 1.15rem;'>🎨 Appearance & Theme</h4>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([65, 35])
            with c1:
                st.markdown("<p style='font-size: 0.95rem; font-weight: 600; margin: 0; color: var(--mt-text);'>Theme Preference</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: var(--mt-text-secondary); margin-bottom: 1.2rem;'>Accessible light and dark surfaces.</p>", unsafe_allow_html=True)
            with c2:
                theme_options = {"System ◒": "System", "Light ☀": "Light", "Dark ◐": "Dark"}
                current_theme = st.session_state.get('theme_preference', 'System')
                display_options = list(theme_options.keys())
                current_display = "System ◒"
                for disp, val in theme_options.items():
                    if val == current_theme:
                        current_display = disp
                        break
                selected_theme_display = st.selectbox("Theme", display_options, index=display_options.index(current_display), label_visibility="collapsed")
                
            st.markdown("<hr style='border: 0; border-top: 1px solid var(--mt-border); margin: 1.5rem 0;'>", unsafe_allow_html=True)

            submitted = st.form_submit_button("Save All Settings", type="primary")
            if submitted:
                prov_val = "demo" if "demo" in ai_provider.lower() else ("openai" if "openai" in ai_provider.lower() else "gemini")
                set_key(ENV_FILE, "WHISPER_MODEL", whisper_model)
                set_key(ENV_FILE, "AI_PRIMARY_PROVIDER", prov_val)
                if hf_token: set_key(ENV_FILE, "HUGGINGFACE_TOKEN", hf_token)
                if gemini_key: set_key(ENV_FILE, "GEMINI_API_KEY", gemini_key)
                if openai_key: set_key(ENV_FILE, "OPENAI_API_KEY", openai_key)
                
                new_theme_value = theme_options[selected_theme_display]
                st.session_state['theme_preference'] = new_theme_value
                
                if 'user_id' in st.session_state:
                    user_rec = db.query(User).filter(User.id == st.session_state['user_id']).first()
                    if user_rec:
                        user_rec.theme_preference = new_theme_value
                        db.commit()
                
                st.success("Settings saved successfully!")
                st.rerun()

        # System Health Information
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            col_sh1, col_sh2 = st.columns([3, 1])
            with col_sh1:
                st.markdown("<h3 style='font-size: 1.15rem; color: var(--mt-text); font-weight: 700; margin: 0;'>💻 System Architecture & Runtime Status</h3>", unsafe_allow_html=True)
                st.caption("Enterprise runtime services and component health.")
            with col_sh2:
                st.markdown(f"<div style='text-align: right;'>{render_status_badge('Operational', 'status')}</div>", unsafe_allow_html=True)

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            
            services = [
                ("Database & Storage", "SQLite (Local) / PostgreSQL Compatible"),
                ("Vector Database", "ChromaDB (Isolated Tenant Chunks)"),
                ("Speech Engine", "Faster-Whisper (CTranslate2)"),
                ("Speaker Diarization", "Pyannote.Audio 3.1+"),
                ("Background Automation", "Persistent Queue Worker (Backoff & Jitter)"),
                ("Security & Encryption", "Fernet 32-byte AES at rest")
            ]
            for idx, (s_name, s_desc) in enumerate(services):
                if idx > 0:
                    st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 6px 0;'></div>", unsafe_allow_html=True)
                col_s_a, col_s_b = st.columns([1, 1])
                with col_s_a:
                    st.markdown(f"<span style='color: var(--mt-text-secondary); font-size: 0.88rem;'>{s_name}</span>", unsafe_allow_html=True)
                with col_s_b:
                    st.markdown(f"<span style='font-weight: 600; color: var(--mt-text); font-size: 0.88rem;'>{s_desc}</span>", unsafe_allow_html=True)
    finally:
        db.close()
