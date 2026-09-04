import streamlit as st
from ai.meeting_analyzer import MeetingAnalyzer
from storage.database import get_db
from storage.models import TranscriptSegment
from transcription.formatter import generate_text_transcript

def render_ask_ai_tab(meeting_id):
    st.header("Ask the Meeting")
    st.markdown("Ask any question about this meeting and AI will answer based on the transcript.")
    
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
            
            # Get Transcript
            db = next(get_db())
            segments = db.query(TranscriptSegment).filter(TranscriptSegment.meeting_id == meeting_id).order_by(TranscriptSegment.start).all()
            
            # Format to dict format for the formatter
            seg_dicts = [{"start": s.start, "end": s.end, "speaker": s.speaker, "text": s.text} for s in segments]
            full_transcript = generate_text_transcript(seg_dicts)
            
            with st.spinner("Thinking..."):
                analyzer = MeetingAnalyzer()
                response = analyzer.ask(full_transcript, prompt)
                
            message_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
