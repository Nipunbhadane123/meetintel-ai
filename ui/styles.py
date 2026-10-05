import streamlit as st

def apply_global_styles():
    theme = st.session_state.get('theme_preference', 'System')
    
    # Base CSS variables (Light Theme)
    light_vars = """
            --mt-primary: #6C4CF1;
            --mt-primary-dark: #4F46E5;
            --mt-secondary: #7C3AED;
            --mt-accent: #38BDF8;
            --mt-cyan: #06B6D4;
            --mt-bg: #F7F8FC; 
            --mt-surface: #FFFFFF;
            --mt-surface-soft: rgba(255, 255, 255, 0.6);
            
            --mt-text: #111827;
            --mt-text-secondary: #64748B;
            --mt-text-muted: #94A3B8;
            
            --mt-border: #E5E7EB;
            --mt-border-light: rgba(15, 23, 42, 0.04);
            
            --mt-success: #10B981;
            --mt-warning: #F59E0B;
            --mt-error: #EF4444;
            
            --mt-grad-primary: linear-gradient(135deg, #7C5CFC 0%, #6C4CF1 50%, #4F46E5 100%);
            --mt-grad-subtle: linear-gradient(90deg, rgba(108, 76, 241, 0.08), rgba(108, 76, 241, 0.02));
            --mt-grad-bg: radial-gradient(circle at 15% 10%, rgba(108, 76, 241, 0.04) 0%, transparent 40%),
                          radial-gradient(circle at 85% 90%, rgba(6, 182, 212, 0.04) 0%, transparent 40%);
            
            --mt-shadow-soft: 0 4px 20px rgba(15, 23, 42, 0.03);
            --mt-shadow-hover: 0 10px 30px rgba(108, 76, 241, 0.08);
            --mt-shadow-card: 0 2px 8px rgba(15, 23, 42, 0.02), 0 1px 2px rgba(15, 23, 42, 0.04);
            
            --mt-input-bg: #FAFAFF;
            --mt-input-focus-bg: #FFFFFF;
    """
    
    # Dark Theme variables
    dark_vars = """
            --mt-primary: #818CF8;
            --mt-primary-dark: #6366F1;
            --mt-secondary: #A78BFA;
            --mt-accent: #38BDF8;
            --mt-cyan: #22D3EE;
            --mt-bg: #0B1020; 
            --mt-surface: #151C2E;
            --mt-surface-soft: #1B2438;
            
            --mt-text: #F8FAFC;
            --mt-text-secondary: #94A3B8;
            --mt-text-muted: #64748B;
            
            --mt-border: #273449;
            --mt-border-light: rgba(248, 250, 252, 0.05);
            
            --mt-success: #34D399;
            --mt-warning: #FBBF24;
            --mt-error: #F87171;
            
            --mt-grad-primary: linear-gradient(135deg, #818CF8 0%, #6366F1 50%, #4F46E5 100%);
            --mt-grad-subtle: linear-gradient(90deg, rgba(129, 140, 248, 0.15), rgba(129, 140, 248, 0.05));
            --mt-grad-bg: radial-gradient(circle at 15% 10%, rgba(129, 140, 248, 0.08) 0%, transparent 40%),
                          radial-gradient(circle at 85% 90%, rgba(34, 211, 238, 0.08) 0%, transparent 40%);
            
            --mt-shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.2);
            --mt-shadow-hover: 0 10px 30px rgba(129, 140, 248, 0.15);
            --mt-shadow-card: 0 4px 12px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.1);
            
            --mt-input-bg: #0B1020;
            --mt-input-focus-bg: #151C2E;
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
            --base-font-family: 'Inter', sans-serif !important;
            
            /* Spacing */
            --mt-space-xs: 4px;
            --mt-space-sm: 8px;
            --mt-space-md: 16px;
            --mt-space-lg: 24px;
            --mt-space-xl: 32px;
            --mt-space-2xl: 48px;
            
            /* Radius */
            --mt-radius-sm: 6px;
            --mt-radius-md: 12px;
            --mt-radius-lg: 16px;
            --mt-radius-xl: 24px;
            
            /* Transitions */
            --mt-transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Modern Font and Global Resets */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"], .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown span {
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: var(--mt-text) !important;
            -webkit-font-smoothing: antialiased;
        }

        /* Center Main Content & Background */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: var(--mt-bg) !important;
            background-image: var(--mt-grad-bg) !important;
            background-attachment: fixed !important;
        }
        
        /* Unified app container */
        .block-container {
            max-width: 1100px !important;
            padding-top: var(--mt-space-xl) !important;
            padding-bottom: var(--mt-space-2xl) !important;
            padding-left: var(--mt-space-2xl) !important;
            padding-right: var(--mt-space-2xl) !important;
            margin: 0 auto;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
            background-color: var(--mt-surface) !important;
            background-image: none !important;
            border-right: 1px solid var(--mt-border) !important;
            box-shadow: 2px 0 20px rgba(15, 23, 42, 0.02) !important;
        }
        
        [data-testid="stSidebarNav"] {
            display: none; /* Hide default nav */
        }
        
        .sidebar-logo-container {
            padding: var(--mt-space-2xl) var(--mt-space-lg) var(--mt-space-xl) var(--mt-space-xl);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .sidebar-logo-icon {
            font-size: 24px;
            background: var(--mt-grad-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        .sidebar-logo-text {
            display: flex;
            flex-direction: column;
        }
        .sidebar-logo-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--mt-text);
            margin: 0;
            letter-spacing: -0.02em;
        }
        .sidebar-logo-subtitle {
            font-size: 0.75rem;
            color: var(--mt-text-muted);
            font-weight: 500;
            margin: 0;
            letter-spacing: 0.02em;
        }

        /* Sidebar Buttons */
        [data-testid="stSidebar"] div.stButton > button {
            border-radius: var(--mt-radius-sm) !important;
            font-weight: 500 !important;
            transition: var(--mt-transition) !important;
            padding: 8px 16px !important;
            min-height: 42px !important;
            height: 42px !important;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
            color: var(--mt-text-secondary) !important;
            width: calc(100% - 16px) !important;
            margin-left: 8px !important;
            margin-right: 8px !important;
            transform: none !important;
        }
        /* Hover (Inactive) */
        [data-testid="stSidebar"] div.stButton > button:hover {
            background: rgba(15, 23, 42, 0.03) !important;
            color: var(--mt-text) !important;
        }
        /* Active Sidebar Button */
        [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
            background: var(--mt-grad-subtle) !important;
            color: var(--mt-primary-dark) !important;
            font-weight: 600 !important;
            box-shadow: inset 3px 0 0 0 var(--mt-primary) !important;
            border-radius: 0 var(--mt-radius-sm) var(--mt-radius-sm) 0 !important;
            margin-left: 0 !important;
            width: 100% !important;
        }
        /* Active + Hover Sidebar Button */
        [data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(90deg, rgba(108,76,241,0.12), rgba(108,76,241,0.04)) !important;
        }

        /* Generic Button styles covering Form Submit */
        div[data-testid="stFormSubmitButton"] > button,
        div.stButton > button {
            border-radius: var(--mt-radius-md) !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
            transition: all 200ms cubic-bezier(0.22, 1, 0.36, 1) !important;
            padding: 0 20px !important;
            min-height: 42px !important;
            height: auto !important;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--mt-border) !important;
            background: var(--mt-surface) !important;
            color: var(--mt-text) !important;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05) !important;
        }
        div[data-testid="stFormSubmitButton"] > button:hover,
        div.stButton > button:hover {
            background: var(--mt-bg) !important;
            border-color: rgba(108, 76, 241, 0.3) !important;
            color: var(--mt-primary-dark) !important;
            box-shadow: 0 4px 12px rgba(108, 76, 241, 0.08) !important;
            transform: translateY(-1px) !important;
        }
        div[data-testid="stFormSubmitButton"] > button:active,
        div.stButton > button:active {
            transform: translateY(1px) scale(0.98) !important;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05) !important;
        }
        
        div[data-testid="stFormSubmitButton"] > button[kind="primary"],
        div[data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"],
        div.stButton > button[kind="primary"] {
            background: var(--mt-grad-primary) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(108, 76, 241, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
        }
        div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"]:hover,
        div.stButton > button[kind="primary"]:hover {
            box-shadow: 0 6px 16px rgba(108, 76, 241, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.3) !important;
            transform: translateY(-1px) !important;
            background: linear-gradient(135deg, #7C3AED 0%, #6366F1 50%, #2563EB 100%) !important;
        }
        div[data-testid="stFormSubmitButton"] > button[kind="primary"]:active,
        div[data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"]:active,
        div.stButton > button[kind="primary"]:active {
            transform: translateY(1px) scale(0.98) !important;
            box-shadow: 0 2px 4px rgba(108, 76, 241, 0.2) !important;
            background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        }

        /* Metric Cards */
        .metric-card {
            background: var(--mt-surface);
            border: 1px solid var(--mt-border);
            border-radius: var(--mt-radius-xl);
            padding: var(--mt-space-lg);
            box-shadow: 0 4px 6px rgba(15,23,42,0.02);
            transition: all 300ms cubic-bezier(0.22, 1, 0.36, 1);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }
        .metric-card:hover {
            box-shadow: 0 12px 24px rgba(15,23,42,0.06), 0 4px 8px rgba(15,23,42,0.03);
            border-color: rgba(108, 76, 241, 0.2);
            transform: translateY(-4px);
        }
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 2px;
            background: var(--mt-grad-primary);
            opacity: 0;
            transition: opacity 300ms ease;
        }
        .metric-card:hover::before {
            opacity: 1;
        }
        
        /* Generic SaaS Cards */
        .saas-card {
            background: var(--mt-surface);
            border-radius: var(--mt-radius-xl);
            padding: var(--mt-space-lg);
            box-shadow: 0 4px 6px rgba(15,23,42,0.02);
            border: 1px solid var(--mt-border);
            margin-bottom: var(--mt-space-md);
            transition: all 300ms cubic-bezier(0.22, 1, 0.36, 1);
        }
        .saas-card:hover {
            box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04), 0 4px 8px rgba(15, 23, 42, 0.02);
            border-color: rgba(108, 76, 241, 0.2);
            transform: translateY(-2px);
        }
        
        div[data-testid="stForm"] {
            background: var(--mt-surface);
            border-radius: var(--mt-radius-xl);
            padding: var(--mt-space-2xl);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03), 0 1px 3px rgba(15, 23, 42, 0.05);
            border: 1px solid var(--mt-border);
            margin-bottom: var(--mt-space-md);
        }
        
        /* Standard Text Inputs */
        div[data-testid="stTextInput"] div[data-baseweb="input"],
        div[data-testid="stTextInput"] .st-emotion-cache-1n76uvr,
        .stTextInput input,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            border-radius: var(--mt-radius-md) !important;
            background: var(--mt-input-bg) !important;
            border: 1px solid var(--mt-border) !important;
            color: var(--mt-text) !important;
            transition: all 250ms cubic-bezier(0.22, 1, 0.36, 1) !important;
        }
        
        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
        .stTextInput input:focus,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
            border-color: var(--mt-primary) !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
            background: var(--mt-input-focus-bg) !important;
        }
        
        /* Selectbox dropdown overrides for Dark mode */
        div[data-baseweb="popover"] > div {
            background: var(--mt-surface) !important;
            border: 1px solid var(--mt-border) !important;
        }
        div[data-baseweb="popover"] ul {
            background: var(--mt-surface) !important;
        }
        div[data-baseweb="popover"] li {
            color: var(--mt-text) !important;
            transition: background 150ms ease;
        }
        div[data-baseweb="popover"] li:hover {
            background: var(--mt-border-light) !important;
        }
        
        /* Password icon animations */
        div[data-testid="stTextInput"] button[aria-label*="password"] {
            transition: all 200ms ease-out !important;
            opacity: 0.6 !important;
        }
        div[data-testid="stTextInput"] button[aria-label*="password"]:hover {
            opacity: 1 !important;
            transform: scale(1.1) !important;
            color: var(--mt-primary) !important;
        }
        div[data-testid="stTextInput"] button[aria-label*="password"]:active {
            transform: scale(0.9) !important;
        }

        /* Premium Chat Input */
        div[data-testid="stChatInput"] {
            padding-bottom: 24px !important;
            background: transparent !important;
            border: none !important;
        }
        div[data-testid="stChatInput"] > div {
            border-radius: var(--mt-radius-xl) !important;
            border: 1px solid var(--mt-border) !important;
            box-shadow: var(--mt-shadow-soft) !important;
            background: var(--mt-input-bg) !important;
            transition: var(--mt-transition) !important;
        }
        div[data-testid="stChatInput"] > div:focus-within {
            border-color: var(--mt-primary) !important;
            box-shadow: 0 0 0 3px rgba(108, 76, 241, 0.15), var(--mt-shadow-soft) !important;
            background: var(--mt-input-focus-bg) !important;
        }
        div[data-testid="stChatInput"] textarea {
            border: none !important;
            box-shadow: none !important;
            padding: 16px 24px !important;
            font-size: 1rem !important;
            color: var(--mt-text) !important;
        }
        div[data-testid="stChatInput"] button {
            background: var(--mt-grad-primary) !important;
            border-radius: 50% !important;
            width: 38px !important;
            height: 38px !important;
            margin: 6px 12px !important;
            transition: var(--mt-transition) !important;
        }
        div[data-testid="stChatInput"] button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 4px 12px rgba(108, 76, 241, 0.3) !important;
        }
        div[data-testid="stChatInput"] button svg {
            fill: white !important;
            stroke: white !important;
            color: white !important;
        }

        /* Badges */
        .badge {
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            letter-spacing: 0.02em;
        }
        .badge-completed { background: rgba(16,185,129,0.1); color: #047857; border: 1px solid rgba(16,185,129,0.2); }
        .badge-processing { background: rgba(108,76,241,0.1); color: #5B2FE0; border: 1px solid rgba(108,76,241,0.2); }
        .badge-pending { background: rgba(245,158,11,0.1); color: #B45309; border: 1px solid rgba(245,158,11,0.2); }
        .badge-failed { background: rgba(239,68,68,0.1); color: #B91C1C; border: 1px solid rgba(239,68,68,0.2); }
        
        /* File Uploader styling */
        .stFileUploader > div {
            background: rgba(255, 255, 255, 0.8);
            border: 2px dashed rgba(15,23,42,0.12);
            border-radius: var(--mt-radius-lg);
            padding: var(--mt-space-xl) !important;
            text-align: center;
            transition: var(--mt-transition);
        }
        .stFileUploader > div:hover {
            border-color: var(--mt-primary);
            background: white;
            box-shadow: var(--mt-shadow-soft);
        }

        /* Page Header Title */
        .page-title-container {
            margin-bottom: var(--mt-space-xl);
            padding-bottom: var(--mt-space-md);
            border-bottom: 1px solid var(--mt-border-light);
        }
        .page-title {
            color: var(--mt-text);
            font-weight: 700;
            font-size: 2rem;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 12px;
            letter-spacing: -0.02em;
        }
        .page-subtitle {
            color: var(--mt-text-secondary);
            font-size: 1rem;
            margin: 0;
            line-height: 1.5;
        }
        
        /* Hide Default elements */
        footer {visibility: hidden;}
        header {background: transparent !important;}
        
        /* Remove empty streamlit containers */
        .element-container:has(> .stMarkdown:empty) {
            display: none;
        }
        
        /* Tabs Premium Styling */
        div[data-testid="stTabs"] button[role="tab"] {
            background: transparent !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: var(--mt-radius-md) !important;
            color: var(--mt-text-muted) !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 300ms cubic-bezier(0.22, 1, 0.36, 1) !important;
            margin-right: 8px !important;
        }
        div[data-testid="stTabs"] button[role="tab"]:hover {
            color: var(--mt-text) !important;
            background: rgba(15, 23, 42, 0.03) !important;
        }
        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            background: white !important;
            color: var(--mt-primary-dark) !important;
            box-shadow: var(--mt-shadow-card) !important;
            border: 1px solid var(--mt-border) !important;
            transform: scale(1.02);
        }
        div[data-testid="stTabs"] > div[role="tablist"] {
            gap: 4px !important;
            background: rgba(15, 23, 42, 0.03) !important;
            padding: 6px !important;
            border-radius: var(--mt-radius-lg) !important;
            border-bottom: none !important;
            display: inline-flex !important;
            margin-bottom: var(--mt-space-lg) !important;
        }
        
        /* Smooth transitions for tab panels */
        div[data-testid="stTabs"] div[role="tabpanel"] {
            animation: tabFadeIn 400ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
        }
        
        @keyframes tabFadeIn {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)
