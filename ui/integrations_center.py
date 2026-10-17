import streamlit as st
from storage.database import SessionLocal
from storage import repository
from integrations.manager import IntegrationCenterManager
from ui.components import page_header, render_integration_card, render_status_badge, get_icon_svg

def render_integrations_page():
    page_header(
        title="Enterprise Integration Center",
        subtitle="Manage verified SaaS connectors for meeting sources, calendar reminders, and notification workflows.",
        category="Automation & Ecosystem",
        badge_text="Tenant Isolated",
        badge_type="accent",
        icon="plug"
    )
    
    db = SessionLocal()
    try:
        current_user_id = st.session_state.get('user_id')
        current_user = repository.get_user_by_id(db, current_user_id) if current_user_id else None
        user_role = current_user.role if current_user else "Employee"
        org_id = current_user.org_id if current_user else "org-default-001"

        manager = IntegrationCenterManager(org_id=org_id)
        statuses = manager.get_all_integration_statuses(db)

        with st.container(border=True):
            col_pol1, col_pol2 = st.columns([3.5, 1.3])
            with col_pol1:
                st.markdown("<strong style='color: var(--mt-text); font-size: 1.05rem;'>Active Integration Architecture: Multi-Mode Resilience</strong>", unsafe_allow_html=True)
                st.markdown("<p style='color: var(--mt-text-secondary); margin: 3px 0 0 0; font-size: 0.88rem;'>Enterprise tier support for Verified Live OAuth 2.0, Secure Manual Ingestion fallback, and Sandboxed Demo / Examiner Mode.</p>", unsafe_allow_html=True)
            with col_pol2:
                st.markdown(f"<div style='text-align: right;'>{render_status_badge('Enterprise Verified', 'status')}</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        for prov_key, info in statuses.items():
            render_integration_card(prov_key, info, manager, db, current_user_id, user_role)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            shield_icon = get_icon_svg("shield-check", size=20, color="#6C4DFF")
            st.markdown(f"<h4 style='margin: 0 0 8px 0; color: var(--mt-text); font-size: 1.05rem; font-weight: 700; display: flex; align-items: center; gap: 8px;'>{shield_icon} Security, Privacy & Token Protection Architecture</h4>", unsafe_allow_html=True)
            st.markdown("""
            <p style="color: var(--mt-text-secondary); font-size: 0.88rem; line-height: 1.6; margin: 0;">
                MeetIntel AI enforces strict organization tenant isolation across all third-party integrations.
                OAuth client tokens, refresh tokens, and webhook secrets are encrypted at rest using 32-byte Fernet AES cryptography.
                Secrets are never exposed in user-facing client views, browser local storage, or application audit logs.
            </p>
            """, unsafe_allow_html=True)
    finally:
        db.close()
