import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
        /* CSS Variables - Design Tokens */
        :root {
            /* Colors */
            --primary: #7C3AED;
            --secondary: #4F46E5;
            --accent: #06B6D4;
            --bg-color: #F8FAFC;
            --surface: #FFFFFF;
            --text-main: #0F172A;
            --text-muted: #64748B;
            --success: #10B981;
            --warning: #F59E0B;
            --error: #EF4444;
            
            /* Spacing */
            --space-xs: 4px;
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 24px;
            --space-xl: 32px;
            --space-2xl: 48px;
            
            /* Radius */
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            
            /* Shadows */
            --shadow-soft: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
            --shadow-hover: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -2px rgba(0,0,0,0.04);
        }

        /* Modern Font and Global Resets */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: var(--text-main);
        }

        /* Center Main Content & Background Gradient */
        .stApp {
            background: linear-gradient(135deg, var(--bg-color) 0%, #EFF6FF 50%, #F5F3FF 100%);
        }
        
        /* Unified app container instead of scattered block container styles */
        .block-container {
            max-width: 1024px !important;
            padding-top: var(--space-xl) !important;
            padding-bottom: var(--space-2xl) !important;
            padding-left: var(--space-xl) !important;
            padding-right: var(--space-xl) !important;
            margin: 0 auto;
        }

        /* Sidebar Glassmorphism */
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.75) !important;
            backdrop-filter: blur(24px) !important;
            -webkit-backdrop-filter: blur(24px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.6) !important;
            box-shadow: 2px 0 12px rgba(0, 0, 0, 0.02);
        }
        
        /* Sidebar Logo / Header */
        [data-testid="stSidebarNav"] {
            display: none; /* Hide default nav */
        }
        
        .sidebar-logo-container {
            padding: var(--space-md) 0;
            text-align: center;
        }
        .sidebar-logo-title {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: var(--space-xs);
        }
        .sidebar-logo-subtitle {
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 500;
            letter-spacing: 0.5px;
        }

        /* Button System */
        div.stButton > button {
            border-radius: var(--radius-md) !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            padding: 0 20px !important;
            min-height: 42px !important;
            height: 42px !important;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1 !important;
        }

        /* Primary Button */
        div.stButton > button[kind="primary"] {
            background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(124, 58, 237, 0.25) !important;
        }
        div.stButton > button[kind="primary"]:hover {
            box-shadow: 0 6px 15px rgba(124, 58, 237, 0.4) !important;
            transform: translateY(-1px) !important;
        }

        /* Secondary Button */
        div.stButton > button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid #CBD5E1 !important;
            color: var(--text-main) !important;
            box-shadow: var(--shadow-soft) !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            background: white !important;
            border-color: #94A3B8 !important;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08) !important;
            transform: translateY(-1px) !important;
        }

        /* Metric Cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            box-shadow: var(--shadow-soft);
            border: 1px solid rgba(255, 255, 255, 0.8);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100%;
            min-height: 140px;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }
        .metric-icon {
            font-size: 1.75rem;
            margin-bottom: var(--space-sm);
        }
        .metric-label {
            color: var(--text-muted);
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: var(--space-xs);
        }
        .metric-value {
            color: var(--text-main);
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0;
            line-height: 1.1;
        }
        
        /* Gradients */
        .gradient-text {
            background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Generic SaaS Cards */
        .saas-card {
            background: var(--surface);
            border-radius: 20px;
            padding: 24px;
            box-shadow: var(--shadow-soft);
            border: 1px solid #E2E8F0;
            margin-bottom: var(--space-md);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            height: 100%;
        }
        .saas-card:hover {
            box-shadow: var(--shadow-hover);
            transform: translateY(-1px);
        }
        
        div[data-testid="stForm"] {
            background: var(--surface);
            border-radius: 20px;
            padding: 32px;
            box-shadow: var(--shadow-soft);
            border: 1px solid #E2E8F0;
            margin-bottom: var(--space-md);
        }

        /* Badges */
        .badge {
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }
        .badge-completed { background: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }
        .badge-processing { background: #E0E7FF; color: #3730A3; border: 1px solid #C7D2FE; }
        .badge-pending { background: #FFEDD5; color: #9A3412; border: 1px solid #FED7AA; }
        .badge-failed { background: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
        
        /* File Uploader styling */
        .stFileUploader > div {
            background: rgba(255, 255, 255, 0.7);
            border: 2px dashed #CBD5E1;
            border-radius: var(--radius-lg);
            padding: var(--space-xl) !important;
            text-align: center;
            transition: all 0.2s ease;
        }
        .stFileUploader > div:hover {
            border-color: var(--primary);
            background: rgba(255, 255, 255, 0.95);
        }

        /* Transcript messages */
        .transcript-msg {
            background: var(--surface);
            border-radius: var(--radius-md);
            padding: var(--space-md) var(--space-lg);
            margin-bottom: var(--space-md);
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            border-left: 4px solid #E2E8F0;
            border-top: 1px solid #F1F5F9;
            border-right: 1px solid #F1F5F9;
            border-bottom: 1px solid #F1F5F9;
        }
        .transcript-msg-speaker01 { border-left-color: var(--primary); }
        .transcript-msg-speaker02 { border-left-color: var(--accent); }
        .transcript-msg-speaker03 { border-left-color: var(--warning); }
        .transcript-msg-speaker04 { border-left-color: var(--success); }
        
        .transcript-header {
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            margin-bottom: var(--space-xs);
        }
        .speaker-name {
            font-weight: 600;
            font-size: 0.85rem;
            color: var(--text-main);
        }
        .timestamp {
            font-size: 0.75rem;
            color: var(--text-muted);
        }
        .transcript-text {
            color: #1E293B;
            line-height: 1.6;
            font-size: 0.95rem;
        }
        
        /* Page Header Title */
        .page-title-container {
            margin-bottom: var(--space-xl);
            padding-bottom: var(--space-md);
            border-bottom: 1px solid rgba(0,0,0,0.05);
        }
        .page-title {
            color: var(--text-main);
            font-weight: 800;
            font-size: 2.2rem;
            margin-bottom: var(--space-xs);
            display: flex;
            align-items: center;
            gap: var(--space-sm);
        }
        .page-subtitle {
            color: var(--text-muted);
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
        
        </style>
    """, unsafe_allow_html=True)
