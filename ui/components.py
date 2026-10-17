import os
import streamlit as st
import html
import textwrap
from typing import Any, Optional
from storage.database import get_db
from storage.models import ActionItem, Decision, Meeting, User, AuditEvent
from storage import repository

def safe_escape(val: Any, default: str = "") -> str:
    """
    Safely converts any value (None, int, float, bool, dict, str) into an HTML-escaped string.
    Guarantees no AttributeError when encountering NoneType or unexpected objects.
    """
    if val is None:
        return html.escape(str(default))
    return html.escape(str(val))

# ---------------------------------------------------------------------------
# Consistent Lucide-Style Line Icon SVG System
# ---------------------------------------------------------------------------
LUCIDE_ICONS = {
    "dashboard": '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
    "layout-dashboard": '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
    "check-circle": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "circle-check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "list-check": '<path d="M11 18H3"/><path d="m15 18 2 2 4-4"/><path d="M16 12H3"/><path d="M16 6H3"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/>',
    "audio-lines": '<path d="M2 10v3"/><path d="M6 6v11"/><path d="M10 3v18"/><path d="M14 8v7"/><path d="M18 5v13"/><path d="M22 10v3"/>',
    "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/>',
    "sparkles": '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "folder": '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 8 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "badge-check": '<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="m9 12 2 2 4-4"/>',
    "calendar": '<rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/>',
    "calendar-clock": '<path d="M21 7.5V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h3.5"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><circle cx="16" cy="16" r="6"/><polyline points="16 14 16 16 18 16"/>',
    "calendar-check": '<rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><path d="m9 16 2 2 4-4"/>',
    "library": '<path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/>',
    "network": '<rect width="6" height="6" x="16" y="16" rx="1"/><rect width="6" height="6" x="2" y="16" rx="1"/><rect width="6" height="6" x="9" y="2" rx="1"/><path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"/><path d="M12 12V8"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "workflow": '<rect width="8" height="8" x="3" y="3" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect width="8" height="8" x="13" y="13" rx="2"/>',
    "plug": '<path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "chart": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "trending-up": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>',
    "shield-check": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/>',
    "history": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>',
    "settings": '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "alert-triangle": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "clipboard-check": '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "check-check": '<path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "building": '<rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M8 10h.01"/><path d="M16 10h.01"/><path d="M8 14h.01"/><path d="M16 14h.01"/>',
    "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/><line x1="10" x2="8" y1="9" y2="9"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
}

def get_icon_svg(name: str, size: int = 18, color: Optional[str] = None, stroke_width: float = 2.0) -> str:
    """Returns a standalone, crisp SVG line pictogram matching Lucide icon specifications."""
    clean_name = name.lower().strip().replace(" ", "-")
    content = LUCIDE_ICONS.get(clean_name)
    if not content:
        # Fallback mappings
        if any(k in clean_name for k in ["dash", "home"]):
            content = LUCIDE_ICONS["dashboard"]
        elif any(k in clean_name for k in ["check", "commit", "done", "complete"]):
            content = LUCIDE_ICONS["check-circle"]
        elif any(k in clean_name for k in ["mic", "audio", "meet", "recording"]):
            content = LUCIDE_ICONS["mic"]
        elif any(k in clean_name for k in ["upload", "new", "process"]):
            content = LUCIDE_ICONS["upload"]
        elif any(k in clean_name for k in ["project", "target", "milestone"]):
            content = LUCIDE_ICONS["target"]
        elif any(k in clean_name for k in ["decision", "scale"]):
            content = LUCIDE_ICONS["scale"]
        elif any(k in clean_name for k in ["prep", "plan", "brief"]):
            content = LUCIDE_ICONS["calendar-clock"]
        elif any(k in clean_name for k in ["search", "knowledge", "find"]):
            content = LUCIDE_ICONS["search"]
        elif any(k in clean_name for k in ["calendar", "date", "followup", "schedule"]):
            content = LUCIDE_ICONS["calendar-check"]
        elif any(k in clean_name for k in ["auto", "rule", "zap"]):
            content = LUCIDE_ICONS["zap"]
        elif any(k in clean_name for k in ["integ", "plug", "connect"]):
            content = LUCIDE_ICONS["plug"]
        elif any(k in clean_name for k in ["team", "user", "member"]):
            content = LUCIDE_ICONS["users"]
        elif any(k in clean_name for k in ["quality", "bench", "eval", "metric", "chart"]):
            content = LUCIDE_ICONS["chart"]
        elif any(k in clean_name for k in ["audit", "log", "shield", "security"]):
            content = LUCIDE_ICONS["shield-check"]
        elif any(k in clean_name for k in ["setting", "config"]):
            content = LUCIDE_ICONS["settings"]
        elif any(k in clean_name for k in ["block", "warn", "risk", "alert"]):
            content = LUCIDE_ICONS["alert-triangle"]
        elif any(k in clean_name for k in ["pending", "time", "clock"]):
            content = LUCIDE_ICONS["clock"]
        else:
            content = LUCIDE_ICONS["sparkles"]

    color_attr = color if color else "currentColor"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color_attr}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-{safe_escape(clean_name)}" '
        f'style="vertical-align: middle; display: inline-block; flex-shrink: 0;">'
        f'{content}'
        f'</svg>'
    )

def render_status_badge(text: str, badge_type: str = "status") -> str:
    """Returns a clean, accessible HTML badge pill preserving test assertions."""
    raw_str = str(text) if text is not None else "Unknown"
    safe_text = safe_escape(raw_str)
    low = raw_str.lower()
    
    if any(k in low for k in ["complete", "approved", "synced", "live", "success", "active", "connected — live", "enterprise verified"]):
        cls = "badge-completed"
        icon = "✓ "
    elif any(k in low for k in ["in progress", "processing", "scheduled", "connecting", "underway", "sync in progress"]):
        cls = "badge-processing"
        icon = "⚡ "
    elif any(k in low for k in ["pending", "draft", "needs assignment", "review required", "needs clarification", "review-before-send"]):
        cls = "badge-pending"
        icon = "⏱ "
    elif any(k in low for k in ["blocked", "rejected", "failed", "overdue", "needs attention", "error", "cancelled", "expired", "authentication expired", "sync failed", "permission required"]):
        cls = "badge-failed"
        icon = "⚠️ "
    elif any(k in low for k in ["demo", "mock", "sandboxed", "connected — demo", "connected (demo)"]):
        cls = "badge-demo"
        icon = "🧪 "
    elif any(k in low for k in ["disconnected", "not connected", "not configured", "not linked"]):
        cls = "badge-neutral"
        icon = "○ "
    else:
        cls = "badge-neutral"
        icon = ""
        
    return f'<span class="badge {cls}">{icon}{safe_text}</span>'

def render_evidence_quote(excerpt: str, label: str = "Source Evidence (Verbatim Transcript)", source_meta: str = None):
    """Renders a verified transcript excerpt with clear styling and no heavy code boxes."""
    safe_excerpt = safe_escape(excerpt, default="Directly extracted from meeting dialogue.")
    safe_label = safe_escape(label, default="Source Evidence")
    search_icon = get_icon_svg("search", size=14, color="#6C4DFF", stroke_width=2.2)
    meta_html = f'<span style="float: right; color: var(--mt-text-secondary); font-size: 0.75rem; font-weight: normal;">Source: {safe_escape(source_meta)}</span>' if source_meta else ''
    html_box = (
        f'<div class="evidence-box">'
        f'<div class="evidence-box-title"><span style="display: inline-flex; align-items: center; gap: 5px;">{search_icon} {safe_label}</span>{meta_html}</div>'
        f'<div class="evidence-box-text">"{safe_excerpt}"</div>'
        f'</div>'
    )
    st.markdown(html_box, unsafe_allow_html=True)

def metric_card(title, value, icon, subtitle=""):
    """Renders a refined executive metric card with subtle borders, generous spacing, and a clean pictogram."""
    safe_title = safe_escape(title)
    safe_value = safe_escape(value)
    safe_subtitle = safe_escape(subtitle)
    
    # Render pictogram inside a gentle lavender-tinted background
    icon_str = str(icon or "sparkles")
    if "<svg" in icon_str:
        icon_html = icon_str
    elif any(icon_str.startswith(k) for k in ["✓", "⏱", "⚠️", "🎙", "📋", "⚡", "🎯", "👥", "🛡", "◈", "📈", "⚙"]):
        # Map common glyphs to corresponding Lucide line SVGs
        glyph_map = {
            "✓": "check-circle",
            "⏱": "clock",
            "⚠️": "alert-triangle",
            "🎙": "mic",
            "📋": "list-check",
            "⚡": "zap",
            "🎯": "target",
            "👥": "users",
            "🛡": "shield-check",
            "◈": "layout-dashboard",
            "📈": "chart",
            "⚙": "settings",
        }
        mapped_key = glyph_map.get(icon_str[0], "sparkles")
        icon_html = get_icon_svg(mapped_key, size=18, color="#6C4DFF", stroke_width=2)
    else:
        icon_html = get_icon_svg(icon_str, size=18, color="#6C4DFF", stroke_width=2)

    html_str = (
        f'<div class="metric-card">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">'
        f'<div style="font-size: 0.72rem; color: var(--mt-text-secondary); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;">{safe_title}</div>'
        f'<div style="width: 32px; height: 32px; border-radius: 8px; background: var(--mt-primary-light); color: var(--mt-primary); display: flex; align-items: center; justify-content: center; flex-shrink: 0;">{icon_html}</div>'
        f'</div>'
        f'<div style="font-size: 1.85rem; font-weight: 750; color: var(--mt-text); line-height: 1.1; margin-bottom: 4px; letter-spacing: -0.02em;">{safe_value}</div>'
        f'<div style="font-size: 0.8rem; color: var(--mt-text-secondary); line-height: 1.4;">{safe_subtitle}</div>'
        f'</div>'
    )
    st.markdown(html_str, unsafe_allow_html=True)

def render_metric_card(title, value, subtitle="", icon="dashboard"):
    """Enterprise metric card supporting title, value, subtitle, icon."""
    metric_card(title=title, value=value, icon=icon, subtitle=subtitle)

def page_header(title: str, subtitle: Optional[str] = None, category: Optional[str] = None, badge_text: Optional[str] = None, badge_type: str = "status", icon: Optional[str] = None):
    """Renders a standardized enterprise page header with clean breathing room and subtle category context."""
    title_str = str(title or "")
    cat_html = f"<div style='font-size: 0.7rem; font-weight: 700; color: var(--mt-primary); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;'>{safe_escape(category)}</div>" if category else ""
    sub_html = f'<p class="page-subtitle" style="max-width: 760px; margin: 4px 0 0 0;">{safe_escape(subtitle)}</p>' if subtitle else ''
    badge_html = f"<div style='margin-left: auto; align-self: center;'>{render_status_badge(badge_text, badge_type)}</div>" if badge_text else ""
    
    icon_html = ""
    if icon:
        icon_html = f"<span style='display: inline-flex; align-items: center; margin-right: 8px;'>{get_icon_svg(icon, size=24, color='#6C4DFF')}</span>"

    header_html = (
        f'<div class="page-title-container" style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 22px;">'
        f'<div style="flex: 1; min-width: 280px;">'
        f'{cat_html}'
        f'<h2 class="page-title">{icon_html}{safe_escape(title_str)}</h2>'
        f'{sub_html}'
        f'</div>'
        f'{badge_html}'
        f'</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

def section_header(title, subtitle=None, category=None):
    """Renders a consistent, professional section header."""
    page_header(title=title, subtitle=subtitle, category=category)

def empty_state(icon, title, description, action_label: str = None, action_key: str = None):
    """Renders an unboxed, calm, compact empty state placeholder with Lucide line icon."""
    safe_title = safe_escape(title)
    safe_desc = safe_escape(description)
    
    icon_str = str(icon or "sparkles")
    if "<svg" in icon_str:
        icon_svg = icon_str
    elif any(icon_str.startswith(k) for k in ["✓", "⏱", "⚠️", "🎙", "📋", "⚡", "🎯", "👥", "🛡", "◈", "📈", "⚙", "📁", "🎉", "🔍", "📭"]):
        glyph_map = {
            "✓": "check-circle",
            "⏱": "clock",
            "⚠️": "alert-triangle",
            "🎙": "mic",
            "📋": "list-check",
            "⚡": "zap",
            "🎯": "target",
            "👥": "users",
            "🛡": "shield-check",
            "◈": "layout-dashboard",
            "📈": "chart",
            "⚙": "settings",
            "📁": "folder",
            "🎉": "sparkles",
            "🔍": "search",
            "📭": "folder",
        }
        mapped_key = glyph_map.get(icon_str[0], "sparkles")
        icon_svg = get_icon_svg(mapped_key, size=24, color="#6C4DFF", stroke_width=2)
    else:
        icon_svg = get_icon_svg(icon_str, size=24, color="#6C4DFF", stroke_width=2)

    html_str = (
        f'<div style="text-align: center; padding: 32px 20px; background: transparent; margin: 8px 0;">'
        f'<div style="width: 48px; height: 48px; border-radius: 50%; background: var(--mt-primary-light); color: var(--mt-primary); display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto;">'
        f'{icon_svg}'
        f'</div>'
        f'<h4 style="color: var(--mt-text); font-weight: 650; font-size: 1rem; margin: 0 0 4px 0;">{safe_title}</h4>'
        f'<p style="color: var(--mt-text-secondary); font-size: 0.86rem; max-width: 440px; margin: 0 auto; line-height: 1.5;">{safe_desc}</p>'
        f'</div>'
    )
    st.markdown(html_str, unsafe_allow_html=True)
    if action_label and action_key:
        c1, c2, c3 = st.columns([2, 1.5, 2])
        with c2:
            return st.button(action_label, key=action_key, use_container_width=True, type="primary")
    return False

def error_state(title: str, message: str, retry_key: str = None):
    """Renders an enterprise error banner with optional retry button."""
    safe_title = safe_escape(title, default="Operational Notice")
    safe_msg = safe_escape(message)
    alert_icon = get_icon_svg("alert-triangle", size=18, color="#DC4C64", stroke_width=2)
    html_str = (
        f'<div style="background: var(--mt-error-bg); border: 1px solid var(--mt-error-border); border-left: 3px solid var(--mt-error); border-radius: var(--mt-radius-md); padding: 14px 18px; margin: var(--mt-space-md) 0;">'
        f'<div style="font-weight: 700; color: var(--mt-error); font-size: 0.92rem; margin-bottom: 3px; display: flex; align-items: center; gap: 6px;">{alert_icon} {safe_title}</div>'
        f'<div style="color: var(--mt-text-secondary); font-size: 0.86rem; line-height: 1.5;">{safe_msg}</div>'
        f'</div>'
    )
    st.markdown(html_str, unsafe_allow_html=True)
    if retry_key:
        return st.button("Retry", key=retry_key, type="secondary")
    return False

def render_task_card(item: ActionItem, db, current_user_id: str, user_role: str, is_blocked: bool = False, show_meeting: bool = True):
    """Renders a structured, clean task execution card without heavy nested borders."""
    cal_synced = item.calendar_event and item.calendar_event.sync_status == "Synced"
    meeting_title = item.meeting.title if (item.meeting and show_meeting) else None

    with st.container(border=True):
        # Header Row: Title & Badges
        col_title, col_badges = st.columns([3.2, 1.3])
        with col_title:
            st.markdown(f"<h3 style='margin: 0; font-size: 1.1rem; font-weight: 700; color: var(--mt-text);'>{safe_escape(item.task)}</h3>", unsafe_allow_html=True)
            if item.description:
                st.markdown(f"<p style='color: var(--mt-text-secondary); font-size: 0.88rem; margin: 4px 0 0 0; line-height: 1.45;'>{safe_escape(item.description)}</p>", unsafe_allow_html=True)
        with col_badges:
            badge_html = f"<div style='text-align: right; display: flex; gap: 6px; justify-content: flex-end;'>{render_status_badge(item.approval_status, 'approval')}{render_status_badge(item.status, 'execution')}</div>"
            st.markdown(badge_html, unsafe_allow_html=True)

        # Source Evidence Box
        render_evidence_quote(item.evidence_excerpt, "Source Evidence (Verbatim Transcript)", source_meta=meeting_title)

        # Structured Metadata Grid with subtle dividers
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        with col_m1:
            st.caption("Assignee")
            assignee_display = item.assigned_to or "Unassigned"
            if item.assignment_status == "Needs assignment":
                st.markdown(f"<span style='color: var(--mt-warning); font-weight: 600; font-size: 0.88rem;'>{safe_escape(assignee_display)}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: var(--mt-text); font-weight: 600; font-size: 0.88rem;'>{safe_escape(assignee_display)}</span>", unsafe_allow_html=True)
        with col_m2:
            st.caption("Target Deadline")
            st.markdown(f"<span style='color: var(--mt-text); font-weight: 600; font-size: 0.88rem;'>{safe_escape(item.deadline, default='TBD')}</span>", unsafe_allow_html=True)
        with col_m3:
            st.caption("Priority")
            p_color = "var(--mt-error)" if item.priority in ["High", "Urgent"] else "var(--mt-text)"
            st.markdown(f"<span style='color: {p_color}; font-weight: 600; font-size: 0.88rem;'>{safe_escape(item.priority, default='Medium')}</span>", unsafe_allow_html=True)
        with col_m4:
            st.caption("Estimated Effort")
            st.markdown(f"<span style='color: var(--mt-text); font-weight: 600; font-size: 0.88rem;'>{item.estimated_effort_hours or 2.0} hrs</span>", unsafe_allow_html=True)
        with col_m5:
            st.caption("Calendar Sync")
            if cal_synced:
                st.markdown(render_status_badge("Synced", "status"), unsafe_allow_html=True)
            else:
                st.markdown(render_status_badge("Local Task", "status"), unsafe_allow_html=True)

        if item.completion_notes:
            st.markdown(f"<div style='margin-top: 8px; padding: 6px 12px; background: var(--mt-surface-soft); border-radius: var(--mt-radius-sm); font-size: 0.85rem; color: var(--mt-text-secondary);'>📝 <strong>Progress Notes:</strong> {safe_escape(item.completion_notes)}</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        # Interactive Control Bar
        c1, c2, c3 = st.columns([1.5, 3, 1])
        with c1:
            st_opts = ["Draft", "Pending", "Approved", "Scheduled", "In Progress", "Blocked", "Completed"]
            curr_idx = st_opts.index(item.status) if item.status in st_opts else 1
            new_status = st.selectbox("Execution Status", st_opts, index=curr_idx, key=f"t_st_{item.id}", label_visibility="collapsed")
        with c2:
            new_notes = st.text_input("Notes / Blockers", placeholder="Update progress notes or blocker details...", key=f"t_not_{item.id}", label_visibility="collapsed")
        with c3:
            if st.button("Update", key=f"t_upd_{item.id}", use_container_width=True):
                repository.update_action_item_status(
                    db,
                    item.id,
                    new_status=new_status,
                    actor_user_id=current_user_id,
                    completion_notes=new_notes if new_notes else item.completion_notes
                )
                st.toast(f"Task #{item.id} updated!")
                st.rerun()

        # Team Lead / Admin Controls (Approval & Reassignment)
        if user_role in ["Admin", "Team Lead"]:
            with st.expander("🛡️ Management Actions (Sign-off & Assignment)", expanded=False):
                col_a1, col_a2, col_a3 = st.columns([1.2, 1.2, 2.5])
                with col_a1:
                    if item.approval_status != "Approved":
                        if st.button("✓ Approve Task", key=f"mgt_appr_{item.id}", type="primary", use_container_width=True):
                            repository.approve_action_item(db, item.id, approver_user_id=current_user_id)
                            from integrations.google_workspace import GoogleWorkspaceIntegration
                            gcal = GoogleWorkspaceIntegration(org_id=item.org_id)
                            curr_user = repository.get_user_by_id(db, current_user_id)
                            gcal.sync_task_to_calendar(db, task=item, user=curr_user)
                            st.toast(f"Task #{item.id} approved and synced!")
                            st.rerun()
                    else:
                        st.caption("✓ Signed off by leadership")
                with col_a2:
                    if item.approval_status != "Rejected":
                        if st.button("✕ Reject Task", key=f"mgt_rej_{item.id}", use_container_width=True):
                            repository.reject_action_item(db, item.id, approver_user_id=current_user_id, reason="Rejected in review")
                            st.toast(f"Task #{item.id} rejected.")
                            st.rerun()
                with col_a3:
                    org_users = repository.get_all_org_users(db, item.org_id or "org-default-001")
                    u_names = [u.full_name or u.username for u in org_users]
                    u_dict = {u.full_name or u.username: u for u in org_users}
                    sel_user = st.selectbox("Reassign To Member", u_names, key=f"mgt_re_{item.id}", label_visibility="collapsed")
                    if st.button("Confirm Reassignment", key=f"mgt_btn_re_{item.id}"):
                        target = u_dict.get(sel_user)
                        if target:
                            repository.reassign_action_item(db, item.id, new_assigned_user_id=target.id, actor_user_id=current_user_id)
                            st.toast(f"Task reassigned to {sel_user}!")
                            st.rerun()

        # Audit History Expander
        with st.expander("📜 Task Audit Trail & Changes", expanded=False):
            trail = repository.get_audit_trail(db, org_id=item.org_id, entity_type="task", limit=10)
            item_trail = [e for e in trail if str(e.entity_id) == str(item.id)]
            if not item_trail:
                st.caption("No specific audit entries recorded for this item yet.")
            else:
                for ev in item_trail:
                    ts = ev.timestamp.strftime("%Y-%m-%d %H:%M:%S") if ev.timestamp else "Recently"
                    st.markdown(f"<div style='font-size: 0.82rem; padding: 4px 0; border-bottom: 1px solid var(--mt-border);'><strong>[{safe_escape(ev.action)}]</strong> {safe_escape(ev.details or '')} <span style='color: var(--mt-text-secondary);'>({ts} by {safe_escape(ev.actor_username)})</span></div>", unsafe_allow_html=True)

def render_decision_card(decision: Decision, db, current_user_id: str, user_role: str, on_supersede=None):
    """Renders a structured, verified organizational decision record with subtle surfaces."""
    meeting = repository.get_meeting(db, decision.meeting_id) if decision.meeting_id else None
    meeting_title = meeting.title if meeting else "General Meeting"

    with st.container(border=True):
        col_title, col_status = st.columns([3.2, 1.2])
        with col_title:
            st.caption(f"Decision #{decision.id} • {safe_escape(meeting_title)}")
            st.markdown(f"<h3 style='margin: 0 0 6px 0; font-size: 1.15rem; font-weight: 700; color: var(--mt-text);'>{safe_escape(decision.title or decision.decision)}</h3>", unsafe_allow_html=True)
        with col_status:
            st.markdown(f"<div style='text-align: right;'>{render_status_badge(decision.status, 'status')}</div>", unsafe_allow_html=True)

        st.markdown(f"<p style='color: var(--mt-text); font-size: 0.92rem; margin: 8px 0; line-height: 1.5;'><strong>Agreement:</strong> {safe_escape(decision.decision)}</p>", unsafe_allow_html=True)

        # 2-column Rationale & Alternatives with clean light borders
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown(f"<div style='background: var(--mt-surface-soft); border-radius: var(--mt-radius-sm); padding: 10px 14px;'><div style='font-size: 0.7rem; font-weight: 700; color: var(--mt-text-secondary); text-transform: uppercase;'>Rationale & Context</div><div style='font-size: 0.86rem; color: var(--mt-text); margin-top: 3px; line-height: 1.45;'>{safe_escape(decision.rationale or decision.context or 'Consensus documented in meeting.')}</div></div>", unsafe_allow_html=True)
        with col_r2:
            st.markdown(f"<div style='background: var(--mt-surface-soft); border-radius: var(--mt-radius-sm); padding: 10px 14px;'><div style='font-size: 0.7rem; font-weight: 700; color: var(--mt-text-secondary); text-transform: uppercase;'>Alternatives Considered</div><div style='font-size: 0.86rem; color: var(--mt-text); margin-top: 3px; line-height: 1.45;'>{safe_escape(decision.alternatives or 'None recorded.')}</div></div>", unsafe_allow_html=True)

        # Verbatim Transcript Excerpt
        render_evidence_quote(decision.evidence_excerpt, "Supporting Transcript Excerpt", meeting_title)

        # Footer Metadata
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown(f"<span style='font-size: 0.82rem; color: var(--mt-text-secondary);'>Proposer: <strong style='color: var(--mt-text);'>{safe_escape(decision.proposer or 'Team')}</strong></span>", unsafe_allow_html=True)
        with col_f2:
            grounded_label = "Source Grounded (Verified Excerpt)" if decision.evidence_excerpt else "Pending Excerpt Verification"
            st.markdown(f"<div style='text-align: right;'>{render_status_badge(grounded_label, 'status')}</div>", unsafe_allow_html=True)

        # Supersede / Revision Action for Leadership
        if user_role in ["Admin", "Team Lead"] and decision.status == "Approved":
            with st.expander(f"⚙️ Supersede / Revise Decision #{decision.id}"):
                new_dec = st.text_input("New Agreement Replacing Current Decision", key=f"sup_txt_{decision.id}")
                if st.button("Confirm Revision & Mark Superseded", key=f"sup_btn_{decision.id}", type="primary"):
                    if new_dec.strip():
                        curr_user = repository.get_user_by_id(db, current_user_id)
                        new_d = Decision(
                            meeting_id=decision.meeting_id,
                            org_id=decision.org_id,
                            title=f"Revised: {new_dec[:50]}",
                            decision=new_dec,
                            context=f"Revision superseding Decision #{decision.id}",
                            rationale="Updated in organizational review.",
                            status="Approved",
                            proposer=curr_user.full_name or curr_user.username if curr_user else "Team Lead"
                        )
                        db.add(new_d)
                        db.commit()
                        db.refresh(new_d)
                        repository.supersede_decision(db, old_decision_id=decision.id, new_decision_id=new_d.id, actor_user_id=current_user_id)
                        st.toast(f"Decision #{decision.id} superseded by #{new_d.id}!")
                        st.rerun()

def render_integration_card(prov_key: str, info: dict, manager=None, db=None, current_user_id: str = None, user_role: str = "Admin"):
    """Renders a standardized, clean SaaS integration card with complete type safety."""
    raw_status = str(info.get("status") or "Not configured")
    is_demo = bool(info.get("is_demo", False))
    is_conn = "Connected" in raw_status
    
    if "expired" in raw_status.lower() or "token expired" in str(info.get("last_result", "")).lower():
        status_label = "Authentication expired"
    elif raw_status == "Needs attention":
        status_label = "Needs attention"
    elif is_demo and is_conn:
        status_label = "Connected — Demo"
    elif is_conn:
        status_label = "Connected — Live"
    elif raw_status in ["Not connected", "Disconnected", "Not configured"]:
        status_label = "Disconnected"
    else:
        status_label = raw_status

    mode_label = "Sandboxed Demo Mode" if is_demo else "Live Service"

    name_str = safe_escape(info.get("name", prov_key.replace("_", " ").title()))
    category_str = safe_escape(info.get("category", "Integration").upper())
    
    raw_acct = info.get("account_email")
    if not raw_acct:
        if status_label == "Authentication expired":
            acct_display = "Re-authentication required"
        elif not is_conn:
            acct_display = "Not linked"
        elif is_demo:
            acct_display = "demo.workspace@acmeglobal.io"
        else:
            acct_display = "Not configured"
    else:
        acct_display = str(raw_acct)
    acct_str = safe_escape(acct_display)
    
    last_sync_val = str(info.get("last_sync") or "Never")
    sync_str = safe_escape(last_sync_val)
    sync_hdr_label = "LAST SYNCHRONIZATION" if (is_conn and status_label != "Authentication expired") else "LAST RECORDED SYNC"
    
    last_res_val = str(info.get("last_result") or "No synchronization activity recorded.")
    res_str = safe_escape(last_res_val)
    
    guide_str = safe_escape(info.get("setup_guide") or "Contact your organization administrator to configure credentials.")

    with st.container(border=True):
        col_hdr, col_badge = st.columns([3, 1.5])
        with col_hdr:
            st.caption(category_str)
            st.markdown(f"<h3 style='margin: 0 0 4px 0; font-size: 1.2rem; font-weight: 700; color: var(--mt-text);'>{name_str}</h3>", unsafe_allow_html=True)
            st.markdown(f"<span style='color: var(--mt-text-secondary); font-size: 0.88rem;'>Account: <strong style='color: var(--mt-text);'>{acct_str}</strong></span>", unsafe_allow_html=True)
        with col_badge:
            badges_html = f"<div style='text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 4px;'>{render_status_badge(mode_label, 'mode')}{render_status_badge(status_label, 'status')}</div>"
            st.markdown(badges_html, unsafe_allow_html=True)

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f"<div style='background: var(--mt-surface-soft); border-radius: var(--mt-radius-sm); padding: 8px 12px;'><div style='font-size: 0.72rem; color: var(--mt-text-secondary); font-weight: 600;'>{sync_hdr_label}</div><strong style='color: var(--mt-text); font-size: 0.88rem;'>{sync_str}</strong></div>", unsafe_allow_html=True)
        with col_s2:
            st.markdown(f"<div style='background: var(--mt-surface-soft); border-radius: var(--mt-radius-sm); padding: 8px 12px;'><div style='font-size: 0.72rem; color: var(--mt-text-secondary); font-weight: 600;'>LAST SYNC RESULT & GUIDANCE</div><span style='color: var(--mt-text); font-size: 0.88rem;'>{res_str}</span></div>", unsafe_allow_html=True)

        st.markdown(f"<p style='color: var(--mt-text-secondary); font-size: 0.82rem; margin: 10px 0 12px 0; line-height: 1.4;'><strong>Setup Prerequisite:</strong> {guide_str}</p>", unsafe_allow_html=True)

        col_b1, col_b2, col_b3, col_b4 = st.columns([1.2, 1.2, 1.8, 2.5])
        with col_b1:
            if st.button("Test Connection", key=f"btn_test_{prov_key}"):
                with st.spinner(f"Verifying {info.get('name', prov_key)} connection..."):
                    res = manager.test_connection(db, prov_key)
                    if res.get("status") == "success":
                        st.success(res["message"])
                    elif res.get("status") == "info":
                        st.info(res["message"])
                    else:
                        st.error(res["message"])
        with col_b2:
            if is_conn and status_label != "Authentication expired":
                if user_role in ["Admin", "Team Lead"] and st.button("Disconnect", key=f"btn_disconn_{prov_key}"):
                    manager.disconnect(db, prov_key, user_id=current_user_id)
                    st.toast(f"{info.get('name', prov_key)} disconnected.")
                    st.rerun()
            else:
                btn_action_label = "Reconnect" if status_label == "Authentication expired" else "Connect"
                if user_role in ["Admin", "Team Lead"] and manager:
                    if prov_key in ["google_meet", "google_calendar"] and hasattr(manager, "google"):
                        if manager.google and manager.google.is_configured():
                            auth_url = manager.google.get_auth_url()
                            st.link_button("✦ Authorize Google Workspace", auth_url, type="primary", use_container_width=True)
                        else:
                            if st.button(btn_action_label, key=f"btn_conn_{prov_key}", type="primary", use_container_width=True):
                                if manager.google:
                                    manager.google.exchange_code(db, "demo_code")
                                st.toast(f"{info.get('name', prov_key)} connected in Demo Mode!")
                                st.rerun()
                    elif prov_key == "zoom" and hasattr(manager, "zoom"):
                        if st.button(btn_action_label, key=f"btn_conn_{prov_key}", type="primary", use_container_width=True):
                            if manager.zoom and manager.zoom.is_configured():
                                repository.upsert_integration_connection(
                                    db,
                                    provider="zoom",
                                    connection_status="Connected",
                                    org_id=manager.org_id,
                                    account_email=os.getenv("ZOOM_ACCOUNT_EMAIL", "active@zoom.us"),
                                    last_import_result="Live webhook listener active."
                                )
                                st.toast("Zoom live connection verified!")
                            else:
                                repository.upsert_integration_connection(
                                    db,
                                    provider="zoom",
                                    connection_status="Connected (Demo)",
                                    org_id=manager.org_id,
                                    account_email="demo.zoom@acmeglobal.io",
                                    last_import_result="Ready for webhook reception (Demo)."
                                )
                                st.toast("Zoom connected in Demo Mode!")
                            st.rerun()
                    elif prov_key == "email_smtp":
                        if st.button(btn_action_label, key=f"btn_conn_{prov_key}", type="primary", use_container_width=True):
                            if manager.email.is_configured():
                                repository.upsert_integration_connection(
                                    db,
                                    provider="email_smtp",
                                    connection_status="Connected",
                                    org_id=manager.org_id,
                                    account_email=os.getenv("SMTP_FROM", "mailer@acmeglobal.io"),
                                    last_import_result="Live SMTP server configured."
                                )
                                st.toast("SMTP live connection verified!")
                            else:
                                repository.upsert_integration_connection(
                                    db,
                                    provider="email_smtp",
                                    connection_status="Connected (Demo)",
                                    org_id=manager.org_id,
                                    account_email="demo.mailer@acmeglobal.io",
                                    last_import_result="Ready for simulated email delivery."
                                )
                                st.toast("Email service connected in Demo Mode!")
                            st.rerun()
        with col_b3:
            if prov_key == "google_meet":
                if st.button("Discover Drive Artifacts", key="btn_disc_gmeet"):
                    discovered = manager.google.discover_and_import_artifacts(db, user_id=current_user_id)
                    st.toast(f"Discovered {len(discovered)} ready artifacts in Google Workspace!")
                    for item in discovered:
                        st.info(f"📁 {safe_escape(item.get('title'))} ({safe_escape(item.get('date'))}) — {safe_escape(item.get('file_type'))} [{safe_escape(item.get('status'))}]")
            elif prov_key == "google_calendar":
                if st.button("Sync Pending Deadlines", key="btn_sync_gcal"):
                    with st.spinner("Syncing approved action items to calendar..."):
                        synced_count = manager.google.sync_all_approved_tasks(db)
                        st.toast(f"Synchronized {synced_count} pending deadlines to Google Calendar!")
                        st.rerun()

def render_meeting_card(meeting, button_key, button_label="View Dossier →"):
    """Renders a structured, modern enterprise meeting dossier preview card with clean pictogram and metadata."""
    raw_source = getattr(meeting, 'source_platform', 'upload') or 'upload'
    source_lower = str(raw_source).lower()
    source_label = "Google Meet" if "meet" in source_lower else "Zoom" if "zoom" in source_lower else "Audio Upload"
    source_icon_name = "calendar" if "meet" in source_lower else "sparkles" if "zoom" in source_lower else "mic"
    
    duration_str = f"{int(meeting.duration)//60}m {int(meeting.duration)%60}s" if meeting.duration else "N/A"
    summary = meeting.executive_summary if meeting.executive_summary else 'No summary generated yet.'
    meeting_date_str = meeting.date.strftime('%B %d, %Y') if meeting.date else 'Recent Session'
    
    icon_svg = get_icon_svg(source_icon_name, size=20, color="#6C4DFF")
    clock_svg = get_icon_svg("clock", size=14, color="#73809A")
    users_svg = get_icon_svg("users", size=14, color="#73809A")
    
    with st.container(border=True):
        col_content, col_actions = st.columns([3.8, 1.4])
        with col_content:
            st.markdown(
                f"<div style='display: flex; align-items: center; gap: 6px; margin-bottom: 4px;'>"
                f"<span style='color: var(--mt-primary); font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;'>{source_label}</span>"
                f"<span style='color: var(--mt-border);'>•</span>"
                f"<span style='color: var(--mt-text-secondary); font-size: 0.72rem; font-weight: 500;'>{meeting_date_str}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            st.markdown(f"<h3 style='margin: 0 0 6px 0; font-size: 1.15rem; color: var(--mt-text); font-weight: 700; letter-spacing: -0.015em;'>{safe_escape(meeting.title)}</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='color: var(--mt-text-secondary); font-size: 0.88rem; line-height: 1.5; margin-bottom: 8px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;'>{safe_escape(summary)}</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div style='display: flex; align-items: center; gap: 14px; font-size: 0.78rem; color: var(--mt-text-secondary); font-weight: 500;'>"
                f"<span style='display: inline-flex; align-items: center; gap: 4px;'>{clock_svg} {duration_str}</span>"
                f"<span style='display: inline-flex; align-items: center; gap: 4px;'>{users_svg} {meeting.speaker_count or 0} Participants</span>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col_actions:
            st.markdown(f"<div style='text-align: right; margin-bottom: 12px;'>{render_status_badge(meeting.processing_status, 'status')}</div>", unsafe_allow_html=True)
            if st.button(button_label, key=button_key, use_container_width=True, type="primary"):
                st.session_state['current_meeting_id'] = meeting.id
                st.session_state['current_page'] = "Meeting Results"
                st.rerun()

def transcript_message(speaker, timestamp, text):
    speaker_str = str(speaker or "Speaker")
    speaker_num = hash(speaker_str) % 4 + 1
    color_class = f"transcript-msg-speaker0{speaker_num}"
    html_msg = (
        f'<div class="transcript-msg {color_class}">'
        f'<div class="transcript-header">'
        f'<span class="speaker-name">{safe_escape(speaker_str)}</span>'
        f'<span class="timestamp">{safe_escape(timestamp)}</span>'
        f'</div>'
        f'<div class="transcript-text">{safe_escape(text)}</div>'
        f'</div>'
    )
    st.markdown(html_msg, unsafe_allow_html=True)
