import streamlit as st
import time
import os
from storage.database import get_db, SessionLocal
from storage.repository import create_meeting, update_meeting_status, save_transcript, get_meeting
from audio.processor import process_audio, cleanup_file
from transcription.whisper_engine import WhisperTranscriber
from transcription.diarization import SpeakerDiarizer
from transcription.alignment import align_transcript_with_speakers
from transcription.formatter import format_transcript, generate_text_transcript
from validation.transcript_validator import validate_transcript
from ai.meeting_analyzer import MeetingAnalyzer

from ui.components import page_header, error_state, safe_escape

def render_processing_page():
    page_header(
        title="AI Processing Pipeline",
        subtitle="Transcribing dialogue, identifying speakers, extracting decisions, and syncing action items.",
        category="Pipeline Execution",
        badge_text="In Progress",
        badge_type="accent",
        icon="sparkles"
    )
    
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
    
    # Pipeline UI Container
    st.markdown("""
        <div id="pipeline-ui" style="background: var(--mt-surface); border-radius: var(--mt-radius-xl); padding: var(--mt-space-xl); border: 1px solid var(--mt-border); box-shadow: var(--mt-shadow-card); margin-top: var(--mt-space-xl);">
            <div style="display: flex; flex-direction: column; gap: var(--mt-space-md);">
                <div id="step-audio" style="display: flex; align-items: center; gap: 12px; color: var(--mt-text-muted); font-weight: 500; font-size: 1rem;"><div style="width: 24px; height: 24px; border-radius: 50%; border: 2px solid var(--mt-border); display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">1</div> Audio extraction</div>
                <div id="step-whisper" style="display: flex; align-items: center; gap: 12px; color: var(--mt-text-muted); font-weight: 500; font-size: 1rem;"><div style="width: 24px; height: 24px; border-radius: 50%; border: 2px solid var(--mt-border); display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">2</div> Transcription</div>
                <div id="step-diarization" style="display: flex; align-items: center; gap: 12px; color: var(--mt-text-muted); font-weight: 500; font-size: 1rem;"><div style="width: 24px; height: 24px; border-radius: 50%; border: 2px solid var(--mt-border); display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">3</div> Speaker identification</div>
                <div id="step-ai" style="display: flex; align-items: center; gap: 12px; color: var(--mt-text-muted); font-weight: 500; font-size: 1rem;"><div style="width: 24px; height: 24px; border-radius: 50%; border: 2px solid var(--mt-border); display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">4</div> AI analysis</div>
                <div id="step-index" style="display: flex; align-items: center; gap: 12px; color: var(--mt-text-muted); font-weight: 500; font-size: 1rem;"><div style="width: 24px; height: 24px; border-radius: 50%; border: 2px solid var(--mt-border); display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">5</div> Knowledge indexing</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress UI
    progress_bar = st.progress(0)
    status_box = st.empty()
    st.write("")
    
    def update_pipeline(step_id, status="processing"):
        # Helper to update UI without raw HTML rewriting, just rely on streamlit native for now.
        pass
    
    # Check if already processing
    if 'processing_started' not in st.session_state:
        st.session_state['processing_started'] = True
        processed_wav = None
        db = SessionLocal()
        
        try:
            total_start_time = time.time()
            
            duration = metadata.get('duration_sec', 0.0)
            user_id = st.session_state.get('user_id')
            meeting = create_meeting(db, metadata.get('filename', 'Unknown'), user_id=user_id, duration=duration, file_hash=metadata.get('file_hash'))
            st.session_state['current_meeting_id'] = meeting.id
            
            # 2. Extract Audio
            t0 = time.time()
            progress_bar.progress(10, text="1/5 • Audio extraction")
            status_box.info("Preprocessing audio format...")
            processed_wav = process_audio(file_path)
            audio_time = time.time() - t0
            
            # 3. Whisper
            t0 = time.time()
            progress_bar.progress(30, text="2/5 • Transcription")
            status_box.info("Running AI Transcription (this may take a while)...")
            transcriber = WhisperTranscriber()
            whisper_segments = transcriber.transcribe(processed_wav)
            whisper_time = time.time() - t0
            
            # 4. Pyannote
            t0 = time.time()
            progress_bar.progress(60, text="3/5 • Speaker identification")
            status_box.info("Identifying distinct speakers...")
            diarizer = SpeakerDiarizer()
            speaker_segments = diarizer.diarize(processed_wav)
            diarization_time = time.time() - t0
            
            # 5. Alignment
            t0 = time.time()
            progress_bar.progress(80, text="Synchronizing data")
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
            progress_bar.progress(90, text="4/5 • AI analysis")
            status_box.info("Generating intelligent insights...")
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
            
            from storage.models import ActionItem, Decision, Participant, Deadline, Priority, MeetingAttendance, User
            from storage.repository import log_audit_event
            
            # Map known users in this org for accurate assignee linkage
            org_users = db.query(User).filter(User.org_id == meeting.org_id).all()
            user_map = {}
            for u in org_users:
                user_map[u.username.lower()] = u
                if u.full_name:
                    user_map[u.full_name.lower()] = u
                    for part in u.full_name.lower().split():
                        if len(part) > 2:
                            user_map[part] = u

            for ai in insights.get('action_items', []):
                raw_assigned = ai.get('assigned_to', 'Unassigned')
                matched_user = None
                assignment_status = ai.get('assignment_status', 'Assigned')
                
                # Check for employee match
                if raw_assigned and raw_assigned.lower() != "unassigned":
                    matched_user = user_map.get(raw_assigned.lower())
                    if not matched_user:
                        # Try first name matching
                        matched_user = user_map.get(raw_assigned.lower().split()[0])
                    
                    if matched_user:
                        assigned_name = matched_user.full_name or matched_user.username
                        assigned_user_id = matched_user.id
                        assignment_status = "Assigned"
                    else:
                        assigned_name = raw_assigned
                        assigned_user_id = None
                        assignment_status = "Needs assignment"
                else:
                    assigned_name = "Unassigned"
                    assigned_user_id = None
                    assignment_status = "Needs assignment"

                db.add(ActionItem(
                    meeting_id=meeting.id,
                    org_id=meeting.org_id,
                    task=ai['task'],
                    description=ai.get('description') or f"Action item identified from meeting dialogue: {ai.get('evidence_excerpt', '')}",
                    evidence_excerpt=ai.get('evidence_excerpt') or "",
                    assigned_to=assigned_name,
                    assigned_user_id=assigned_user_id,
                    assignment_status=assignment_status,
                    deadline=ai.get('deadline') or 'Not specified',
                    priority=ai.get('priority', 'Medium'),
                    status="Pending",
                    approval_status="Draft",
                    confidence=ai.get('confidence', 0.95),
                    dependencies=json.dumps(ai.get('dependencies', [])),
                    estimated_effort_hours=ai.get('estimated_effort_hours')
                ))
                
            for d in insights.get('decisions', []):
                db.add(Decision(
                    meeting_id=meeting.id,
                    org_id=meeting.org_id,
                    title=d.get('title') or d['decision'][:60],
                    decision=d['decision'],
                    context=d['context'],
                    rationale=d.get('rationale') or "Agreed by consensus during review.",
                    alternatives=d.get('alternatives') or "No alternative recorded.",
                    evidence_excerpt=d.get('evidence_excerpt') or "",
                    confidence=d.get('confidence', 0.95),
                    status=d.get('status', 'Approved'),
                    proposer=d.get('proposer', 'Team')
                ))
                
            for p in insights.get('participants', []):
                p_name = p.get('name', 'Unknown Participant')
                db.add(Participant(
                    meeting_id=meeting.id, 
                    name=p_name, 
                    speaker_id=p.get('speaker_id', 'Unknown'), 
                    responsibilities=json.dumps(p.get('responsibilities', []))
                ))
                # Add attendance record
                matched_p_user = user_map.get(p_name.lower())
                db.add(MeetingAttendance(
                    meeting_id=meeting.id,
                    user_id=matched_p_user.id if matched_p_user else None,
                    name=p_name,
                    email=matched_p_user.email if matched_p_user else f"{p_name.lower().replace(' ', '.')}@acmeglobal.io",
                    status="Attended",
                    verified_source="Meeting Dialogue Alignment"
                ))
                
            for dl in insights.get('deadlines', []):
                db.add(Deadline(meeting_id=meeting.id, description=dl['description'], date=dl['date'], related_task=dl['related_task']))
                
            for pr in insights.get('priorities', []):
                db.add(Priority(meeting_id=meeting.id, item=pr['item'], priority_level=pr['priority']))
                
            update_meeting_status(db, meeting.id, "Completed")
            db.commit()
            
            # Log audit event
            log_audit_event(
                db,
                org_id=meeting.org_id,
                user_id=meeting.user_id,
                actor_username=st.session_state.get('username', 'System'),
                entity_type="meeting",
                entity_id=meeting.id,
                action="UPDATE",
                details=f"Meeting '{meeting.title}' processed. Extracted {len(insights.get('action_items', []))} action items and {len(insights.get('decisions', []))} decisions."
            )
            db_time = time.time() - t0
            
            # 9. Index into Knowledge Base
            t0 = time.time()
            progress_bar.progress(95, text="5/5 • Knowledge indexing")
            status_box.info("Building semantic search vectors...")
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
            
            progress_bar.progress(100, text="Done!")
            status_box.success("Processing complete!")
            
            time.sleep(1)
            st.session_state['current_page'] = "Meeting Results"
            st.rerun()
            
        except Exception as e:
            progress_bar.progress(100, text="Error occurred")
            error_state("Pipeline Processing Interrupted", "Unable to complete meeting processing. Please verify audio format and try again.")
            import logging
            logging.getLogger(__name__).error(f"Processing failed: {e}", exc_info=True)
            if 'current_meeting_id' in st.session_state:
                try:
                    update_meeting_status(db, st.session_state['current_meeting_id'], "Failed")
                except Exception:
                    pass
            
            if st.button("Return to Dashboard", type="primary"):
                if 'processing_started' in st.session_state:
                    del st.session_state['processing_started']
                st.session_state['current_page'] = "Dashboard"
                st.rerun()
        finally:
            if processed_wav:
                cleanup_file(processed_wav)
            if file_path:
                cleanup_file(file_path)
            db.close()


