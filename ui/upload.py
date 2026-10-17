import streamlit as st
import os
import hashlib
from pathlib import Path
from audio.validator import validate_file, get_file_metadata, SUPPORTED_EXTENSIONS
from ui.components import page_header, render_status_badge, safe_escape, get_icon_svg
from storage.database import SessionLocal
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
    page_header(
        title="Process New Meeting",
        subtitle="Upload recordings or import from your connected conferencing tools for automated transcription and action item extraction.",
        category="Ingestion & Processing",
        badge_text="Multi-Format Pipeline",
        badge_type="accent",
        icon="upload"
    )
    
    # Check if we already have a validated file in session state for this visit
    if 'current_upload' in st.session_state and Path(st.session_state['current_upload']).exists() and 'processing_started' not in st.session_state:
        metadata = st.session_state.get('upload_metadata', {})
        file_hash = metadata.get('file_hash')
        
        # Check if this file is already processed
        existing_meeting = None
        db = SessionLocal()
        try:
            user_id = st.session_state.get('user_id')
            if file_hash:
                existing_meeting = get_meeting_by_hash(db, file_hash, user_id=user_id)
        finally:
            db.close()
        
        with st.container(border=True):
            mic_svg = get_icon_svg("mic", size=32, color="#6C4DFF")
            st.markdown(f"""
                <div style="text-align: center; padding: 16px 0 4px 0;">
                    <div style="width: 56px; height: 56px; border-radius: 50%; background: var(--mt-primary-light); display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto;">
                        {mic_svg}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<h3 style='text-align: center; margin: 0 0 8px 0; color: var(--mt-text); font-weight: 700; font-size: 1.25rem;'>{safe_escape(metadata.get('filename', 'Audio Recording'))}</h3>", unsafe_allow_html=True)
            
            # File specs row
            st.markdown(f"""
            <div style="display: flex; justify-content: center; gap: 1.5rem; color: var(--mt-text-secondary); margin-bottom: 1.25rem; flex-wrap: wrap;">
                <span style="display: inline-flex; align-items: center; gap: 6px; font-size: 0.88rem;"><strong style="color: var(--mt-text);">Size:</strong> {metadata.get('size_mb', '0')} MB</span>
                <span style="display: inline-flex; align-items: center; gap: 6px; font-size: 0.88rem;"><strong style="color: var(--mt-text);">Duration:</strong> {metadata.get('duration', 'Unknown')}</span>
                <span style="display: inline-flex; align-items: center; gap: 6px; font-size: 0.88rem;"><strong style="color: var(--mt-text);">Format:</strong> {metadata.get('format', 'audio').upper()}</span>
            </div>
            """, unsafe_allow_html=True)
            
            if existing_meeting and existing_meeting.processing_status == "Completed":
                st.markdown(f"<div style='text-align: center; margin-bottom: 1rem;'>{render_status_badge('Already Processed', 'status')}</div>", unsafe_allow_html=True)
                st.info("This exact meeting audio has already been processed and analyzed. You can view the results directly.")
                
                col_spacer1, col1, col2, col_spacer2 = st.columns([1, 2, 2, 1])
                with col1:
                    if st.button("Cancel & Select Another", type="secondary", use_container_width=True):
                        try: os.remove(st.session_state['current_upload'])
                        except: pass
                        del st.session_state['current_upload']
                        st.rerun()
                with col2:
                    if st.button("▶ View Meeting Results", type="primary", use_container_width=True):
                        st.session_state['current_meeting_id'] = existing_meeting.id
                        st.session_state['current_page'] = "Meeting Results"
                        st.rerun()
            else:
                st.markdown(f"<div style='text-align: center; margin-bottom: 1.25rem;'>{render_status_badge('Validated & Ready', 'status')}</div>", unsafe_allow_html=True)
                
                col_spacer1, col1, col2, col_spacer2 = st.columns([1, 2, 2, 1])
                with col1:
                    if st.button("Cancel & Remove File", type="secondary", use_container_width=True):
                        try: os.remove(st.session_state['current_upload'])
                        except: pass
                        del st.session_state['current_upload']
                        if 'upload_metadata' in st.session_state:
                            del st.session_state['upload_metadata']
                        st.rerun()
                with col2:
                    if st.button("▶ Start AI Processing", type="primary", use_container_width=True):
                        st.session_state['current_page'] = "Processing"
                        st.rerun()
        return
        
    # Ingestion Methods Tabs
    tab_upload, tab_zoom, tab_meet = st.tabs(["📁 Direct File Upload", "🎥 Import from Zoom", "📅 Import from Google Meet"])
    
    with tab_upload:
        extensions = [ext.replace('.', '') for ext in SUPPORTED_EXTENSIONS]
        
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 4px 0; font-weight: 700; font-size: 1.05rem;'>Audio / Video File Ingestion</h4>", unsafe_allow_html=True)
        st.caption(f"Accepted formats: {', '.join([ext.upper() for ext in extensions])} • Up to 250 MB")
        
        uploaded_file = st.file_uploader(
            "Upload audio/video meeting recording",
            type=extensions,
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            temp_path = UPLOAD_DIR / uploaded_file.name
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            with st.spinner("Validating audio stream and metadata integrity..."):
                is_valid, error_msg = validate_file(str(temp_path))
                
            if not is_valid:
                st.error(f"Unable to process this file: {error_msg}")
                if temp_path.exists():
                    os.remove(temp_path)
                st.stop()
                
            metadata = get_file_metadata(str(temp_path))
            metadata['file_hash'] = get_file_hash(str(temp_path))
            
            st.session_state['current_upload'] = str(temp_path)
            st.session_state['upload_metadata'] = metadata
            st.rerun()

    with tab_zoom:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 6px 0; font-weight: 700; font-size: 1.05rem;'>🎥 Zoom Cloud Recording Import</h4>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-bottom: 12px;'>{render_status_badge('Sandbox Mode', 'demo')}</div>", unsafe_allow_html=True)
        st.info("In this demonstration environment without live Zoom OAuth production credentials, entering a Meeting ID will simulate a cloud recording fetch using a verified reference sample.")
        
        col_z1, col_z2 = st.columns([3, 1])
        with col_z1:
            meeting_id_input = st.text_input("Zoom Meeting ID or Recording URL", placeholder="e.g. 849 2014 9912", label_visibility="collapsed")
        with col_z2:
            import_zoom_clicked = st.button("Import Recording", type="primary", key="import_zoom", use_container_width=True)
            
        if import_zoom_clicked:
            if not meeting_id_input.strip():
                st.error("Please enter a Zoom Meeting ID or Link.")
            else:
                with st.spinner("Connecting to Zoom Cloud API and retrieving recording artifact..."):
                    import time
                    time.sleep(1.5)
                    
                    sample_path = "sample_data/test_meeting.wav"
                    if not os.path.exists(sample_path) and os.path.exists("test_meeting.wav"):
                        sample_path = "test_meeting.wav"
                        
                    if os.path.exists(sample_path):
                        metadata = get_file_metadata(sample_path)
                        metadata['file_hash'] = get_file_hash(sample_path)
                        metadata['filename'] = f"Zoom_Meeting_{meeting_id_input.strip().replace(' ', '_')}.wav"
                        st.session_state['current_upload'] = sample_path
                        st.session_state['upload_metadata'] = metadata
                        st.toast("Successfully retrieved Zoom cloud recording!")
                        st.rerun()
                    else:
                        st.error("Reference audio sample not found in repository.")
                        
    with tab_meet:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 6px 0; font-weight: 700; font-size: 1.05rem;'>📅 Google Meet / Drive Recording Import</h4>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-bottom: 12px;'>{render_status_badge('Sandbox Mode', 'demo')}</div>", unsafe_allow_html=True)
        st.info("In this demonstration environment without a Google Workspace enterprise service account, entering a Google Drive link will simulate a Drive recording fetch using a verified reference sample.")
        
        col_g1, col_g2 = st.columns([3, 1])
        with col_g1:
            meet_link_input = st.text_input("Google Drive Recording Link", placeholder="https://drive.google.com/file/d/.../view", label_visibility="collapsed")
        with col_g2:
            import_meet_clicked = st.button("Import Recording", type="primary", key="import_meet", use_container_width=True)
            
        if import_meet_clicked:
            if not meet_link_input.strip():
                st.error("Please enter a Google Drive recording link.")
            else:
                with st.spinner("Connecting to Google Drive API and retrieving recording stream..."):
                    import time
                    time.sleep(1.5)
                    
                    sample_path = "sample_data/test_meeting.wav"
                    if not os.path.exists(sample_path) and os.path.exists("test_meeting.wav"):
                        sample_path = "test_meeting.wav"
                        
                    if os.path.exists(sample_path):
                        metadata = get_file_metadata(sample_path)
                        metadata['file_hash'] = get_file_hash(sample_path)
                        metadata['filename'] = "Google_Meet_Enterprise_Review.wav"
                        st.session_state['current_upload'] = sample_path
                        st.session_state['upload_metadata'] = metadata
                        st.toast("Successfully retrieved Google Meet recording!")
                        st.rerun()
                    else:
                        st.error("Reference audio sample not found in repository.")
