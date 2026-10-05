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
                background: var(--mt-surface) !important;
                border-radius: var(--mt-radius-xl) !important;
                padding: var(--mt-space-2xl) !important;
                box-shadow: var(--mt-shadow-card) !important;
                border: 1px solid var(--mt-border) !important;
                margin-bottom: var(--mt-space-2xl) !important;
                text-align: center !important;
            }}
            .upload-ready-card-marker {{ display: none; }}
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<div style='font-size: 3rem; margin-bottom: 1rem;'>📄</div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin-bottom: 0.5rem; color: var(--mt-text); font-weight: 650;'>{metadata.get('filename', 'Unknown File')}</h3>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="display: flex; justify-content: center; gap: 2rem; color: var(--mt-text-secondary); margin-bottom: 2rem;">
                <span style="display: flex; align-items: center; gap: 6px;"><span style="color: var(--mt-primary);">📦</span> {metadata.get('size_mb', '0')} MB</span>
                <span style="display: flex; align-items: center; gap: 6px;"><span style="color: var(--mt-primary);">⏱️</span> {metadata.get('duration', 'Unknown')}</span>
                <span style="display: flex; align-items: center; gap: 6px;"><span style="color: var(--mt-primary);">⚙️</span> {metadata.get('format', 'Unknown').upper()}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Check if this file is already processed
            file_hash = metadata.get('file_hash')
            db = next(get_db())
            user_id = st.session_state.get('user_id')
            existing_meeting = get_meeting_by_hash(db, file_hash, user_id=user_id) if file_hash else None
            
            if existing_meeting and existing_meeting.processing_status == "Completed":
                st.markdown("<span class='badge badge-completed' style='margin-bottom: 2rem; box-shadow: var(--mt-shadow-soft);'>✓ Already Processed</span>", unsafe_allow_html=True)
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
                st.markdown("<span class='badge badge-completed' style='margin-bottom: 2rem; box-shadow: var(--mt-shadow-soft);'>✓ Validated & Ready</span>", unsafe_allow_html=True)
                
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
        
    # Add tabs for upload methods
    tab_upload, tab_zoom, tab_meet = st.tabs(["📁 Upload File", "🎥 Import from Zoom", "📅 Import from Google Meet"])
    
    with tab_upload:
        # Show Uploader
        extensions = [ext.replace('.', '') for ext in SUPPORTED_EXTENSIONS]
        
        with st.container():
            st.markdown(f"""
                <div class="uploader-card-marker"></div>
                <style>
                div[data-testid="stVerticalBlock"]:has(.uploader-card-marker):not(:has(div[data-testid="stVerticalBlock"]:has(.uploader-card-marker))) {{
                    background: var(--mt-surface) !important;
                    border-radius: var(--mt-radius-xl) !important;
                    padding: var(--mt-space-2xl) !important;
                    box-shadow: var(--mt-shadow-card) !important;
                    border: 1px solid var(--mt-border) !important;
                    margin-bottom: var(--mt-space-2xl) !important;
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
                st.stop()
                
            metadata = get_file_metadata(str(temp_path))
            metadata['file_hash'] = get_file_hash(str(temp_path))
            
            st.session_state['current_upload'] = str(temp_path)
            st.session_state['upload_metadata'] = metadata
            st.rerun()

    with tab_zoom:
        st.markdown("<h3 style='color: var(--mt-text); margin-bottom: 1rem;'>Connect to Zoom</h3>", unsafe_allow_html=True)
        st.info("Since this is a development environment without real Zoom credentials, importing a meeting will simulate a successful recording retrieval using a mock file.")
        
        meeting_id_input = st.text_input("Zoom Meeting ID or Link", placeholder="e.g. 123 456 7890")
        if st.button("Import Recording", type="primary", key="import_zoom"):
            if not meeting_id_input:
                st.error("Please enter a Meeting ID.")
            else:
                with st.spinner("Connecting to Zoom and downloading recording..."):
                    import time
                    time.sleep(2)  # Simulate network request
                    
                    # Use the sample wav file
                    sample_path = "sample_data/test_meeting.wav"
                    if not os.path.exists(sample_path) and os.path.exists("test_meeting.wav"):
                        sample_path = "test_meeting.wav"
                        
                    if os.path.exists(sample_path):
                        metadata = get_file_metadata(sample_path)
                        metadata['file_hash'] = get_file_hash(sample_path)
                        metadata['filename'] = f"Zoom_Meeting_{meeting_id_input}.wav"
                        st.session_state['current_upload'] = sample_path
                        st.session_state['upload_metadata'] = metadata
                        st.success("Successfully imported from Zoom!")
                        st.rerun()
                    else:
                        st.error("Mock recording file not found in repository.")
                        
    with tab_meet:
        st.markdown("<h3 style='color: var(--mt-text); margin-bottom: 1rem;'>Connect to Google Meet</h3>", unsafe_allow_html=True)
        st.info("Since this is a development environment without Google Workspace Service Account credentials, this action will simulate a Google Drive file download.")
        
        meet_link_input = st.text_input("Google Drive Recording Link", placeholder="https://drive.google.com/file/d/.../view")
        if st.button("Import Recording", type="primary", key="import_meet"):
            if not meet_link_input:
                st.error("Please enter a Google Drive link.")
            else:
                with st.spinner("Authenticating with Google Workspace and downloading recording..."):
                    import time
                    time.sleep(2)  # Simulate network request
                    
                    # Use the sample wav file
                    sample_path = "sample_data/test_meeting.wav"
                    if not os.path.exists(sample_path) and os.path.exists("test_meeting.wav"):
                        sample_path = "test_meeting.wav"
                        
                    if os.path.exists(sample_path):
                        metadata = get_file_metadata(sample_path)
                        metadata['file_hash'] = get_file_hash(sample_path)
                        metadata['filename'] = f"Google_Meet_Recording.wav"
                        st.session_state['current_upload'] = sample_path
                        st.session_state['upload_metadata'] = metadata
                        st.success("Successfully imported from Google Meet!")
                        st.rerun()
                    else:
                        st.error("Mock recording file not found in repository.")
