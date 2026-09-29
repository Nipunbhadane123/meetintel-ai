import streamlit as st

def metric_card(title, value, icon, subtitle=""):
    html = f"""
    <div class="metric-card" style="background: var(--mt-surface); border: 1px solid var(--mt-border); border-radius: var(--mt-radius-lg); padding: var(--mt-space-lg); box-shadow: var(--mt-shadow-soft);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: var(--mt-space-md);">
            <div style="font-size: 0.85rem; color: var(--mt-text-muted); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;">{title}</div>
            <div style="font-size: 1.25rem; color: var(--mt-primary); background: rgba(109, 61, 245, 0.08); width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: 8px;">{icon}</div>
        </div>
        <div style="font-size: 2rem; font-weight: 700; color: var(--mt-text); line-height: 1.1; margin-bottom: var(--mt-space-xs);">{value}</div>
        <div style="font-size: 0.8rem; color: var(--mt-text-muted);">{subtitle}</div>
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
                background: var(--mt-surface) !important;
                border-radius: var(--mt-radius-lg) !important;
                padding: var(--mt-space-lg) !important;
                box-shadow: var(--mt-shadow-soft) !important;
                border: 1px solid var(--mt-border) !important;
                margin-bottom: var(--mt-space-md) !important;
                transition: var(--mt-transition) !important;
            }}
            div[data-testid="stVerticalBlock"]:has(.meeting-card-marker-{meeting.id}):not(:has(div[data-testid="stVerticalBlock"]:has(.meeting-card-marker-{meeting.id}))):hover {{
                box-shadow: var(--mt-shadow-hover) !important;
                border-color: rgba(109, 61, 245, 0.3) !important;
                transform: translateY(-2px) !important;
            }}
            .meeting-card-marker-{meeting.id} {{
                display: none;
            }}
            </style>
        """, unsafe_allow_html=True)
        
        col_icon, col_content, col_actions = st.columns([0.5, 8, 2.5])
        
        with col_icon:
            st.markdown("<div style='font-size: 1.5rem; line-height: 1; margin-top: 0.25rem; color: var(--mt-primary);'>◈</div>", unsafe_allow_html=True)
            
        with col_content:
            st.markdown(f"<h3 style='margin: 0 0 6px 0; font-size: 1.1rem; color: var(--mt-text); font-weight: 600;'>{meeting.title}</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='color: var(--mt-text-muted); font-size: 0.8rem; margin-bottom: 8px;'>{meeting.date.strftime('%Y-%m-%d')} • {duration_str} • {meeting.speaker_count} speakers</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='color: var(--mt-text-secondary); font-size: 0.85rem; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;'>{summary}</div>", unsafe_allow_html=True)
            
        with col_actions:
            st.markdown(f"<div style='text-align: right; margin-bottom: var(--mt-space-md);'><span class='badge {badge_class}'>{badge_icon} {meeting.processing_status}</span></div>", unsafe_allow_html=True)
            if st.button(button_label, key=button_key, use_container_width=True):
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
        
    icon_html = f"<span style='margin-right: var(--mt-space-xs); color: var(--mt-primary);'>{icon}</span>" if icon else ""
        
    html = f"""
    <div class="page-title-container">
        <h2 class="page-title">{icon_html}{text_title}</h2>
        {f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def empty_state(icon, title, description):
    html = f"""
    <div style="text-align: center; padding: var(--mt-space-2xl) var(--mt-space-lg); background: var(--mt-surface-soft); border-radius: var(--mt-radius-xl); border: 1px dashed rgba(16,24,40,0.15); margin: var(--mt-space-xl) 0;">
        <div style="font-size: 3rem; margin-bottom: var(--mt-space-sm);">{icon}</div>
        <h4 style="color: var(--mt-text); font-weight: 600; margin-bottom: var(--mt-space-xs);">{title}</h4>
        <p style="color: var(--mt-text-secondary); font-size: 0.95rem; max-width: 400px; margin: 0 auto;">{description}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
