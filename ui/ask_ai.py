import streamlit as st
import logging
import concurrent.futures
from ai.meeting_analyzer import MeetingAnalyzer
from ui.components import safe_escape, render_status_badge, get_icon_svg

logger = logging.getLogger(__name__)

def render_ask_ai_tab(meeting_id):
    spark_icon = get_icon_svg("sparkles", size=18, color="#6C4DFF")
    st.markdown(f"""
        <div style="margin-bottom: var(--mt-space-md);">
            <h3 style="margin-top: 0; margin-bottom: 4px; font-weight: 700; color: var(--mt-text); display: flex; align-items: center; gap: 8px;">{spark_icon} Ask the Meeting</h3>
            <p style="color: var(--mt-text-secondary); font-size: 0.92rem; margin: 0;">Query this specific session using grounded retrieval. Every answer is linked to verbatim dialogue evidence.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if "ask_ai_messages" not in st.session_state:
        st.session_state.ask_ai_messages = []

    user_name = st.session_state.get('username', 'User')
    initial = (user_name[0] if user_name else "U").upper()

    # Render chat messages
    for message in st.session_state.ask_ai_messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; gap: 12px; margin-bottom: 16px; padding-left: 15%; justify-content: flex-end;">
                <div style="background: var(--mt-primary-light); padding: 12px 18px; border-radius: var(--mt-radius-lg); border-top-right-radius: 2px; border: 1px solid rgba(108, 76, 241, 0.2); line-height: 1.5; color: var(--mt-text); box-shadow: var(--mt-shadow-soft); font-size: 0.94rem;">
                    {safe_escape(message["content"])}
                </div>
                <div style="flex-shrink: 0; width: 32px; height: 32px; background: var(--mt-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-weight: 700; font-size: 0.85rem; box-shadow: var(--mt-shadow-soft);">{safe_escape(initial)}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            bot_icon = get_icon_svg("sparkles", size=16, color="#6C4DFF")
            st.markdown(f"""
            <div style="display: flex; gap: 12px; margin-bottom: 16px; padding-right: 10%;">
                <div style="flex-shrink: 0; width: 32px; height: 32px; background: var(--mt-surface); border-radius: 50%; border: 1px solid var(--mt-border); display: flex; align-items: center; justify-content: center; color: var(--mt-primary); box-shadow: var(--mt-shadow-soft);">{bot_icon}</div>
                <div style="background: var(--mt-surface); padding: 16px 20px; border-radius: var(--mt-radius-lg); border-top-left-radius: 2px; box-shadow: var(--mt-shadow-card); border: 1px solid var(--mt-border); line-height: 1.6; width: 100%; font-size: 0.94rem; color: var(--mt-text);">
                    {safe_escape(message["content"])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if "status" in message and message["status"] == "LLM_UNAVAILABLE":
                col1, col2 = st.columns([1.5, 3.5])
                with col1:
                    if st.button("🔄 Retry AI Answer", key=f"retry_askai_{id(message)}", type="secondary"):
                        if st.session_state.ask_ai_messages and st.session_state.ask_ai_messages[-1]["role"] == "assistant":
                            st.session_state.ask_ai_messages.pop()
                        st.rerun()
            
            if "sources" in message and message["sources"]:
                with st.expander(f"🔍 Grounded In {len(message['sources'])} Verified Transcript Excerpts"):
                    for i, src in enumerate(message["sources"]):
                        content_type = safe_escape(src.get('content_type', 'Transcript Segment')).capitalize()
                        raw_excerpt = src.get('excerpt') or src.get('content') or ''
                        clean_excerpt = safe_escape(raw_excerpt[:200])
                        st.markdown(f"""
                        <div style="background: var(--mt-bg); border: 1px solid var(--mt-border); border-left: 3px solid var(--mt-primary); border-radius: var(--mt-radius-sm); padding: 8px 12px; margin-bottom: 8px;">
                            <div style="font-weight: 700; font-size: 0.76rem; color: var(--mt-primary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">Citation {i+1} • {content_type}</div>
                            <div style="font-size: 0.86rem; color: var(--mt-text); font-style: italic; line-height: 1.4;">"...{clean_excerpt}..."</div>
                        </div>
                        """, unsafe_allow_html=True)

    if prompt := st.chat_input("E.g., What decisions or deadlines were committed in this session?"):
        if not prompt.strip():
            st.warning("Please enter a question.")
            return

        st.session_state.ask_ai_messages.append({"role": "user", "content": prompt})
        st.rerun()

    # If last message was user, generate response
    if st.session_state.ask_ai_messages and st.session_state.ask_ai_messages[-1]["role"] == "user":
        prompt = st.session_state.ask_ai_messages[-1]["content"]
        
        with st.spinner("✨ Synthesizing answer grounded in meeting transcripts..."):
            analyzer = MeetingAnalyzer()
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    user_id = st.session_state.get('user_id')
                    future = executor.submit(analyzer.rag_ask, prompt, user_id=user_id, meeting_id=meeting_id)
                    response = future.result()
                
                answer = response.get("answer", "No response generated.")
                sources = response.get("sources", [])
                status = response.get("status", "UNKNOWN")
                
                if not response.get("generation_success", True):
                    answer = "Relevant meeting dialogue was retrieved, but generative synthesis is temporarily busy. Please inspect the verified transcript citations below."
                
                st.session_state.ask_ai_messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": sources,
                    "status": status,
                    "error_type": response.get("error_type")
                })
                st.rerun()
                
            except Exception as e:
                logger.error(f"Ask AI failed: {e}", exc_info=True)
                st.session_state.ask_ai_messages.append({
                    "role": "assistant",
                    "content": "Meeting knowledge service is temporarily busy. Please try asking again in a moment.",
                    "status": "ERROR"
                })
                st.rerun()
