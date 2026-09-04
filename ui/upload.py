import streamlit as st
import os
import shutil
from pathlib import Path
from audio.validator import validate_file, get_file_metadata, SUPPORTED_EXTENSIONS

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def render_upload_page():
    st.header("Upload your meeting")
    st.markdown("Drop an audio or video file here to begin transcription and AI analysis.")
    
    # Configure file uploader
    extensions = [ext.replace('.', '') for ext in SUPPORTED_EXTENSIONS]
    
    uploaded_file = st.file_uploader(
        "Supported formats: " + " • ".join([ext.upper() for ext in extensions]),
        type=extensions
    )
    
    if uploaded_file is not None:
        # Save file temporarily to validate it
        temp_path = UPLOAD_DIR / uploaded_file.name
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # Validate
        with st.spinner("Validating file..."):
            is_valid, error_msg = validate_file(str(temp_path))
            
        if not is_valid:
            st.error(error_msg)
            # Clean up invalid file
            if temp_path.exists():
                os.remove(temp_path)
            return
            
        # File is valid, get metadata
        metadata = get_file_metadata(str(temp_path))
        
        # Display File Info
        st.success("File uploaded successfully!")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Filename", metadata['filename'])
        col2.metric("Size", f"{metadata['size_mb']} MB")
        col3.metric("Duration", metadata.get('duration', 'Unknown'))
        col4.metric("Format", metadata['format'])
        
        st.markdown("---")
        
        # Store in session state for processing
        st.session_state['current_upload'] = str(temp_path)
        st.session_state['upload_metadata'] = metadata
        
        if st.button("Start Transcription", type="primary", use_container_width=True):
            # Reset processing state for the new file
            if 'processing_started' in st.session_state:
                del st.session_state['processing_started']
            st.session_state['current_page'] = "Processing"
            st.rerun()

