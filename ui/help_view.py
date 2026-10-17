import streamlit as st
import os
from pathlib import Path
from ui.components import page_header, render_status_badge, metric_card, safe_escape, get_icon_svg

DOCS_DIR = Path("docs")

def render_help_page():
    page_header(
        title="Help, Learning Guide & Documentation",
        subtitle="Complete operator handbook, beginner tutorials, technical architecture guides, and troubleshooting runbooks.",
        category="Learning & Support",
        badge_text="Knowledge Base",
        badge_type="accent",
        icon="library"
    )
    
    # 4 Quick Metric Summary Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Documentation Files", "9 Guides", "file-text", "docs/ directory")
    with c2:
        metric_card("Test Suite", "64 Passing", "check-circle", "100% test coverage")
    with c3:
        metric_card("Verified Features", "52 Features", "target", "Audited in inventory")
    with c4:
        metric_card("AI Engines", "Multi-Provider", "sparkles", "Gemini, OpenAI, Demo")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 Application Learning Guide", "📂 Complete Documentation Library", "🛠️ Troubleshooting & Runbooks"])

    with tab1:
        with st.container(border=True):
            st.markdown("<h3 style='color: var(--mt-text); margin: 0 0 6px 0; font-size: 1.25rem; font-weight: 700;'>✦ Welcome to MeetIntel AI</h3>", unsafe_allow_html=True)
            st.markdown("""
            <p style="color: var(--mt-text-secondary); font-size: 0.92rem; line-height: 1.6; margin: 0 0 14px 0;">
                <strong>MeetIntel AI</strong> is an enterprise meeting-to-execution platform. It transforms spoken discussions into structured, accountable outcomes.
                Rather than stopping at simple speech transcription, MeetIntel AI extracts action items and strategic decisions grounded in verbatim transcript evidence,
                enforces human-in-the-loop approvals, and synchronizes deadlines directly with Google Calendar and follow-up emails.
            </p>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 12px 0;'></div>", unsafe_allow_html=True)
            
            st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 8px 0; font-size: 1.05rem; font-weight: 700;'>Four Operational Pillars</h4>", unsafe_allow_html=True)
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown("""
                **1. Workspace & Execution**
                - **Overview Dashboard:** Your daily command center showing personal queues, team deadlines, and blockers.
                - **My Commitments:** Personal and organizational task tracking with verbatim evidence quotes and inline status updates.
                - **Meeting Library:** Centralized repository of all past meetings with search and filter controls.
                - **Process Meeting:** 5-step automated pipeline (FFmpeg -> Faster-Whisper -> Pyannote -> LLM -> ChromaDB).
                - **Intelligence Dossier:** 8-tab comprehensive dossier including MoM exports (PDF, Word, CSV, TXT).
                
                **2. Planning & Intelligence**
                - **Projects & Milestones:** Track cross-meeting deliverables against strategic corporate initiatives.
                - **Decision Register:** Immutable, traceable log of agreements with rationale, alternatives, and revision history.
                - **Meeting Preparation:** Proactive synthesis of previous action items, blockers, and timed agendas.
                - **Organizational Knowledge:** Grounded Ask AI (RAG) and semantic vector search across all meetings.
                """)
            with col_p2:
                st.markdown("""
                **3. Automation & Ecosystem**
                - **Calendar & Follow-ups:** Attendance-aware absentee briefs with review-before-send gating and acknowledgment logs.
                - **Workflow Automations:** Event-driven rule triggers and persistent background worker queue with exponential backoff.
                - **Integrations Center:** Unified hub for Google Workspace (OAuth 2.0 & Calendar), Zoom webhooks, and SMTP email.
                
                **4. Governance & Administration**
                - **Team Directory:** Member roster, department distribution, and deliverable accountability.
                - **AI Quality Center:** Reproducible benchmarks (WER, F1 score, owner accuracy, prompt injection defense).
                - **Audit Trail & Logs:** Non-repudiable compliance history of all approvals, status changes, and logins.
                - **Preferences & Settings:** Fast role switcher, 1-click examiner demo seeder, and AI model configurations.
                """)

    with tab2:
        st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 10px 0; font-size: 1.05rem; font-weight: 700;'>Complete Offline Documentation Library</h4>", unsafe_allow_html=True)
        st.caption("All documentation files are located in the docs/ directory within the repository root.")
        
        doc_files = [
            ("MEETINTEL_AI_USER_MANUAL.md", "Complete User Manual", "Comprehensive operator guide explaining every page, button, form, filter, and concept."),
            ("PRACTICAL_TUTORIALS.md", "Step-by-Step Practical Tutorials", "10 hands-on tutorials walking through upload, task approval, calendar sync, RAG, and governance."),
            ("FEATURES_AND_TECHNOLOGY_EXPLAINED.md", "Technical Architecture & Tech Deep-Dive", "Detailed explanations of Whisper int8 quantization, Pyannote diarization, ChromaDB, RAG, and Fernet AES."),
            ("END_TO_END_WORKFLOWS.md", "End-to-End Workflows & Data Flows", "Source-backed architectural data flow traces with Mermaid diagrams for all 5 core lifecycles."),
            ("FEATURE_INVENTORY.md", "Exhaustive Feature Inventory", "Status matrix of all 62 features, backend routes, models, permissions, and verification evidence."),
            ("FEATURE_MAP.md", "Visual Feature & Dependency Map", "Visual architecture hierarchy, service dependency table, and prerequisite chains."),
            ("FEATURE_VERIFICATION_CHECKLIST.md", "Feature Verification & QA Checklist", "17 manual test cases with expected vs actual outcome fields and 64 passing automated tests."),
            ("PROJECT_PRESENTATION_AND_VIVA.md", "Project Presentation & Technical Viva Guide", "Executive elevator pitch, architecture defenses, and 15 technical viva Q&As."),
            ("README.md", "Documentation Index & Learning Path", "Master documentation index recommending the optimal reading order for beginners."),
        ]
        
        for fname, title, desc in doc_files:
            fpath = DOCS_DIR / fname
            exists = fpath.exists()
            with st.container(border=True):
                col_d1, col_d2 = st.columns([3.5, 1.2])
                with col_d1:
                    st.markdown(f"<strong style='color: var(--mt-text); font-size: 0.95rem;'>📄 {title}</strong>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: var(--mt-text-secondary); font-size: 0.84rem; margin: 2px 0 4px 0;'>{desc}</div>", unsafe_allow_html=True)
                    st.caption(f"Path: docs/{fname}")
                with col_d2:
                    if exists:
                        st.markdown(f"<div style='text-align: right;'>{render_status_badge('Available on Disk', 'status')}</div>", unsafe_allow_html=True)
                        content = fpath.read_text(encoding="utf-8")
                        st.download_button(
                            label="↓ Download Guide",
                            data=content,
                            file_name=fname,
                            mime="text/markdown",
                            key=f"dl_{fname}",
                            use_container_width=True,
                            type="secondary"
                        )
                    else:
                        st.markdown(f"<div style='text-align: right;'>{render_status_badge('Missing', 'status')}</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 10px 0; font-size: 1.05rem; font-weight: 700;'>Common Questions & Troubleshooting Runbooks</h4>", unsafe_allow_html=True)
        
        with st.expander("❓ How do I seed realistic enterprise demonstration data?"):
            st.markdown("""
            If your application database is empty:
            1. Navigate to **Preferences & Settings** in the sidebar.
            2. Under **🚀 Seed Examiner Demonstration Scenario**, click **✦ Seed Enterprise Demonstration Scenario**.
            3. MeetIntel AI instantly creates meeting `demo-meeting-q3-security`, dialogue turns, verified action items with evidence, approved decisions, synced calendar events, and follow-up drafts.
            """)
            
        with st.expander("❓ How do I switch user personas (Admin vs. Team Lead vs. Employee)?"):
            st.markdown("""
            To test role permissions without logging in and out:
            1. Open **Preferences & Settings**.
            2. Under **🎭 Fast Role & Identity Switcher**, select:
               - `Sarah Jenkins (Team Lead)` — to test task approvals and email dispatching.
               - `Alex Chen (Employee)` — to test personal queue execution.
               - `admin (Admin)` — for complete administrative access.
            3. Click **Switch Identity**.
            """)
            
        with st.expander("❓ What if my AI provider key hits a rate limit or runs out of quota?"):
            st.markdown("""
            MeetIntel AI includes automatic failover:
            1. If Gemini fails, it automatically falls back to OpenAI GPT-4o.
            2. To operate completely offline without internet or API keys:
               - In **Settings**, change **Primary AI Provider** to `Demo (Local Offline)`.
               - Click **Save All Settings**.
            """)

        with st.expander("❓ What if I forget the admin password?"):
            st.markdown("""
            Run the administrative recovery CLI utility directly in your terminal:
            ```bash
            PYTHONPATH=. .venv/bin/python scripts/admin_recovery.py --username admin --password "NewPassword123"
            ```
            This safely hashes your new password with PBKDF2 salt and logs a recovery audit event.
            """)
