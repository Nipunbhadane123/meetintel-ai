import streamlit as st

def apply_global_styles():
    theme = st.session_state.get('theme_preference', 'System')
    
    # ---------------------------------------------------------------------------
    # Centralized Design Tokens (Enterprise SaaS Violet/Lavender Identity)
    # ---------------------------------------------------------------------------
    light_vars = """
            --mt-primary: #6C4DFF;
            --mt-primary-dark: #5536E8;
            --mt-primary-light: #F0ECFF;
            --mt-primary-subtle: rgba(108, 77, 255, 0.08);
            --mt-secondary: #7C3AED;
            --mt-accent: #F0ECFF;
            --mt-cyan: #06B6D4;
            
            --mt-bg: #F7F8FC; 
            --mt-surface: #FFFFFF;
            --mt-surface-soft: #F1F4F9;
            --mt-surface-hover: #F8FAFD;
            
            --mt-text: #172033;
            --mt-text-secondary: #73809A;
            --mt-text-muted: #94A3B8;
            
            --mt-border: #E9ECF4;
            --mt-border-light: #F1F4F9;
            --mt-border-focus: #6C4DFF;
            
            --mt-success: #169B69;
            --mt-success-bg: rgba(22, 155, 105, 0.08);
            --mt-success-border: rgba(22, 155, 105, 0.22);
            
            --mt-warning: #D98A16;
            --mt-warning-bg: rgba(217, 138, 22, 0.08);
            --mt-warning-border: rgba(217, 138, 22, 0.22);
            
            --mt-error: #DC4C64;
            --mt-error-bg: rgba(220, 76, 100, 0.08);
            --mt-error-border: rgba(220, 76, 100, 0.22);
            
            --mt-info: #2563EB;
            --mt-info-bg: rgba(37, 99, 235, 0.08);
            --mt-info-border: rgba(37, 99, 235, 0.22);
            
            --mt-grad-primary: linear-gradient(135deg, #6C4DFF 0%, #5536E8 100%);
            --mt-grad-subtle: linear-gradient(90deg, rgba(108, 77, 255, 0.08), rgba(108, 77, 255, 0.02));
            --mt-grad-bg: none;
            
            --mt-shadow-soft: 0 1px 3px rgba(23, 32, 51, 0.03);
            --mt-shadow-card: 0 1px 3px rgba(23, 32, 51, 0.02);
            --mt-shadow-hover: 0 4px 12px rgba(108, 77, 255, 0.06);
            --mt-shadow-dropdown: 0 8px 24px -4px rgba(23, 32, 51, 0.08);
            
            --mt-input-bg: #FFFFFF;
            --mt-input-focus-bg: #FFFFFF;
    """
    
    # ---------------------------------------------------------------------------
    # Dark Theme Variables (Preserved & Refined)
    # ---------------------------------------------------------------------------
    dark_vars = """
            --mt-primary: #856EFF;
            --mt-primary-dark: #6C4DFF;
            --mt-primary-light: rgba(108, 77, 255, 0.16);
            --mt-primary-subtle: rgba(133, 110, 255, 0.12);
            --mt-secondary: #A78BFA;
            --mt-accent: #1E1B4B;
            --mt-cyan: #22D3EE;
            
            --mt-bg: #0D111D; 
            --mt-surface: #161D2E;
            --mt-surface-soft: #1C253B;
            --mt-surface-hover: #202B44;
            
            --mt-text: #F1F5F9;
            --mt-text-secondary: #94A3B8;
            --mt-text-muted: #64748B;
            
            --mt-border: #232D42;
            --mt-border-light: rgba(241, 245, 249, 0.06);
            --mt-border-focus: #856EFF;
            
            --mt-success: #22C55E;
            --mt-success-bg: rgba(34, 197, 94, 0.12);
            --mt-success-border: rgba(34, 197, 94, 0.28);
            
            --mt-warning: #F59E0B;
            --mt-warning-bg: rgba(245, 158, 11, 0.12);
            --mt-warning-border: rgba(245, 158, 11, 0.28);
            
            --mt-error: #EF4444;
            --mt-error-bg: rgba(239, 68, 68, 0.12);
            --mt-error-border: rgba(239, 68, 68, 0.28);
            
            --mt-info: #3B82F6;
            --mt-info-bg: rgba(59, 130, 246, 0.12);
            --mt-info-border: rgba(59, 130, 246, 0.28);
            
            --mt-grad-primary: linear-gradient(135deg, #856EFF 0%, #6C4DFF 100%);
            --mt-grad-subtle: linear-gradient(90deg, rgba(133, 110, 255, 0.15), rgba(133, 110, 255, 0.04));
            --mt-grad-bg: none;
            
            --mt-shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.3);
            --mt-shadow-card: 0 2px 8px rgba(0, 0, 0, 0.25);
            --mt-shadow-hover: 0 8px 24px rgba(0, 0, 0, 0.4);
            --mt-shadow-dropdown: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            
            --mt-input-bg: #111726;
            --mt-input-focus-bg: #161D2E;
    """
    
    # Determine the active CSS variables
    if theme == "Dark":
        active_vars = f":root {{ {dark_vars} }}"
    elif theme == "Light":
        active_vars = f":root {{ {light_vars} }}"
    else:
        # System: Default to Light, override with Dark if prefers-color-scheme is dark
        active_vars = f":root {{ {light_vars} }}\n@media (prefers-color-scheme: dark) {{\n  :root {{ {dark_vars} }}\n}}"
        
    dynamic_css = f"<style>\n{active_vars}\n</style>"
    st.markdown(dynamic_css, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        :root {
            /* Map Custom Tokens to Streamlit Native Variables */
            --primary-color: var(--mt-primary) !important;
            --background-color: var(--mt-bg) !important;
            --secondary-background-color: var(--mt-surface) !important;
            --text-color: var(--mt-text) !important;
            --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            
            /* 4px/8px Incremental Spacing Scale */
            --mt-space-2xs: 4px;
            --mt-space-xs: 8px;
            --mt-space-sm: 12px;
            --mt-space-md: 16px;
            --mt-space-lg: 20px;
            --mt-space-xl: 24px;
            --mt-space-2xl: 32px;
            --mt-space-3xl: 48px;
            
            /* Restrained Border Radii */
            --mt-radius-xs: 4px;
            --mt-radius-sm: 6px;
            --mt-radius-md: 8px;
            --mt-radius-lg: 12px;
            --mt-radius-xl: 14px;
            --mt-radius-pill: 9999px;
            
            /* Transitions */
            --mt-transition: all 160ms cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Clean System Font Stack */
        html, body, [class*="css"], .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown span {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            color: var(--mt-text) !important;
            -webkit-font-smoothing: antialiased;
            text-rendering: optimizeLegibility;
        }

        /* Application Background & Viewport */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: var(--mt-bg) !important;
            background-image: none !important;
        }
        
        /* Unified Central App Container */
        .block-container {
            max-width: 1240px !important;
            padding-top: var(--mt-space-xl) !important;
            padding-bottom: var(--mt-space-3xl) !important;
            padding-left: var(--mt-space-xl) !important;
            padding-right: var(--mt-space-xl) !important;
            margin: 0 auto;
        }

        /* ---------------------------------------------------------------------------
           Sidebar Enterprise Styling
           --------------------------------------------------------------------------- */
        [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
            background-color: var(--mt-surface) !important;
            background-image: none !important;
            border-right: 1px solid var(--mt-border) !important;
            box-shadow: none !important;
        }
        
        [data-testid="stSidebarNav"] {
            display: none !important; /* Hide default nav */
        }
        
        .sidebar-logo-container {
            padding: var(--mt-space-md) var(--mt-space-md) var(--mt-space-sm) var(--mt-space-md);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .sidebar-logo-icon {
            font-size: 20px;
            color: var(--mt-primary);
            font-weight: 700;
            line-height: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            background: var(--mt-primary-light);
            border-radius: var(--mt-radius-md);
        }
        .sidebar-logo-text {
            display: flex;
            flex-direction: column;
        }
        .sidebar-logo-title {
            font-size: 1.05rem;
            font-weight: 750;
            color: var(--mt-text);
            margin: 0;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }
        .sidebar-logo-subtitle {
            font-size: 0.72rem;
            color: var(--mt-text-secondary);
            font-weight: 500;
            margin: 0;
            letter-spacing: 0.01em;
        }

        /* Sidebar Section Header */
        .sidebar-section-header {
            font-size: 0.68rem;
            font-weight: 700;
            color: var(--mt-text-secondary);
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 12px 14px 4px 14px;
            margin-top: 4px;
        }

        /* Sidebar Buttons */
        [data-testid="stSidebar"] div.stButton > button {
            border-radius: var(--mt-radius-md) !important;
            font-weight: 500 !important;
            font-size: 0.86rem !important;
            transition: var(--mt-transition) !important;
            padding: 6px 12px !important;
            min-height: 36px !important;
            height: 36px !important;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            background: transparent !important;
            color: var(--mt-text-secondary) !important;
            width: calc(100% - 16px) !important;
            margin: 1px 8px !important;
            text-align: left !important;
            white-space: nowrap !important;
        }
        /* Sidebar Hover */
        [data-testid="stSidebar"] div.stButton > button:hover {
            background: var(--mt-surface-soft) !important;
            color: var(--mt-text) !important;
            border-color: transparent !important;
        }
        /* Sidebar Active Page Button */
        [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
            background: var(--mt-primary-light) !important;
            color: var(--mt-primary) !important;
            font-weight: 650 !important;
            border: 1px solid rgba(108, 77, 255, 0.18) !important;
            border-left: 3px solid var(--mt-primary) !important;
        }
        [data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
            background: var(--mt-primary-light) !important;
            color: var(--mt-primary-dark) !important;
        }

        /* ---------------------------------------------------------------------------
           Button Architecture (Primary, Secondary, Small)
           --------------------------------------------------------------------------- */
        div[data-testid="stFormSubmitButton"] > button,
        div.stButton > button {
            border-radius: var(--mt-radius-md) !important;
            font-weight: 550 !important;
            font-size: 0.88rem !important;
            transition: var(--mt-transition) !important;
            padding: 0 16px !important;
            min-height: 38px !important;
            height: 38px !important;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--mt-border) !important;
            background: var(--mt-surface) !important;
            color: var(--mt-text) !important;
            box-shadow: 0 1px 2px rgba(23, 32, 51, 0.03) !important;
        }
        div[data-testid="stFormSubmitButton"] > button:hover,
        div.stButton > button:hover {
            background: var(--mt-surface-hover) !important;
            border-color: rgba(108, 77, 255, 0.28) !important;
            color: var(--mt-primary) !important;
            box-shadow: 0 2px 6px rgba(23, 32, 51, 0.05) !important;
        }
        div[data-testid="stFormSubmitButton"] > button:active,
        div.stButton > button:active {
            transform: translateY(1px) !important;
        }
        
        /* Primary Button */
        div[data-testid="stFormSubmitButton"] > button[kind="primary"],
        div[data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"],
        div.stButton > button[kind="primary"] {
            background: var(--mt-primary) !important;
            color: #FFFFFF !important;
            border: 1px solid var(--mt-primary-dark) !important;
            box-shadow: 0 1px 3px rgba(108, 77, 255, 0.25) !important;
            font-weight: 600 !important;
        }
        div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"]:hover,
        div.stButton > button[kind="primary"]:hover {
            background: var(--mt-primary-dark) !important;
            border-color: var(--mt-primary-dark) !important;
            color: #FFFFFF !important;
            box-shadow: 0 3px 8px rgba(108, 77, 255, 0.35) !important;
        }

        /* ---------------------------------------------------------------------------
           Cards & Surface Architecture (Fewer Boxes, Refined Spacing)
           --------------------------------------------------------------------------- */
        .metric-card {
            background: var(--mt-surface);
            border: 1px solid var(--mt-border);
            border-radius: var(--mt-radius-xl);
            padding: 18px 20px;
            box-shadow: var(--mt-shadow-card);
            transition: var(--mt-transition);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }
        .metric-card:hover {
            border-color: rgba(108, 77, 255, 0.25);
            box-shadow: var(--mt-shadow-hover);
        }
        
        .saas-card {
            background: var(--mt-surface);
            border-radius: var(--mt-radius-xl);
            padding: 20px 24px;
            box-shadow: var(--mt-shadow-card);
            border: 1px solid var(--mt-border);
            margin-bottom: var(--mt-space-md);
            transition: var(--mt-transition);
        }
        .saas-card:hover {
            border-color: rgba(108, 77, 255, 0.22);
        }

        /* Native Streamlit Bordered Container - Subtle & Spacious */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: var(--mt-radius-xl) !important;
            border: 1px solid var(--mt-border) !important;
            background: var(--mt-surface) !important;
            box-shadow: var(--mt-shadow-card) !important;
            transition: var(--mt-transition) !important;
            padding: 18px 22px !important;
            margin-bottom: 14px !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: rgba(108, 77, 255, 0.22) !important;
        }
        
        /* Prevent nested container double-box clutter */
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlockBorderWrapper"] {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            padding: 4px 0 !important;
            margin-bottom: 4px !important;
            border-radius: 0 !important;
        }
        
        div[data-testid="stForm"] {
            background: var(--mt-surface);
            border-radius: var(--mt-radius-xl);
            padding: 24px;
            box-shadow: var(--mt-shadow-card);
            border: 1px solid var(--mt-border);
            margin-bottom: var(--mt-space-md);
        }

        /* ---------------------------------------------------------------------------
           Form Inputs & Controls
           --------------------------------------------------------------------------- */
        div[data-testid="stTextInput"] div[data-baseweb="input"],
        .stTextInput input,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        div[data-testid="stTextArea"] textarea {
            border-radius: var(--mt-radius-md) !important;
            background: var(--mt-input-bg) !important;
            border: 1px solid var(--mt-border) !important;
            color: var(--mt-text) !important;
            font-size: 0.9rem !important;
            transition: var(--mt-transition) !important;
        }
        
        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
        .stTextInput input:focus,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within,
        div[data-testid="stTextArea"] textarea:focus {
            border-color: var(--mt-border-focus) !important;
            box-shadow: 0 0 0 3px rgba(108, 77, 255, 0.12) !important;
            background: var(--mt-input-focus-bg) !important;
        }
        
        /* Selectbox popover */
        div[data-baseweb="popover"] > div {
            background: var(--mt-surface) !important;
            border: 1px solid var(--mt-border) !important;
            border-radius: var(--mt-radius-md) !important;
            box-shadow: var(--mt-shadow-dropdown) !important;
        }
        div[data-baseweb="popover"] ul {
            background: var(--mt-surface) !important;
        }
        div[data-baseweb="popover"] li {
            color: var(--mt-text) !important;
            font-size: 0.88rem !important;
            transition: background 120ms ease;
        }
        div[data-baseweb="popover"] li:hover {
            background: var(--mt-surface-soft) !important;
            color: var(--mt-primary) !important;
        }

        /* File Uploader */
        .stFileUploader > div {
            background: var(--mt-surface);
            border: 2px dashed var(--mt-border);
            border-radius: var(--mt-radius-xl);
            padding: var(--mt-space-lg) !important;
            text-align: center;
            transition: var(--mt-transition);
        }
        .stFileUploader > div:hover {
            border-color: var(--mt-primary);
            background: var(--mt-accent);
        }

        /* ---------------------------------------------------------------------------
           Badges & Status Pills
           --------------------------------------------------------------------------- */
        .badge {
            padding: 3px 10px;
            border-radius: var(--mt-radius-pill);
            font-size: 0.74rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            letter-spacing: 0.01em;
            line-height: 1.35;
        }
        .badge-completed { background: var(--mt-success-bg); color: var(--mt-success); border: 1px solid var(--mt-success-border); }
        .badge-processing { background: var(--mt-primary-subtle); color: var(--mt-primary); border: 1px solid rgba(108, 77, 255, 0.22); }
        .badge-pending { background: var(--mt-warning-bg); color: var(--mt-warning); border: 1px solid var(--mt-warning-border); }
        .badge-failed { background: var(--mt-error-bg); color: var(--mt-error); border: 1px solid var(--mt-error-border); }
        .badge-demo { background: var(--mt-primary-subtle); color: var(--mt-primary); border: 1px solid rgba(108, 77, 255, 0.2); }
        .badge-neutral { background: rgba(115, 128, 154, 0.08); color: var(--mt-text-secondary); border: 1px solid var(--mt-border); }
        .badge-info { background: var(--mt-info-bg); color: var(--mt-info); border: 1px solid var(--mt-info-border); }

        /* ---------------------------------------------------------------------------
           Structured Evidence Box (Subtle, Clean)
           --------------------------------------------------------------------------- */
        .evidence-box {
            background: rgba(108, 77, 255, 0.025);
            border-radius: var(--mt-radius-md);
            padding: 10px 14px;
            margin: 8px 0;
            border: 1px solid rgba(108, 77, 255, 0.08);
            border-left: 3px solid var(--mt-primary);
        }
        .evidence-box-title {
            font-size: 0.72rem;
            color: var(--mt-text-secondary);
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 3px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .evidence-box-text {
            font-size: 0.88rem;
            color: var(--mt-text);
            font-style: italic;
            line-height: 1.5;
        }

        /* ---------------------------------------------------------------------------
           Transcript Messages & Dialogue Styling
           --------------------------------------------------------------------------- */
        .transcript-msg {
            background: var(--mt-surface);
            border-radius: var(--mt-radius-md);
            padding: 12px 16px;
            margin-bottom: 8px;
            border: 1px solid var(--mt-border);
            border-left: 3px solid var(--mt-primary);
            box-shadow: none;
            transition: var(--mt-transition);
        }
        .transcript-msg:hover {
            border-color: rgba(108, 77, 255, 0.25);
        }
        .transcript-msg-speaker01 { border-left-color: #6C4DFF; }
        .transcript-msg-speaker02 { border-left-color: #0284C7; }
        .transcript-msg-speaker03 { border-left-color: #0D9488; }
        .transcript-msg-speaker04 { border-left-color: #EA580C; }
        .transcript-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 4px;
        }
        .speaker-name {
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--mt-text);
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }
        .timestamp {
            font-size: 0.72rem;
            color: var(--mt-text-secondary);
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            background: var(--mt-surface-soft);
            padding: 2px 6px;
            border-radius: var(--mt-radius-sm);
        }
        .transcript-text {
            font-size: 0.9rem;
            color: var(--mt-text);
            line-height: 1.6;
        }

        /* ---------------------------------------------------------------------------
           Page Header & Typography
           --------------------------------------------------------------------------- */
        .page-title-container {
            margin-bottom: var(--mt-space-lg);
            padding-bottom: 0;
            border-bottom: none;
        }
        .page-title {
            color: var(--mt-text);
            font-weight: 750;
            font-size: 1.8rem;
            margin: 0 0 4px 0;
            display: flex;
            align-items: center;
            gap: 10px;
            letter-spacing: -0.025em;
            line-height: 1.25;
        }
        .page-subtitle {
            color: var(--mt-text-secondary);
            font-size: 0.92rem;
            margin: 0;
            line-height: 1.5;
        }

        /* ---------------------------------------------------------------------------
           Tabs Styling (Segmented, Lavender-Tinted Active State)
           --------------------------------------------------------------------------- */
        div[data-testid="stTabs"] button[role="tab"] {
            background: transparent !important;
            border: none !important;
            padding: 8px 18px !important;
            border-radius: var(--mt-radius-md) !important;
            color: var(--mt-text-secondary) !important;
            font-weight: 550 !important;
            font-size: 0.88rem !important;
            transition: var(--mt-transition) !important;
            margin-right: 4px !important;
        }
        div[data-testid="stTabs"] button[role="tab"]:hover {
            color: var(--mt-text) !important;
            background: rgba(23, 32, 51, 0.03) !important;
        }
        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            background: var(--mt-surface) !important;
            color: var(--mt-primary) !important;
            box-shadow: 0 1px 3px rgba(23, 32, 51, 0.06) !important;
            border: 1px solid var(--mt-border) !important;
            font-weight: 650 !important;
        }
        div[data-testid="stTabs"] > div[role="tablist"] {
            gap: 2px !important;
            background: var(--mt-surface-soft) !important;
            padding: 4px !important;
            border-radius: var(--mt-radius-lg) !important;
            border: 1px solid var(--mt-border) !important;
            border-bottom: 1px solid var(--mt-border) !important;
            display: inline-flex !important;
            margin-bottom: var(--mt-space-md) !important;
        }

        /* Progress Bar (Thin, Rounded) */
        div[data-testid="stProgress"] > div > div > div > div {
            background-color: var(--mt-primary) !important;
            border-radius: var(--mt-radius-pill) !important;
        }
        div[data-testid="stProgress"] > div > div {
            background-color: var(--mt-surface-soft) !important;
            border-radius: var(--mt-radius-pill) !important;
            height: 6px !important;
        }

        /* Expander (Clean, Subtle) */
        div[data-testid="stExpander"] {
            border: 1px solid var(--mt-border) !important;
            border-radius: var(--mt-radius-lg) !important;
            background: var(--mt-surface) !important;
            box-shadow: none !important;
            margin-bottom: 8px !important;
        }
        div[data-testid="stExpander"] details > summary {
            padding: 10px 16px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            color: var(--mt-text) !important;
        }
        div[data-testid="stExpander"] details > summary:hover {
            color: var(--mt-primary) !important;
        }

        /* Chat Input Styling */
        div[data-testid="stChatInput"] {
            padding-bottom: 16px !important;
            background: transparent !important;
            border: none !important;
        }
        div[data-testid="stChatInput"] > div {
            border-radius: var(--mt-radius-xl) !important;
            border: 1px solid var(--mt-border) !important;
            box-shadow: var(--mt-shadow-card) !important;
            background: var(--mt-input-bg) !important;
            transition: var(--mt-transition) !important;
        }
        div[data-testid="stChatInput"] > div:focus-within {
            border-color: var(--mt-primary) !important;
            box-shadow: 0 0 0 3px rgba(108, 77, 255, 0.12) !important;
        }

        /* Clean List Row / Divider Separator */
        .saas-row {
            padding: 14px 18px;
            border-bottom: 1px solid var(--mt-border);
            transition: var(--mt-transition);
            background: var(--mt-surface);
        }
        .saas-row:last-child {
            border-bottom: none;
        }
        .saas-row:hover {
            background: var(--mt-surface-hover);
        }

        /* Hide Default elements */
        footer {visibility: hidden !important;}
        header {background: transparent !important;}
        
        /* Remove empty markdown elements */
        .element-container:has(> .stMarkdown:empty) {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)
