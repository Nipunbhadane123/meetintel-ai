import streamlit as st
from ai.meeting_analyzer import MeetingAnalyzer
from storage.knowledge import get_knowledge_repository
from storage.database import get_db, SessionLocal
from storage.models import Meeting
import concurrent.futures

def render_knowledge_search_page():
    # Header
    st.markdown("""
        <div class="page-title-container" style="border-bottom: none; padding-bottom: 0;">
            <h2 class="page-title" style="margin-bottom: 4px;"><span style="color: var(--mt-primary);">✧</span> Knowledge Search</h2>
            <p class="page-subtitle">Search across your meeting knowledge using semantic search and grounded AI.</p>
        </div>
    """, unsafe_allow_html=True)
    
    repo = get_knowledge_repository()
    db = SessionLocal()
    total_meetings = db.query(Meeting).count()
    db.close()
    
    try:
        total_vectors = repo.vector_store.collection.count()
    except Exception:
        total_vectors = 0
        
    search_mode = st.session_state.get("search_mode_state", "Ask AI")
    
    # Custom compact stats row
    st.markdown(f"""
        <div style="display: flex; gap: var(--mt-space-md); margin-bottom: var(--mt-space-xl);">
            <div style="background: var(--mt-surface); border: 1px solid var(--mt-border); border-radius: var(--mt-radius-md); padding: var(--mt-space-sm) var(--mt-space-md); flex: 1; max-width: 150px; box-shadow: var(--mt-shadow-soft);">
                <div style="font-size: 0.7rem; color: var(--mt-text-muted); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;">Meetings</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: var(--mt-text);">{total_meetings}</div>
            </div>
            <div style="background: var(--mt-surface); border: 1px solid var(--mt-border); border-radius: var(--mt-radius-md); padding: var(--mt-space-sm) var(--mt-space-md); flex: 1; max-width: 150px; box-shadow: var(--mt-shadow-soft);">
                <div style="font-size: 0.7rem; color: var(--mt-text-muted); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;">Vectors</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: var(--mt-text);">{total_vectors}</div>
            </div>
            <div style="background: var(--mt-surface); border: 1px solid var(--mt-border); border-radius: var(--mt-radius-md); padding: var(--mt-space-sm) var(--mt-space-md); flex: 1; max-width: 150px; box-shadow: var(--mt-shadow-soft);">
                <div style="font-size: 0.7rem; color: var(--mt-text-muted); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;">Mode</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: var(--mt-primary);">{search_mode.upper()}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Segmented Control using columns and buttons
    col1, col2, _ = st.columns([1, 1, 3])
    with col1:
        if st.button("✨ Ask AI", use_container_width=True, type="primary" if search_mode == "Ask AI" else "secondary"):
            st.session_state.search_mode_state = "Ask AI"
            st.rerun()
    with col2:
        if st.button("🔎 Semantic Search", use_container_width=True, type="primary" if search_mode == "Semantic" else "secondary"):
            st.session_state.search_mode_state = "Semantic"
            st.rerun()
            
    st.markdown("<div style='height: var(--mt-space-md);'></div>", unsafe_allow_html=True)

    if search_mode == "Ask AI":
        if "global_ask_ai_messages" not in st.session_state:
            st.session_state.global_ask_ai_messages = []

        if not st.session_state.global_ask_ai_messages:
            st.markdown("""
            <div style="text-align: center; padding: var(--mt-space-2xl) var(--mt-space-lg); background: transparent; margin: var(--mt-space-xl) 0;">
                <div style="font-size: 3rem; margin-bottom: var(--mt-space-md); color: var(--mt-primary);">✧</div>
                <h4 style="color: var(--mt-text); font-weight: 600; margin-bottom: var(--mt-space-sm); font-size: 1.5rem;">Ask your meeting knowledge</h4>
                <div style="display: flex; flex-direction: column; gap: var(--mt-space-xs); max-width: 400px; margin: 0 auto; color: var(--mt-text-secondary); font-size: 0.95rem;">
                    <div style="background: var(--mt-surface); border: 1px solid var(--mt-border); padding: var(--mt-space-sm) var(--mt-space-md); border-radius: var(--mt-radius-lg); box-shadow: var(--mt-shadow-soft);">"Find decisions about database migration"</div>
                    <div style="background: var(--mt-surface); border: 1px solid var(--mt-border); padding: var(--mt-space-sm) var(--mt-space-md); border-radius: var(--mt-radius-lg); box-shadow: var(--mt-shadow-soft);">"Which meeting discussed the launch?"</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Render chat messages
        for message in st.session_state.global_ask_ai_messages:
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
                    if st.button("🔄 Retry AI Answer", key=f"retry_global_{id(message)}"):
                        # Remove the failed assistant message so the last message becomes the user query again
                        if st.session_state.global_ask_ai_messages[-1]["role"] == "assistant":
                            st.session_state.global_ask_ai_messages.pop()
                        st.rerun()

            if "sources" in message and message["sources"]:
                    with st.expander(f"Found {len(message['sources'])} supporting sources"):
                        for i, src in enumerate(message["sources"]):
                            st.markdown(f"""
                            <div style="background: var(--mt-bg); border: 1px solid var(--mt-border); border-radius: var(--mt-radius-sm); padding: var(--mt-space-sm) var(--mt-space-md); margin-bottom: var(--mt-space-sm);">
                                <div style="font-weight: 600; font-size: 0.85rem; color: var(--mt-primary); margin-bottom: 4px;">Source {i+1}: {src.get('meeting_title', 'Unknown')}</div>
                                <div style="font-size: 0.75rem; color: var(--mt-text-muted); margin-bottom: 8px;">Type: {src.get('content_type', 'Unknown')}</div>
                                <div style="font-size: 0.85rem; color: var(--mt-text); line-height: 1.4;">"...{src.get('excerpt', src.get('content', ''))[:150]}..."</div>
                            </div>
                            """, unsafe_allow_html=True)

        if prompt := st.chat_input("Ask anything about your meetings..."):
            if not prompt.strip():
                st.warning("Please enter a question.")
                return

            st.session_state.global_ask_ai_messages.append({"role": "user", "content": prompt})
            st.rerun()

        # If last message was user, generate response
        if st.session_state.global_ask_ai_messages and st.session_state.global_ask_ai_messages[-1]["role"] == "user":
            prompt = st.session_state.global_ask_ai_messages[-1]["content"]
            
            with st.spinner("✨ MeetIntel is thinking... retrieving knowledge and analyzing context."):
                analyzer = MeetingAnalyzer()
                try:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                        future = executor.submit(analyzer.rag_ask, prompt, meeting_id=None)
                        response = future.result()  # Rely on RAGService internal timeouts
                    
                    answer = response.get("answer", "Error generating answer.")
                    sources = response.get("sources", [])
                    status = response.get("status", "UNKNOWN")
                    
                    if not response.get("generation_success", True):
                        answer = "Relevant meeting knowledge found.\n\nAI generation is temporarily unavailable, but you can explore the retrieved sources below."
                    
                    st.session_state.global_ask_ai_messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources,
                        "status": status,
                        "error_type": response.get("error_type")
                    })
                    st.rerun()
                    
                except Exception as e:
                    logger.error(f"Global Ask AI failed: {e}", exc_info=True)
                    st.session_state.global_ask_ai_messages.append({
                        "role": "assistant",
                        "content": "AI service is temporarily busy. Please try again in a moment.",
                        "status": "ERROR"
                    })
                    st.rerun()
                    
    else:
        # Semantic Search Mode
        query = st.text_input("Search query", placeholder="Which meeting discussed the database migration?", label_visibility="collapsed")
        if st.button("Search", type="primary"):
            if not query.strip():
                st.warning("Please enter a search query.")
            else:
                with st.spinner("Searching semantic index..."):
                    try:
                        results = repo.semantic_search(query, top_k=10)
                        hits = results.get("results", [])
                        
                        if not hits:
                            st.markdown("""
                            <div style="text-align: center; padding: var(--mt-space-2xl) var(--mt-space-lg); background: var(--mt-surface); border-radius: var(--mt-radius-lg); border: 1px solid var(--mt-border); margin: var(--mt-space-xl) 0; box-shadow: var(--mt-shadow-soft);">
                                <div style="font-size: 3rem; margin-bottom: var(--mt-space-sm);">🔎</div>
                                <h4 style="color: var(--mt-text); font-weight: 600; margin-bottom: var(--mt-space-xs);">No matching meetings found</h4>
                                <p style="color: var(--mt-text-muted); font-size: 0.95rem; max-width: 400px; margin: 0 auto;">Try searching for a topic, a person, a decision, an action item, or a date.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='font-size: 0.85rem; color: var(--mt-text-muted); margin-bottom: var(--mt-space-md);'>Found {len(hits)} results in {results.get('search_time_ms', 0)}ms</div>", unsafe_allow_html=True)
                            for hit in hits:
                                meta = hit["metadata"]
                                title = meta.get("meeting_title", "Unknown Meeting")
                                date = meta.get("meeting_date", "Unknown Date")
                                sim = hit.get("similarity", 0)
                                content = hit.get("content", "")
                                
                                rel_label = "High" if sim > 0.6 else "Medium" if sim > 0.4 else "Low"
                                rel_color = "var(--mt-success)" if rel_label == "High" else "var(--mt-warning)" if rel_label == "Medium" else "var(--mt-text-muted)"
                                
                                st.markdown(f"""
                                <div class="saas-card" style="margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
                                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: var(--mt-space-sm);">
                                        <div>
                                            <h3 style="margin: 0 0 4px 0; font-size: 1.1rem; color: var(--mt-text); font-weight: 600;">{title}</h3>
                                            <div style="font-size: 0.8rem; color: var(--mt-text-muted);">{date} • Type: {meta.get('content_type', 'unknown').capitalize()}</div>
                                        </div>
                                        <div style="background: rgba(0,0,0,0.03); padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; color: {rel_color}; border: 1px solid rgba(0,0,0,0.05);">
                                            Relevance: {rel_label}
                                        </div>
                                    </div>
                                    <div style="background: var(--mt-bg); padding: var(--mt-space-sm) var(--mt-space-md); border-radius: var(--mt-radius-sm); border-left: 2px solid var(--mt-primary); font-size: 0.9rem; color: var(--mt-text); line-height: 1.5; margin-top: var(--mt-space-md);">
                                        "...{content}..."
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"""
                        <div style="background: #FEF2F2; border: 1px solid #FCA5A5; border-radius: var(--mt-radius-md); padding: var(--mt-space-md); margin-top: var(--mt-space-md);">
                            <h4 style="color: #991B1B; margin-top: 0;">Service temporarily unavailable</h4>
                            <p style="color: #7F1D1D; font-size: 0.9rem; margin-bottom: 0;">MeetIntel couldn't complete this search right now. Please try again later.</p>
                        </div>
                        """, unsafe_allow_html=True)
