import streamlit as st
import os
import hashlib
from pathlib import Path
from audio.validator import validate_file, get_file_metadata, SUPPORTED_EXTENSIONS
from ui.components import section_header
from storage.database import get_db
from storage.repository import get_meeting_by_hash

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as afile:
        buf = afile.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(65536)
    return hasher.hexdigest()

def render_upload_page():
    section_header("🎙️ Upload Your Meeting", "Drag & drop your audio or video file below")
    
    # Check if we already have a validated file in session state for this visit
    if 'current_upload' in st.session_state and Path(st.session_state['current_upload']).exists() and 'processing_started' not in st.session_state:
        # Show file details card instead of uploader
        metadata = st.session_state.get('upload_metadata', {})
        
        with st.container():
            st.markdown(f"""
                <div class="upload-ready-card-marker"></div>
                <style>
                div[data-testid="stVerticalBlock"]:has(.upload-ready-card-marker):not(:has(div[data-testid="stVerticalBlock"]:has(.upload-ready-card-marker))) {{
                    background: var(--surface) !important;
                    border-radius: 20px !important;
                    padding: 2rem !important;
                    box-shadow: var(--shadow-soft) !important;
                    border: 1px solid #E2E8F0 !important;
                    margin-bottom: 2rem !important;
                    text-align: center !important;
                }}
                .upload-ready-card-marker {{ display: none; }}
                </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<div style='font-size: 3rem; margin-bottom: 1rem;'>📄</div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin-bottom: 0.5rem;'>{metadata.get('filename', 'Unknown File')}</h3>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="display: flex; justify-content: center; gap: 2rem; color: var(--text-muted); margin-bottom: 2rem;">
                <span>📦 {metadata.get('size_mb', '0')} MB</span>
                <span>⏱️ {metadata.get('duration', 'Unknown')}</span>
                <span>⚙️ {metadata.get('format', 'Unknown').upper()}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Check if this file is already processed
            file_hash = metadata.get('file_hash')
            db = next(get_db())
            existing_meeting = get_meeting_by_hash(db, file_hash) if file_hash else None
            
            if existing_meeting and existing_meeting.processing_status == "Completed":
                st.markdown("<span class='badge badge-completed' style='margin-bottom: 2rem;'>✓ Already Processed</span>", unsafe_allow_html=True)
                st.info("This meeting has already been analyzed. You can view the results directly.")
                
                col_spacer1, col1, col2, col_spacer2 = st.columns([1, 2, 2, 1])
                with col1:
                    if st.button("Cancel", type="secondary", use_container_width=True):
                        try: os.remove(st.session_state['current_upload'])
                        except: pass
                        del st.session_state['current_upload']
                        st.rerun()
                with col2:
                    if st.button("▶ View Results", type="primary", use_container_width=True):
                        st.session_state['current_meeting_id'] = existing_meeting.id
                        st.session_state['current_page'] = "Meeting Results"
                        st.rerun()
            else:
                st.markdown("<span class='badge badge-completed' style='margin-bottom: 2rem;'>✓ Validated & Ready</span>", unsafe_allow_html=True)
                
                col_spacer1, col1, col2, col_spacer2 = st.columns([1, 2, 2, 1])
                with col1:
                    if st.button("Cancel", type="secondary", use_container_width=True):
                        try: os.remove(st.session_state['current_upload'])
                        except: pass
                        del st.session_state['current_upload']
                        if 'upload_metadata' in st.session_state:
                            del st.session_state['upload_metadata']
                        st.rerun()
                with col2:
                    if st.button("▶ Start Transcription", type="primary", use_container_width=True):
                        st.session_state['current_page'] = "Processing"
                        st.rerun()
        return
        
    # Show Uploader
    extensions = [ext.replace('.', '') for ext in SUPPORTED_EXTENSIONS]
    
    with st.container():
        st.markdown(f"""
            <div class="uploader-card-marker"></div>
            <style>
            div[data-testid="stVerticalBlock"]:has(.uploader-card-marker):not(:has(div[data-testid="stVerticalBlock"]:has(.uploader-card-marker))) {{
                background: var(--surface) !important;
                border-radius: 20px !important;
                padding: 2rem !important;
                box-shadow: var(--shadow-soft) !important;
                border: 1px solid #E2E8F0 !important;
                margin-bottom: 2rem !important;
            }}
            .uploader-card-marker {{ display: none; }}
            </style>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Supported formats: " + " • ".join([ext.upper() for ext in extensions]),
            type=extensions
        )
    
    if uploaded_file is not None:
        temp_path = UPLOAD_DIR / uploaded_file.name
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        with st.spinner("Validating file..."):
            is_valid, error_msg = validate_file(str(temp_path))
            
        if not is_valid:
            st.error(f"Unable to process this meeting: {error_msg}")
            if temp_path.exists():
                os.remove(temp_path)
            return
            
        metadata = get_file_metadata(str(temp_path))
        metadata['file_hash'] = get_file_hash(str(temp_path))
        
        st.session_state['current_upload'] = str(temp_path)
        st.session_state['upload_metadata'] = metadata
        st.rerun()
