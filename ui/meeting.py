import streamlit as st
import time
import os
from storage.database import get_db
from storage.repository import create_meeting, update_meeting_status, save_transcript, get_meeting
from audio.processor import process_audio, cleanup_file
from transcription.whisper_engine import WhisperTranscriber
from transcription.diarization import SpeakerDiarizer
from transcription.alignment import align_transcript_with_speakers
from transcription.formatter import format_transcript, generate_text_transcript
from validation.transcript_validator import validate_transcript
from ai.meeting_analyzer import MeetingAnalyzer

def render_processing_page():
    st.title("Processing Meeting...")
    
    if 'current_upload' not in st.session_state:
        st.error("No file uploaded.")
        if st.button("Go Back"):
            st.session_state['current_page'] = "Dashboard"
            st.rerun()
        return
        
    file_path = st.session_state['current_upload']
    metadata = st.session_state.get('upload_metadata', {})
    
    # Progress UI
    progress_text = "Initializing processing..."
    progress_bar = st.progress(0, text=progress_text)
    status_box = st.empty()
    
    # Check if already processing
    if 'processing_started' not in st.session_state:
        st.session_state['processing_started'] = True
        
        try:
            # 1. DB Init
            db = next(get_db())
            duration = metadata.get('duration_sec', 0.0)
            meeting = create_meeting(db, metadata.get('filename', 'Unknown'), duration)
            st.session_state['current_meeting_id'] = meeting.id
            
            # 2. Extract Audio
            progress_bar.progress(10, text="Extracting and preprocessing audio with FFmpeg...")
            status_box.info("Running FFmpeg...")
            processed_wav = process_audio(file_path)
            
            # 3. Whisper
            progress_bar.progress(30, text="Transcribing with Whisper...")
            status_box.info("Running Whisper (this may take a while)...")
            transcriber = WhisperTranscriber()
            whisper_segments = transcriber.transcribe(processed_wav)
            
            # 4. Pyannote
            progress_bar.progress(60, text="Detecting speakers with Pyannote...")
            status_box.info("Running Speaker Diarization...")
            diarizer = SpeakerDiarizer()
            speaker_segments = diarizer.diarize(processed_wav)
            
            # 5. Alignment
            progress_bar.progress(80, text="Aligning transcript and speakers...")
            aligned_segments = align_transcript_with_speakers(whisper_segments, speaker_segments)
            
            # 6. Format and Validate
            clean_segments = format_transcript(aligned_segments, mode="Clean Verbatim")
            validation = validate_transcript(clean_segments)
            if validation["overall_status"] == "FAILED":
                st.warning("Transcript validation failed. Results may be inaccurate.")
                
            # 7. Save to DB
            save_transcript(db, meeting.id, clean_segments)
            
            # 8. AI Insights
            progress_bar.progress(90, text="Generating AI Insights...")
            status_box.info("Calling AI Provider...")
            text_transcript = generate_text_transcript(clean_segments)
            
            analyzer = MeetingAnalyzer()
            insights = analyzer.analyze(text_transcript)
            
            import json
            
            # Update DB with insights
            meeting.executive_summary = insights.get('executive_summary', '')
            meeting.meeting_objective = insights.get('meeting_objective', '')
            meeting.meeting_plan = insights.get('meeting_plan', '')
            meeting.emotional_analysis = insights.get('emotional_analysis', 'Neutral')
            meeting.key_topics = json.dumps(insights.get('key_topics', []))
            meeting.key_points = json.dumps(insights.get('key_points', []))
            meeting.risks = json.dumps(insights.get('risks', []))
            meeting.recommendations = json.dumps(insights.get('recommendations', []))
            meeting.next_steps = json.dumps(insights.get('next_steps', []))
            
            # Save Action Items and Decisions (omitting detailed DB persistence for brevity here, but handled in full app)
            from storage.models import ActionItem, Decision
            for ai in insights.get('action_items', []):
                db.add(ActionItem(meeting_id=meeting.id, task=ai['task'], owner=ai.get('owner', ''), deadline=ai.get('deadline', ''), priority=ai.get('priority', '')))
            for d in insights.get('decisions', []):
                db.add(Decision(meeting_id=meeting.id, decision=d['decision'], context=d['context']))
                
            update_meeting_status(db, meeting.id, "Completed")
            db.commit()
            
            # Cleanup temp files
            cleanup_file(processed_wav)
            cleanup_file(file_path)
            
            progress_bar.progress(100, text="Done!")
            status_box.success("Processing complete!")
            
            time.sleep(1)
            st.session_state['current_page'] = "Meeting Results"
            st.rerun()
            
        except Exception as e:
            progress_bar.progress(100, text="Error occurred")
            st.error(f"Something went wrong while processing the meeting.\n\nReason: {str(e)}")
            import logging
            logging.getLogger(__name__).error("Processing failed", exc_info=True)
            if 'current_meeting_id' in st.session_state:
                update_meeting_status(next(get_db()), st.session_state['current_meeting_id'], "Failed")
            
            if st.button("Go Back"):
                if 'processing_started' in st.session_state:
                    del st.session_state['processing_started']
                st.session_state['current_page'] = "Dashboard"
                st.rerun()

