import streamlit as st
from storage.database import get_db
from storage.repository import get_user_by_username, create_user
from storage.auth import verify_password, hash_password

def render_login_page():
    # Hide the default app padding for the login page to allow full width
    st.markdown("""
        <style>
        .block-container {
            max-width: 100% !important;
            padding: 0 !important;
        }
        .stApp {
            background-image: none !important;
            background-color: var(--mt-bg) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("""
<style>
div.stMarkdown .login-left-panel, div.stMarkdown .login-left-panel p, div.stMarkdown .login-left-panel h1, div.stMarkdown .login-left-panel span, div.stMarkdown .login-left-panel div {
    color: #FFFFFF !important;
}
div.stMarkdown .login-left-desc {
    color: #EDEBFF !important;
}
div.stMarkdown .login-pill {
    color: #F8FAFF !important;
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.35) !important;
}
div.stMarkdown .login-arrow {
    color: rgba(255,255,255,0.75) !important;
}
</style>
<div class="login-left-panel" style="height: 100vh; display: flex; flex-direction: column; justify-content: center; padding: 5rem; position: relative; overflow: hidden; background: linear-gradient(135deg, #4338CA 0%, #6366F1 50%, #7C3AED 100%); border-top-right-radius: 40px; border-bottom-right-radius: 40px; box-shadow: 15px 0 40px rgba(108, 76, 241, 0.15);">
<div style="position: absolute; top: -150px; left: -50px; width: 400px; height: 400px; background: radial-gradient(circle, rgba(6,182,212,0.15) 0%, transparent 70%); border-radius: 50%; filter: blur(50px); pointer-events: none;"></div>
<div style="position: absolute; bottom: -100px; right: -50px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(124,58,237,0.2) 0%, transparent 70%); border-radius: 50%; filter: blur(40px); pointer-events: none;"></div>
<div style="position: relative; z-index: 1;">
<div style="font-size: 1.5rem; font-weight: 750; margin-bottom: 2rem; letter-spacing: -0.02em; display: flex; align-items: center; gap: 10px;">
<div style="color: rgba(255,255,255,0.9) !important; filter: drop-shadow(0 2px 10px rgba(255,255,255,0.3));">✦</div> 
MeetIntel AI
</div>
<h1 style="font-size: 3rem; font-weight: 750; line-height: 1.1; margin-bottom: 1.5rem; text-shadow: 0 1px 2px rgba(30, 20, 80, 0.12) !important;">AI-Powered<br>Meeting Intelligence</h1>
<p class="login-left-desc" style="font-size: 1.1rem; line-height: 1.6; max-width: 450px; margin-bottom: 3rem;">
Turn every conversation into searchable, actionable intelligence.
</p>
<div style="display: flex; align-items: center; gap: 12px; font-size: 0.9rem; font-weight: 600; letter-spacing: 0.02em;">
<span class="login-pill" style="padding: 6px 12px; border-radius: 12px;">Transcript</span>
<span class="login-arrow">→</span>
<span class="login-pill" style="padding: 6px 12px; border-radius: 12px;">Insights</span>
<span class="login-arrow">→</span>
<span class="login-pill" style="padding: 6px 12px; border-radius: 12px;">Decisions</span>
<span class="login-arrow">→</span>
<span class="login-pill" style="padding: 6px 12px; border-radius: 12px;">Action Items</span>
</div>
</div>
</div>
""", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="padding: 0 4rem; max-width: 500px; margin: 0 auto;">
                <h2 style="font-size: 2rem; font-weight: 700; color: var(--mt-text); margin-bottom: 8px; letter-spacing: -0.02em;">Welcome back</h2>
                <p style="color: var(--mt-text-secondary); font-size: 1rem; margin-bottom: 32px;">Please enter your details to access your workspace.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Center the tabs in the right column
        c_left, c_mid, c_right = st.columns([1, 4, 1])
        with c_mid:
            tab1, tab2 = st.tabs(["Login", "Create Account"])
            
            with tab1:
                with st.form("login_form", clear_on_submit=False):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    submit = st.form_submit_button("Sign in", type="primary", use_container_width=True)
                    
                    if submit:
                        if not username or not password:
                            st.error("Please enter both username and password.")
                        else:
                            db = next(get_db())
                            user = get_user_by_username(db, username)
                            if user and verify_password(password, user.hashed_password):
                                st.session_state['user_id'] = user.id
                                st.session_state['username'] = user.username
                                st.session_state['theme_preference'] = getattr(user, 'theme_preference', 'System')
                                st.session_state['current_page'] = "Dashboard"
                                st.rerun()
                            else:
                                st.error("Invalid username or password.")
                                
            with tab2:
                with st.form("register_form", clear_on_submit=False):
                    new_username = st.text_input("Username")
                    new_email = st.text_input("Email")
                    new_password = st.text_input("Password", type="password")
                    new_password_confirm = st.text_input("Confirm Password", type="password")
                    reg_submit = st.form_submit_button("Register", type="primary", use_container_width=True)
                    
                    if reg_submit:
                        if not new_username or not new_email or not new_password:
                            st.error("Please fill in all fields.")
                        elif new_password != new_password_confirm:
                            st.error("Passwords do not match.")
                        else:
                            db = next(get_db())
                            existing_user = get_user_by_username(db, new_username)
                            if existing_user:
                                st.error("Username already exists.")
                            else:
                                user = create_user(db, new_username, new_email, hash_password(new_password))
                                st.success("Registration successful! Please login.")
                            
def logout():
    st.session_state.pop('user_id', None)
    st.session_state.pop('username', None)
    st.session_state.pop('theme_preference', None)
    st.session_state['current_page'] = "Login"
    st.rerun()
