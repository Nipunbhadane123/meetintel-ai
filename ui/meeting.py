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

from ui.components import section_header

def render_processing_page():
    section_header("⚙️ Analyzing Your Meeting", "Please wait while our AI processes your audio")
    
    if 'current_upload' not in st.session_state:
        st.error("No file uploaded.")
        if st.button("Go Back"):
            st.session_state['current_page'] = "Dashboard"
            st.rerun()
        return
        
    file_path = st.session_state['current_upload']
    metadata = st.session_state.get('upload_metadata', {})
    
    st.write("")
    st.markdown(f"**Processing:** `{metadata.get('filename', 'Unknown')}`")
    
    # Progress UI
    progress_bar = st.progress(0)
    status_box = st.empty()
    st.write("")
    
    # Check if already processing
    if 'processing_started' not in st.session_state:
        st.session_state['processing_started'] = True
        
        try:
            total_start_time = time.time()
            
            # 1. DB Init
            db = next(get_db())
            duration = metadata.get('duration_sec', 0.0)
            meeting = create_meeting(db, metadata.get('filename', 'Unknown'), duration, metadata.get('file_hash'))
            st.session_state['current_meeting_id'] = meeting.id
            
            # 2. Extract Audio
            t0 = time.time()
            progress_bar.progress(10, text="Extracting and preprocessing audio with FFmpeg...")
            status_box.info("Running FFmpeg...")
            processed_wav = process_audio(file_path)
            audio_time = time.time() - t0
            
            # 3. Whisper
            t0 = time.time()
            progress_bar.progress(30, text="Transcribing with Whisper...")
            status_box.info("Running Whisper (this may take a while)...")
            transcriber = WhisperTranscriber()
            whisper_segments = transcriber.transcribe(processed_wav)
            whisper_time = time.time() - t0
            
            # 4. Pyannote
            t0 = time.time()
            progress_bar.progress(60, text="Detecting speakers with Pyannote...")
            status_box.info("Running Speaker Diarization...")
            diarizer = SpeakerDiarizer()
            speaker_segments = diarizer.diarize(processed_wav)
            diarization_time = time.time() - t0
            
            # 5. Alignment
            t0 = time.time()
            progress_bar.progress(80, text="Aligning transcript and speakers...")
            aligned_segments = align_transcript_with_speakers(whisper_segments, speaker_segments)
            
            # 6. Format and Validate
            clean_segments = format_transcript(aligned_segments, mode="Clean Verbatim")
            validation = validate_transcript(clean_segments)
            if validation["overall_status"] == "FAILED":
                st.warning("Transcript validation failed. Results may be inaccurate.")
                
            # 7. Save to DB
            save_transcript(db, meeting.id, clean_segments)
            alignment_db_time = time.time() - t0
            
            # 8. AI Insights
            t0 = time.time()
            progress_bar.progress(90, text="Generating AI Insights...")
            status_box.info("Calling AI Provider...")
            text_transcript = generate_text_transcript(clean_segments)
            
            analyzer = MeetingAnalyzer()
            insights = analyzer.analyze(text_transcript)
            llm_time = time.time() - t0
            
            import json
            
            # Update DB with insights
            t0 = time.time()
            meeting.executive_summary = insights.get('summary', '') or insights.get('executive_summary', '')
            meeting.meeting_objective = insights.get('meeting_objective', '')
            meeting.meeting_plan = insights.get('meeting_plan', '')
            meeting.emotional_analysis = insights.get('emotional_analysis', 'Neutral')
            meeting.key_topics = json.dumps(insights.get('key_topics', []))
            meeting.key_points = json.dumps(insights.get('key_points', []))
            meeting.risks = json.dumps(insights.get('risks', []))
            meeting.recommendations = json.dumps(insights.get('recommendations', []))
            meeting.next_steps = json.dumps(insights.get('next_steps', []))
            
            from storage.models import ActionItem, Decision, Participant, Deadline, Priority
            
            for ai in insights.get('action_items', []):
                db.add(ActionItem(
                    meeting_id=meeting.id, 
                    task=ai['task'], 
                    assigned_to=ai.get('assigned_to', 'Unassigned'), 
                    deadline=ai.get('deadline') or 'Not specified', 
                    priority=ai.get('priority', 'Medium'),
                    status=ai.get('status', 'Pending')
                ))
                
            for d in insights.get('decisions', []):
                db.add(Decision(meeting_id=meeting.id, decision=d['decision'], context=d['context']))
                
            for p in insights.get('participants', []):
                db.add(Participant(
                    meeting_id=meeting.id, 
                    name=p.get('name', 'Unknown Participant'), 
                    speaker_id=p.get('speaker_id', 'Unknown'), 
                    responsibilities=json.dumps(p.get('responsibilities', []))
                ))
                
            for dl in insights.get('deadlines', []):
                db.add(Deadline(meeting_id=meeting.id, description=dl['description'], date=dl['date'], related_task=dl['related_task']))
                
            for pr in insights.get('priorities', []):
                db.add(Priority(meeting_id=meeting.id, item=pr['item'], priority_level=pr['priority']))
                
            update_meeting_status(db, meeting.id, "Completed")
            db.commit()
            db_time = time.time() - t0
            
            # 9. Index into Knowledge Base
            t0 = time.time()
            progress_bar.progress(95, text="Indexing into Knowledge Base...")
            status_box.info("Generating embeddings...")
            from storage.knowledge import get_knowledge_repository
            repo = get_knowledge_repository()
            repo.index_meeting(meeting.id)
            index_time = time.time() - t0            
            total_time = time.time() - total_start_time
            
            # Save metrics to session state to display later if needed
            st.session_state['last_metrics'] = {
                "audio": audio_time,
                "whisper": whisper_time,
                "diarization": diarization_time,
                "alignment": alignment_db_time,
                "llm": llm_time,
                "db": db_time,
                "total": total_time
            }
            
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
            st.markdown(f"""
            <div class="saas-card" style="border-left: 4px solid var(--mt-error);">
                <h3 style="color: var(--mt-error); margin-top: 0;">Something went wrong</h3>
                <p style="color: var(--mt-text-muted); margin-bottom: 1rem;">We couldn't process this meeting.</p>
                <div style="background: #F1F5F9; padding: 1rem; border-radius: 8px; font-family: monospace; font-size: 0.8rem; margin-bottom: 1rem;">
                    {str(e)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            import logging
            logging.getLogger(__name__).error("Processing failed", exc_info=True)
            if 'current_meeting_id' in st.session_state:
                update_meeting_status(next(get_db()), st.session_state['current_meeting_id'], "Failed")
            
            if st.button("Retry", type="secondary"):
                if 'processing_started' in st.session_state:
                    del st.session_state['processing_started']
                st.session_state['current_page'] = "Dashboard"
                st.rerun()

