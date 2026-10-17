import streamlit as st
import datetime
import json
from storage.database import SessionLocal
from storage.models import Meeting, ActionItem, Decision, User
from storage import repository
from ui.components import page_header, empty_state, render_status_badge, safe_escape, get_icon_svg

def render_meeting_prep_page():
    page_header(
        title="Pre-Meeting Intelligence & Briefing",
        subtitle="Prepare for upcoming meetings with historical context, unresolved blockers, and evidence-grounded agendas.",
        category="Planning & Preparation",
        badge_text="Proactive Briefing",
        badge_type="accent",
        icon="calendar-clock"
    )
    
    db = SessionLocal()
    try:
        current_user_id = st.session_state.get('user_id')
        current_user = repository.get_user_by_id(db, current_user_id) if current_user_id else None
        org_id = current_user.org_id if current_user else "org-default-001"

        meetings = repository.get_all_meetings(db, org_id=org_id)
        if not meetings:
            empty_state("calendar-clock", "No historical meetings found", "Upload or sync at least one meeting to generate preparation briefs.")
            return

        meeting_titles = [f"{m.title} ({m.date.strftime('%Y-%m-%d') if m.date else 'Recent'})" for m in meetings]
        meeting_by_title = {f"{m.title} ({m.date.strftime('%Y-%m-%d') if m.date else 'Recent'})": m for m in meetings}

        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 4px 0; color: var(--mt-text); font-weight: 700; font-size: 1.1rem;'>Select Context for Upcoming Meeting</h4>", unsafe_allow_html=True)
            st.markdown("<p style='color: var(--mt-text-secondary); font-size: 0.88rem; margin-bottom: 14px;'>MeetIntel AI synthesizes past commitments, decisions, and open blockers into an executive briefing.</p>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                selected_ref = st.selectbox("Baseline Previous Meeting", meeting_titles)
                target_meeting = meeting_by_title.get(selected_ref)
            with col2:
                upcoming_topic = st.text_input("Upcoming Session Goal", value="Sprint Execution & Security Readiness Review")

            if st.button("✦ Generate Preparation Brief", type="primary"):
                with st.spinner("Synthesizing historical outcomes and unresolved commitments..."):
                    outstanding_tasks = db.query(ActionItem).filter(
                        ActionItem.org_id == org_id,
                        ActionItem.status.in_(["Approved", "In Progress", "Blocked"])
                    ).limit(5).all()

                    unresolved_decisions = db.query(Decision).filter(
                        Decision.org_id == org_id,
                        Decision.status == "Proposed"
                    ).all()

                    blockers = [t for t in outstanding_tasks if t.status == "Blocked"]

                    st.session_state['generated_prep_brief'] = {
                        "baseline_meeting": target_meeting.title,
                        "target_date": datetime.date.today().strftime('%B %d, %Y'),
                        "upcoming_goal": upcoming_topic,
                        "summary": target_meeting.executive_summary or "The team reviewed key sprint deliverables.",
                        "outstanding_tasks": [f"{t.task} (Owner: {t.assigned_to}, Deadline: {t.deadline})" for t in outstanding_tasks],
                        "blockers": [f"⚠️ {b.task} is BLOCKED (Dependency pending)" for b in blockers] if blockers else ["No active blockers detected."],
                        "decisions": [f"• {d.decision}" for d in target_meeting.decisions[:3]] if target_meeting.decisions else ["No prior decisions logged."],
                        "suggested_agenda": [
                            "1. Review of previous action item progress and deliverables (10 min)",
                            "2. Deep dive into blocker resolutions and dependency risks (15 min)",
                            "3. Decision confirmation on planned release milestones (15 min)",
                            "4. Assignment of accountable follow-ups and next deadlines (10 min)"
                        ],
                        "discussion_points": [
                            f"Check-in on {outstanding_tasks[0].task if outstanding_tasks else 'API readiness'}",
                            "Assess whether external integration dependencies impact rollout",
                            "Confirm attendance and follow-up ownership for absent members"
                        ]
                    }

        if 'generated_prep_brief' in st.session_state:
            brief = st.session_state['generated_prep_brief']
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                col_b_h1, col_b_h2 = st.columns([3.2, 1.3])
                with col_b_h1:
                    st.caption("EXECUTIVE MEETING PREPARATION BRIEF")
                    st.markdown(f"<h2 style='margin: 0; font-size: 1.4rem; font-weight: 750; color: var(--mt-text);'>{safe_escape(brief['upcoming_goal'])}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color: var(--mt-text-secondary); margin: 4px 0 0 0; font-size: 0.88rem;'>Target Date: {safe_escape(brief['target_date'])} • Baseline: {safe_escape(brief['baseline_meeting'])}</p>", unsafe_allow_html=True)
                with col_b_h2:
                    st.markdown(f"<div style='text-align: right;'>{render_status_badge('AI Grounded Brief', 'status')}</div>", unsafe_allow_html=True)

                st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

                st.markdown("<h4 style='color: var(--mt-text); margin-bottom: 4px; font-weight: 700; font-size: 1rem;'>1. Previous Session Synthesis</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: var(--mt-text-secondary); line-height: 1.6; font-size: 0.9rem; margin-bottom: 14px;'>{safe_escape(brief['summary'])}</p>", unsafe_allow_html=True)

                st.markdown("<h4 style='color: var(--mt-text); margin: 14px 0 6px 0; font-weight: 700; font-size: 1rem;'>2. Known Blockers & Risk Items</h4>", unsafe_allow_html=True)
                blockers_html = "".join([f"<div style='color: var(--mt-error); font-weight: 550; font-size: 0.88rem; padding: 2px 0;'>{safe_escape(blk)}</div>" for blk in brief['blockers']])
                st.markdown(f"<div style='background: var(--mt-error-bg); border-left: 3px solid var(--mt-error); padding: 10px 14px; border-radius: var(--mt-radius-sm); margin-bottom: 14px;'>{blockers_html}</div>", unsafe_allow_html=True)

                st.markdown("<h4 style='color: var(--mt-text); margin: 14px 0 6px 0; font-weight: 700; font-size: 1rem;'>3. Outstanding Action Items from Previous Sessions</h4>", unsafe_allow_html=True)
                for task in brief['outstanding_tasks']:
                    st.markdown(f"<div style='padding: 4px 0; font-size: 0.88rem; color: var(--mt-text); border-bottom: 1px solid var(--mt-border);'>• {safe_escape(task)}</div>", unsafe_allow_html=True)

                st.markdown("<h4 style='color: var(--mt-text); margin: 16px 0 6px 0; font-weight: 700; font-size: 1rem;'>4. Suggested Agenda</h4>", unsafe_allow_html=True)
                for item in brief['suggested_agenda']:
                    st.markdown(f"<div style='padding: 3px 0; font-size: 0.88rem; color: var(--mt-text-secondary);'>{safe_escape(item)}</div>", unsafe_allow_html=True)

                st.markdown("<h4 style='color: var(--mt-text); margin: 16px 0 6px 0; font-weight: 700; font-size: 1rem;'>5. Recommended Discussion Points</h4>", unsafe_allow_html=True)
                for point in brief['discussion_points']:
                    st.markdown(f"<div style='padding: 3px 0; font-size: 0.88rem; color: var(--mt-text-secondary);'>• {safe_escape(point)}</div>", unsafe_allow_html=True)
    finally:
        db.close()
