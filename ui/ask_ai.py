import streamlit as st
import json
from ai.meeting_analyzer import MeetingAnalyzer
from storage.database import get_db
from storage.models import TranscriptSegment, Meeting
from storage.repository import get_meeting
from transcription.formatter import generate_text_transcript
from ui.components import section_header

def render_ask_ai_tab(meeting_id):
    section_header("🤖 Ask the Meeting", "Ask any question about this meeting and AI will answer based on the transcript.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("E.g., What decisions were made?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                db = next(get_db())
                meeting = get_meeting(db, meeting_id)
                segments = db.query(TranscriptSegment).filter(TranscriptSegment.meeting_id == meeting_id).order_by(TranscriptSegment.start).all()
                
                if not segments:
                    message_placeholder.error("No transcript is available for this meeting.")
                    st.session_state.messages.append({"role": "assistant", "content": "No transcript is available for this meeting."})
                    return
                
                seg_dicts = [{"start": s.start, "end": s.end, "speaker": s.speaker, "text": s.text} for s in segments]
                full_transcript = generate_text_transcript(seg_dicts)
                
                # Fetch structured insights
                structured_insights = {
                    "summary": meeting.executive_summary or "",
                    "decisions": meeting.decisions,
                    "action_items": meeting.action_items,
                    "participants": meeting.participants,
                    "deadlines": meeting.deadlines,
                    "priorities": meeting.priorities
                }
                # Convert relational objects to strings for the prompt
                insights_str = f"Summary: {structured_insights['summary']}\n"
                
                with st.spinner("Thinking..."):
                    analyzer = MeetingAnalyzer()
                    response = analyzer.ask(full_transcript, prompt, json.dumps(insights_str))
                    
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Ask AI failed: {e}", exc_info=True)
                error_msg = "AI service is temporarily unavailable. Please try again."
                if "API key" in str(e) or "GEMINI_API_KEY" in str(e):
                    error_msg = "Gemini API key is not configured."
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
