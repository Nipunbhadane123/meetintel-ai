import streamlit as st
from ai.meeting_analyzer import MeetingAnalyzer
from ui.components import section_header
import logging
import concurrent.futures

logger = logging.getLogger(__name__)

def render_ask_ai_tab(meeting_id):
    st.markdown("""
        <div style="margin-bottom: var(--mt-space-md);">
            <h3 style="margin-top: 0; margin-bottom: 4px; font-weight: 650; color: var(--mt-text);">✨ Ask the Meeting</h3>
            <p style="color: var(--mt-text-secondary); font-size: 0.95rem;">Ask any question about this meeting and AI will answer based on the knowledge base.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if "ask_ai_messages" not in st.session_state:
        st.session_state.ask_ai_messages = []

    # Render chat messages
    for message in st.session_state.ask_ai_messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; gap: var(--mt-space-md); margin-bottom: var(--mt-space-md); padding-left: 20%; justify-content: flex-end;">
                <div style="background: var(--mt-surface-soft); padding: 12px 18px; border-radius: 20px; border-top-right-radius: 4px; border: 1px solid rgba(109,61,245,0.15); line-height: 1.5; color: var(--mt-text); box-shadow: var(--mt-shadow-soft);">
                    {message["content"]}
                </div>
                <div style="flex-shrink: 0; width: 32px; height: 32px; background: var(--mt-grad-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 0.8rem; box-shadow: var(--mt-shadow-soft);">U</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; gap: var(--mt-space-md); margin-bottom: var(--mt-space-md); padding-right: 15%;">
                <div style="flex-shrink: 0; width: 32px; height: 32px; background: var(--mt-surface); border-radius: 50%; border: 1px solid var(--mt-border); display: flex; align-items: center; justify-content: center; font-size: 1rem; color: var(--mt-primary); box-shadow: var(--mt-shadow-soft);">✧</div>
                <div style="background: var(--mt-surface); padding: 16px 20px; border-radius: 20px; border-top-left-radius: 4px; box-shadow: var(--mt-shadow-soft); border: 1px solid var(--mt-border); line-height: 1.6; width: 100%;">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if "status" in message and message["status"] == "LLM_UNAVAILABLE":
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("🔄 Retry AI Answer", key=f"retry_askai_{id(message)}"):
                        if st.session_state.ask_ai_messages[-1]["role"] == "assistant":
                            st.session_state.ask_ai_messages.pop()
                        st.rerun()
            
            if "sources" in message and message["sources"]:
                with st.expander(f"Found {len(message['sources'])} supporting sources"):
                    for i, src in enumerate(message["sources"]):
                        st.markdown(f"""
                        <div style="background: var(--mt-bg); border: 1px solid var(--mt-border); border-radius: var(--mt-radius-sm); padding: var(--mt-space-sm) var(--mt-space-md); margin-bottom: var(--mt-space-sm);">
                            <div style="font-weight: 600; font-size: 0.85rem; color: var(--mt-primary); margin-bottom: 4px;">Source {i+1}: {src.get('content_type', 'Unknown').capitalize()}</div>
                            <div style="font-size: 0.85rem; color: var(--mt-text); line-height: 1.4;">"...{src.get('excerpt', src.get('content', ''))[:150]}..."</div>
                        </div>
                        """, unsafe_allow_html=True)

    if prompt := st.chat_input("E.g., What decisions were made?"):
        if not prompt.strip():
            st.warning("Please enter a question.")
            return

        st.session_state.ask_ai_messages.append({"role": "user", "content": prompt})
        st.rerun()

    # If last message was user, generate response
    if st.session_state.ask_ai_messages and st.session_state.ask_ai_messages[-1]["role"] == "user":
        prompt = st.session_state.ask_ai_messages[-1]["content"]
        
        with st.spinner("✨ MeetIntel is thinking... retrieving knowledge and analyzing context."):
            analyzer = MeetingAnalyzer()
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(analyzer.rag_ask, prompt, meeting_id=meeting_id)
                    response = future.result()  # Rely on RAGService internal timeouts
                
                answer = response.get("answer", "Error generating answer.")
                sources = response.get("sources", [])
                status = response.get("status", "UNKNOWN")
                
                if not response.get("generation_success", True):
                    answer = "Relevant meeting knowledge found.\n\nAI generation is temporarily unavailable, but you can explore the retrieved sources below."
                
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
                    "content": "AI service is temporarily busy. Please try again in a moment.",
                    "status": "ERROR"
                })
                st.rerun()
