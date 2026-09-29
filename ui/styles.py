import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
        /* CSS Variables - Design Tokens */
        :root {
            /* Colors */
            --mt-primary: #6D4AFF;
            --mt-primary-dark: #5735D6;
            --mt-secondary: #4F46E5;
            --mt-accent: #8B5CF6;
            --mt-bg: #F7F8FC;
            --mt-surface: #FFFFFF;
            --mt-surface-soft: #FAFAFF;
            
            --mt-text: #101828;
            --mt-text-secondary: #475467;
            --mt-text-muted: #98A2B3;
            
            --mt-border: rgba(16,24,40,0.08);
            
            --mt-success: #12B76A;
            --mt-warning: #F79009;
            --mt-error: #F04438;
            
            /* Gradients */
            --mt-grad-primary: linear-gradient(135deg, #7C3AED 0%, #6366F1 50%, #4F46E5 100%);
            --mt-grad-subtle: linear-gradient(90deg, rgba(109,61,245,0.13), rgba(109,61,245,0.04));
            
            /* Spacing */
            --mt-space-xs: 4px;
            --mt-space-sm: 8px;
            --mt-space-md: 16px;
            --mt-space-lg: 24px;
            --mt-space-xl: 32px;
            --mt-space-2xl: 48px;
            
            /* Radius */
            --mt-radius-sm: 8px;
            --mt-radius-md: 12px;
            --mt-radius-lg: 16px;
            --mt-radius-xl: 20px;
            
            /* Shadows */
            --mt-shadow-soft: 0 2px 10px rgba(16,24,40,0.04);
            --mt-shadow-hover: 0 8px 24px rgba(79,70,229,0.08);
            
            /* Transitions */
            --mt-transition: all 160ms ease;
        }

        /* Modern Font and Global Resets */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;650;700;750&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: var(--mt-text);
        }

        /* Center Main Content & Background */
        .stApp {
            background-color: var(--mt-bg);
            background-image: 
                radial-gradient(circle at 85% 5%, rgba(124,58,237,0.06), transparent 30%),
                radial-gradient(circle at 15% 90%, rgba(79,70,229,0.04), transparent 30%);
            background-attachment: fixed;
        }
        
        /* Unified app container */
        .block-container {
            max-width: 1024px !important;
            padding-top: var(--mt-space-xl) !important;
            padding-bottom: var(--mt-space-2xl) !important;
            padding-left: var(--mt-space-xl) !important;
            padding-right: var(--mt-space-xl) !important;
            margin: 0 auto;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: var(--mt-surface) !important;
            border-right: 1px solid var(--mt-border) !important;
            box-shadow: 2px 0 12px rgba(16, 24, 40, 0.02) !important;
        }
        
        [data-testid="stSidebarNav"] {
            display: none; /* Hide default nav */
        }
        
        .sidebar-logo-container {
            padding: var(--mt-space-xl) var(--mt-space-lg) var(--mt-space-lg) var(--mt-space-lg);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .sidebar-logo-icon {
            font-size: 26px;
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
            font-size: 1.15rem;
            font-weight: 750;
            color: var(--mt-text);
            margin: 0;
            line-height: 1.2;
            letter-spacing: -0.02em;
        }
        .sidebar-logo-subtitle {
            font-size: 0.75rem;
            color: var(--mt-text-muted);
            font-weight: 500;
            margin: 0;
            line-height: 1.2;
            letter-spacing: 0.02em;
        }

        /* Sidebar Buttons */
        [data-testid="stSidebar"] div.stButton > button {
            border-radius: var(--mt-radius-sm) !important;
            font-weight: 500 !important;
            transition: var(--mt-transition) !important;
            padding: 8px 16px !important;
            min-height: 40px !important;
            height: 40px !important;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
            color: var(--mt-text-secondary) !important;
            width: 100% !important;
            transform: none !important;
        }
        /* Hover (Inactive) */
        [data-testid="stSidebar"] div.stButton > button:hover {
            background: rgba(109, 61, 245, 0.04) !important;
            color: var(--mt-secondary) !important;
            box-shadow: none !important;
            transform: none !important;
        }
        /* Active Sidebar Button */
        [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
            background: var(--mt-grad-subtle) !important;
            color: #5B35D5 !important;
            font-weight: 600 !important;
            box-shadow: inset 3px 0 0 0 var(--mt-accent), 0 1px 2px rgba(109, 61, 245, 0.02) !important;
            border-radius: 0 var(--mt-radius-sm) var(--mt-radius-sm) 0 !important;
            transform: none !important;
        }
        /* Active + Hover Sidebar Button */
        [data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(90deg, rgba(109,61,245,0.16), rgba(109,61,245,0.06)) !important;
            color: #5B35D5 !important;
            box-shadow: inset 3px 0 0 0 var(--mt-accent), 0 1px 3px rgba(109, 61, 245, 0.04) !important;
            transform: none !important;
        }
        /* Focus */
        [data-testid="stSidebar"] div.stButton > button:focus {
            box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
            outline: none !important;
        }

        /* Main Content Buttons */
        div.stMainBlockContainer div.stButton > button {
            border-radius: var(--mt-radius-sm) !important;
            font-weight: 500 !important;
            transition: var(--mt-transition) !important;
            padding: 0 16px !important;
            min-height: 36px !important;
            height: auto !important;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--mt-border) !important;
            background: var(--mt-surface) !important;
            color: var(--mt-text) !important;
            box-shadow: var(--mt-shadow-soft) !important;
        }
        /* Hover Main Secondary */
        div.stMainBlockContainer div.stButton > button:hover {
            background: rgba(109, 61, 245, 0.02) !important;
            border-color: rgba(109, 61, 245, 0.15) !important;
            color: var(--mt-primary-dark) !important;
            box-shadow: var(--mt-shadow-hover) !important;
            transform: translateY(-1px) !important;
        }
        
        /* Main Primary Buttons */
        div.stMainBlockContainer div.stButton > button[kind="primary"] {
            background: var(--mt-grad-primary) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 2px 6px rgba(109, 61, 245, 0.25) !important;
        }
        /* Main Primary Hover */
        div.stMainBlockContainer div.stButton > button[kind="primary"]:hover {
            box-shadow: 0 4px 12px rgba(109, 61, 245, 0.35) !important;
            transform: translateY(-1px) !important;
            background: linear-gradient(135deg, #7132DE, #5558E2, #473FCC) !important;
            color: white !important;
        }

        /* Metric Cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border-radius: var(--mt-radius-lg);
            padding: var(--mt-space-lg);
            box-shadow: var(--mt-shadow-soft);
            border: 1px solid rgba(255, 255, 255, 0.8);
            transition: var(--mt-transition);
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100%;
            min-height: 140px;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--mt-shadow-hover);
        }
        .metric-icon {
            font-size: 1.75rem;
            margin-bottom: var(--mt-space-sm);
        }
        .metric-label {
            color: var(--mt-text-muted);
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: var(--mt-space-xs);
        }
        .metric-value {
            color: var(--mt-text);
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0;
            line-height: 1.1;
        }
        
        /* Gradients */
        .gradient-text {
            background: linear-gradient(90deg, var(--mt-primary), var(--mt-secondary), var(--mt-accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Generic SaaS Cards */
        .saas-card {
            background: var(--mt-surface);
            border-radius: var(--mt-radius-xl);
            padding: var(--mt-space-lg);
            box-shadow: var(--mt-shadow-soft);
            border: 1px solid var(--mt-border);
            margin-bottom: var(--mt-space-md);
            transition: var(--mt-transition);
            height: 100%;
        }
        .saas-card:hover {
            box-shadow: var(--mt-shadow-hover);
            transform: translateY(-2px);
        }
        
        div[data-testid="stForm"] {
            background: var(--mt-surface);
            border-radius: var(--mt-radius-xl);
            padding: var(--mt-space-xl);
            box-shadow: var(--mt-shadow-soft);
            border: 1px solid var(--mt-border);
            margin-bottom: var(--mt-space-md);
        }
        
        /* Premium Chat Input & Text Inputs */
        div[data-testid="stChatInput"] {
            padding-bottom: 24px !important;
            background: transparent !important;
            border: none !important;
        }
        div[data-testid="stChatInput"] > div {
            border-radius: var(--mt-radius-xl) !important;
            border: 1px solid var(--mt-border) !important;
            box-shadow: 0 8px 24px rgba(16, 24, 40, 0.06) !important;
            background: white !important;
            transition: var(--mt-transition) !important;
        }
        div[data-testid="stChatInput"] > div:focus-within {
            border-color: var(--mt-primary) !important;
            box-shadow: 0 0 0 3px rgba(109, 61, 245, 0.12), 0 8px 24px rgba(16, 24, 40, 0.06) !important;
        }
        div[data-testid="stChatInput"] textarea {
            border: none !important;
            box-shadow: none !important;
            padding: 16px 24px !important;
            font-size: 1rem !important;
            background: transparent !important;
            color: var(--mt-text) !important;
        }
        div[data-testid="stChatInput"] textarea:focus {
            box-shadow: none !important;
            border: none !important;
        }
        div[data-testid="stChatInput"] button {
            background: var(--mt-grad-primary) !important;
            border-radius: 50% !important;
            width: 38px !important;
            height: 38px !important;
            margin: 6px 8px !important;
            transition: var(--mt-transition) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        div[data-testid="stChatInput"] button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 4px 12px rgba(109, 61, 245, 0.3) !important;
        }
        div[data-testid="stChatInput"] button svg {
            fill: white !important;
            stroke: white !important;
            color: white !important;
        }
        
        /* Standard Text Inputs */
        div[data-baseweb="input"] {
            border-radius: var(--mt-radius-md) !important;
            background: white !important;
            border: 1px solid var(--mt-border) !important;
            transition: var(--mt-transition) !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: var(--mt-primary) !important;
            box-shadow: 0 0 0 3px rgba(109, 61, 245, 0.12) !important;
        }

        /* Badges */
        .badge {
            padding: 0.25rem 0.75rem;
            border-radius: var(--mt-radius-sm);
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }
        .badge-completed { background: rgba(18,183,106,0.10); color: #087443; border: 1px solid rgba(18,183,106,0.15); }
        .badge-processing { background: rgba(109,61,245,0.10); color: #5B2FE0; border: 1px solid rgba(109,61,245,0.15); }
        .badge-pending { background: rgba(247,144,9,0.10); color: #B54708; border: 1px solid rgba(247,144,9,0.15); }
        .badge-failed { background: rgba(240,68,56,0.10); color: #B42318; border: 1px solid rgba(240,68,56,0.15); }
        
        /* File Uploader styling */
        .stFileUploader > div {
            background: rgba(255, 255, 255, 0.7);
            border: 1px dashed rgba(16,24,40,0.15);
            border-radius: var(--mt-radius-lg);
            padding: var(--mt-space-xl) !important;
            text-align: center;
            transition: var(--mt-transition);
        }
        .stFileUploader > div:hover {
            border-color: var(--mt-primary);
            background: rgba(255, 255, 255, 0.95);
        }

        /* Transcript messages */
        .transcript-msg {
            background: var(--mt-surface);
            border-radius: var(--mt-radius-md);
            padding: var(--mt-space-md) var(--mt-space-lg);
            margin-bottom: var(--mt-space-md);
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            border-left: 3px solid #E2E8F0;
            border-top: 1px solid var(--mt-border);
            border-right: 1px solid var(--mt-border);
            border-bottom: 1px solid var(--mt-border);
        }
        .transcript-msg-speaker01 { border-left-color: var(--mt-primary); }
        .transcript-msg-speaker02 { border-left-color: var(--mt-accent); }
        .transcript-msg-speaker03 { border-left-color: var(--mt-warning); }
        .transcript-msg-speaker04 { border-left-color: var(--mt-success); }
        
        .transcript-header {
            display: flex;
            align-items: center;
            gap: var(--mt-space-sm);
            margin-bottom: var(--mt-space-xs);
        }
        .speaker-name {
            font-weight: 600;
            font-size: 0.85rem;
            color: var(--mt-text);
        }
        .timestamp {
            font-size: 0.75rem;
            color: var(--mt-text-muted);
        }
        .transcript-text {
            color: var(--mt-text-secondary);
            line-height: 1.6;
            font-size: 0.95rem;
        }
        
        /* Page Header Title */
        .page-title-container {
            margin-bottom: var(--mt-space-xl);
            padding-bottom: var(--mt-space-md);
            border-bottom: 1px solid var(--mt-border);
        }
        .page-title {
            color: var(--mt-text);
            font-weight: 750;
            font-size: 2.2rem;
            margin-bottom: var(--mt-space-xs);
            display: flex;
            align-items: center;
            gap: var(--mt-space-sm);
            letter-spacing: -0.02em;
        }
        .page-subtitle {
            color: var(--mt-text-secondary);
            font-size: 1.05rem;
            margin: 0;
        }
        
        /* Hide Default elements */
        footer {visibility: hidden;}
        header {background: transparent !important;}
        
        /* Remove empty streamlit containers taking up height */
        .element-container:has(> .stMarkdown:empty) {
            display: none;
        }
        .stMarkdown p:empty {
            display: none;
        }
        
        /* Tabs Premium Styling */
        div[data-testid="stTabs"] {
            /* Container styling if needed */
        }
        div[data-testid="stTabs"] button[data-baseweb="tab"] {
            background: transparent !important;
            border: none !important;
            padding: 8px 16px !important;
            border-radius: var(--mt-radius-md) !important;
            color: var(--mt-text-secondary) !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
            margin-right: 4px !important;
            transition: var(--mt-transition) !important;
        }
        div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
            color: var(--mt-text) !important;
            background: rgba(16, 24, 40, 0.04) !important;
        }
        div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
            background: var(--mt-surface) !important;
            color: var(--mt-text) !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(16, 24, 40, 0.08) !important;
            border: 1px solid var(--mt-border) !important;
        }
        /* Hide default bottom border for tabs */
        div[data-testid="stTabs"] > div[data-baseweb="tab-list"] {
            gap: 4px !important;
            background: rgba(16, 24, 40, 0.03) !important;
            padding: 6px !important;
            border-radius: var(--mt-radius-lg) !important;
            border-bottom: none !important;
            display: inline-flex !important;
            margin-bottom: var(--mt-space-lg) !important;
        }
        div[data-testid="stTabs"] > div[data-baseweb="tab-highlight"] {
            display: none !important;
        }
        
        </style>
    """, unsafe_allow_html=True)
