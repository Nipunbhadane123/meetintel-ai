import streamlit as st
from storage.database import get_db, SessionLocal
from storage.repository import get_user_by_username, create_user
from storage.auth import verify_password, hash_password

def render_login_page():
    # Full width layout for authentication canvas
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
    color: #F0ECFF !important;
}
div.stMarkdown .login-pill {
    color: #FFFFFF !important;
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.28) !important;
}
div.stMarkdown .login-arrow {
    color: rgba(255,255,255,0.7) !important;
}
</style>
<div class="login-left-panel" style="height: 100vh; display: flex; flex-direction: column; justify-content: center; padding: 5rem; position: relative; overflow: hidden; background: linear-gradient(135deg, #5536E8 0%, #6C4DFF 50%, #7C3AED 100%); border-top-right-radius: 36px; border-bottom-right-radius: 36px; box-shadow: 12px 0 36px rgba(108, 77, 255, 0.12);">
<div style="position: absolute; top: -150px; left: -50px; width: 400px; height: 400px; background: radial-gradient(circle, rgba(6,182,212,0.12) 0%, transparent 70%); border-radius: 50%; filter: blur(50px); pointer-events: none;"></div>
<div style="position: absolute; bottom: -100px; right: -50px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(124,58,237,0.18) 0%, transparent 70%); border-radius: 50%; filter: blur(40px); pointer-events: none;"></div>
<div style="position: relative; z-index: 1;">
<div style="font-size: 1.4rem; font-weight: 750; margin-bottom: 2rem; letter-spacing: -0.02em; display: flex; align-items: center; gap: 10px;">
<div style="color: rgba(255,255,255,0.95) !important; filter: drop-shadow(0 2px 8px rgba(255,255,255,0.25)); font-size: 1.5rem;">✦</div> 
MeetIntel AI
</div>
<h1 style="font-size: 2.85rem; font-weight: 750; line-height: 1.15; margin-bottom: 1.25rem; letter-spacing: -0.02em;">AI-Powered<br>Meeting Intelligence</h1>
<p class="login-left-desc" style="font-size: 1.05rem; line-height: 1.6; max-width: 440px; margin-bottom: 2.5rem;">
Turn every executive conversation into searchable, accountable execution intelligence.
</p>
<div style="display: flex; align-items: center; gap: 10px; font-size: 0.88rem; font-weight: 600; letter-spacing: 0.02em; flex-wrap: wrap;">
<span class="login-pill" style="padding: 6px 12px; border-radius: 10px;">Transcript</span>
<span class="login-arrow">→</span>
<span class="login-pill" style="padding: 6px 12px; border-radius: 10px;">Insights</span>
<span class="login-arrow">→</span>
<span class="login-pill" style="padding: 6px 12px; border-radius: 10px;">Decisions</span>
<span class="login-arrow">→</span>
<span class="login-pill" style="padding: 6px 12px; border-radius: 10px;">Action Items</span>
</div>
</div>
</div>
""", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="padding: 0 4rem; max-width: 480px; margin: 0 auto;">
                <h2 style="font-size: 1.85rem; font-weight: 700; color: var(--mt-text); margin-bottom: 6px; letter-spacing: -0.02em;">Welcome back</h2>
                <p style="color: var(--mt-text-secondary); font-size: 0.92rem; margin-bottom: 24px;">Please enter your credentials to access your workspace.</p>
            </div>
        """, unsafe_allow_html=True)
        
        c_left, c_mid, c_right = st.columns([1, 4, 1])
        with c_mid:
            tab1, tab2 = st.tabs(["Login", "Create Account"])
            
            with tab1:
                with st.form("login_form", clear_on_submit=False):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    submit = st.form_submit_button("Sign in", type="primary", use_container_width=True)
                    
                    if submit:
                        username_clean = (username or "").strip()
                        if not username_clean or not password:
                            st.error("Please enter both username and password.")
                        else:
                            db = SessionLocal()
                            try:
                                user = get_user_by_username(db, username_clean)
                                if user and verify_password(password, user.hashed_password):
                                    st.session_state['user_id'] = user.id
                                    st.session_state['username'] = user.username
                                    st.session_state['user_role'] = getattr(user, 'role', 'Employee')
                                    st.session_state['org_id'] = getattr(user, 'org_id', 'org-default-001')
                                    st.session_state['theme_preference'] = getattr(user, 'theme_preference', 'System')
                                    st.session_state['current_page'] = "Dashboard"
                                    
                                    # Record successful login audit event
                                    from storage import repository
                                    repository.log_audit_event(
                                        db,
                                        org_id=user.org_id or "org-default-001",
                                        user_id=user.id,
                                        actor_username=user.username,
                                        entity_type="auth",
                                        entity_id=user.id,
                                        action="LOGIN",
                                        details=f"User '{user.username}' successfully authenticated."
                                    )
                                    st.rerun()
                                else:
                                    # Record failed login audit event
                                    from storage import repository
                                    repository.log_audit_event(
                                        db,
                                        org_id="org-default-001",
                                        user_id=None,
                                        actor_username=username_clean,
                                        entity_type="auth",
                                        entity_id="login",
                                        action="LOGIN_FAILED",
                                        details=f"Failed login attempt for username '{username_clean}'."
                                    )
                                    st.error("Invalid username or password.")
                            finally:
                                db.close()
                                
            with tab2:
                with st.form("register_form", clear_on_submit=False):
                    new_username = st.text_input("Username")
                    new_email = st.text_input("Email")
                    new_password = st.text_input("Password", type="password")
                    new_password_confirm = st.text_input("Confirm Password", type="password")
                    reg_submit = st.form_submit_button("Register", type="primary", use_container_width=True)
                    
                    if reg_submit:
                        new_username_clean = (new_username or "").strip()
                        new_email_clean = (new_email or "").strip()
                        if not new_username_clean or not new_email_clean or not new_password:
                            st.error("Please fill in all fields.")
                        elif len(new_password) < 8:
                            st.error("Password must be at least 8 characters long.")
                        elif new_password != new_password_confirm:
                            st.error("Passwords do not match.")
                        else:
                            db = SessionLocal()
                            try:
                                existing_user = get_user_by_username(db, new_username_clean)
                                if existing_user:
                                    st.error("Username already exists.")
                                else:
                                    from storage.repository import get_user_by_email
                                    existing_email = get_user_by_email(db, new_email_clean)
                                    if existing_email:
                                        st.error("An account with this email already exists.")
                                    else:
                                        user = create_user(db, new_username_clean, new_email_clean, hash_password(new_password))
                                        st.success("Registration successful! Please login.")
                            finally:
                                db.close()
                            
def logout():
    user_id = st.session_state.get('user_id')
    username = st.session_state.get('username')
    if user_id:
        db = SessionLocal()
        try:
            from storage import repository
            repository.log_audit_event(
                db,
                org_id=st.session_state.get('org_id', 'org-default-001'),
                user_id=user_id,
                actor_username=username or "User",
                entity_type="auth",
                entity_id=user_id,
                action="LOGOUT",
                details=f"User '{username}' signed out."
            )
        except Exception:
            pass
        finally:
            db.close()
    st.session_state.pop('user_id', None)
    st.session_state.pop('username', None)
    st.session_state.pop('user_role', None)
    st.session_state.pop('org_id', None)
    st.session_state.pop('theme_preference', None)
    st.session_state['current_page'] = "Login"
    st.rerun()
