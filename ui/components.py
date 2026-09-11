import streamlit as st

def metric_card(title, value, icon, subtitle=""):
    html = f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: var(--space-xs);">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_meeting_card(meeting, button_key, button_label="View Results →"):
    status_lower = meeting.processing_status.lower()
    badge_class = "badge-completed" if "complete" in status_lower else "badge-processing" if "process" in status_lower else "badge-pending"
    badge_icon = "✓" if "complete" in status_lower else "●"
    duration_str = f"{int(meeting.duration)//60}m {int(meeting.duration)%60}s"
    summary = meeting.executive_summary if meeting.executive_summary else 'No summary available.'
    
    with st.container():
        # Inject CSS to style this specific container
        st.markdown(f"""
            <div class="meeting-card-marker-{meeting.id}"></div>
            <style>
            div[data-testid="stVerticalBlock"]:has(.meeting-card-marker-{meeting.id}):not(:has(div[data-testid="stVerticalBlock"]:has(.meeting-card-marker-{meeting.id}))) {{
                background: var(--surface) !important;
                border-radius: 20px !important;
                padding: 1.5rem !important;
                box-shadow: var(--shadow-soft) !important;
                border: 1px solid #E2E8F0 !important;
                margin-bottom: 1rem !important;
                transition: transform 0.2s ease, box-shadow 0.2s ease !important;
            }}
            div[data-testid="stVerticalBlock"]:has(.meeting-card-marker-{meeting.id}):not(:has(div[data-testid="stVerticalBlock"]:has(.meeting-card-marker-{meeting.id}))):hover {{
                box-shadow: var(--shadow-hover) !important;
                transform: translateY(-1px) !important;
            }}
            /* Hide the marker */
            .meeting-card-marker-{meeting.id} {{
                display: none;
            }}
            </style>
        """, unsafe_allow_html=True)
        
        col_icon, col_content, col_actions = st.columns([1, 8, 3])
        
        with col_icon:
            st.markdown("<div style='font-size: 2.5rem; line-height: 1; margin-top: 0.25rem;'>🎵</div>", unsafe_allow_html=True)
            
        with col_content:
            st.markdown(f"<h3 style='margin: 0 0 0.25rem 0; font-size: 1.15rem; color: var(--text-main); font-weight: 600;'>{meeting.title}</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.5rem;'>{meeting.date.strftime('%Y-%m-%d %H:%M')} • {duration_str} • {meeting.speaker_count} speakers</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='color: var(--text-muted); font-size: 0.9rem; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;'>{summary}</div>", unsafe_allow_html=True)
            
        with col_actions:
            st.markdown(f"<div style='text-align: right; margin-bottom: 0.75rem;'><span class='badge {badge_class}'>{badge_icon} {meeting.processing_status}</span></div>", unsafe_allow_html=True)
            if st.button(button_label, key=button_key, type="primary", use_container_width=True):
                st.session_state['current_meeting_id'] = meeting.id
                st.session_state['current_page'] = "Meeting Results"
                st.rerun()

def transcript_message(speaker, timestamp, text):
    speaker_num = hash(speaker) % 4 + 1
    color_class = f"transcript-msg-speaker0{speaker_num}"
    
    html = f"""
    <div class="transcript-msg {color_class}">
        <div class="transcript-header">
            <span class="speaker-name">{speaker}</span>
            <span class="timestamp">{timestamp}</span>
        </div>
        <div class="transcript-text">{text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def section_header(title, subtitle=None):
    # Check if title has emoji
    icon = ""
    text_title = title
    if len(title) > 0 and ord(title[0]) > 1000:
        icon = title[0]
        text_title = title[1:].strip()
        
    icon_html = f"<span style='margin-right: var(--space-xs);'>{icon}</span>" if icon else ""
        
    html = f"""
    <div class="page-title-container">
        <h2 class="page-title">{icon_html}{text_title}</h2>
        {f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def empty_state(icon, title, description):
    html = f"""
    <div style="text-align: center; padding: var(--space-2xl) var(--space-lg); background: rgba(255,255,255,0.4); border-radius: 20px; border: 2px dashed #CBD5E1; margin: var(--space-xl) 0;">
        <div style="font-size: 3rem; margin-bottom: var(--space-sm);">{icon}</div>
        <h4 style="color: var(--text-main); font-weight: 600; margin-bottom: var(--space-xs);">{title}</h4>
        <p style="color: var(--text-muted); font-size: 0.95rem; max-width: 400px; margin: 0 auto;">{description}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
