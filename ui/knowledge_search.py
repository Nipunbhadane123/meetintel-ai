import streamlit as st
import logging
import concurrent.futures
from ai.meeting_analyzer import MeetingAnalyzer
from storage.knowledge import get_knowledge_repository
from storage.database import SessionLocal
from storage.models import Meeting
from ui.components import page_header, render_status_badge, empty_state, safe_escape, metric_card, get_icon_svg

logger = logging.getLogger(__name__)

def render_knowledge_search_page():
    page_header(
        title="Enterprise Knowledge Search",
        subtitle="Query across your meeting repository with hybrid semantic search and grounded AI intelligence.",
        category="Enterprise Knowledge",
        badge_text="Semantic & RAG",
        badge_type="accent",
        icon="search"
    )
    
    user_id = st.session_state.get('user_id')
    username = st.session_state.get('username', 'User')
    user_initial = (username[0].upper() if username else "U")
    
    repo = get_knowledge_repository()
    db = SessionLocal()
    try:
        total_meetings = db.query(Meeting).filter(Meeting.user_id == user_id).count()
    except Exception:
        total_meetings = 0
    finally:
        db.close()
    
    try:
        user_vectors = repo.vector_store.collection.get(where={"user_id": user_id}, include=[])
        total_vectors = len(user_vectors["ids"]) if user_vectors and "ids" in user_vectors else 0
    except Exception:
        total_vectors = 0
        
    search_mode = st.session_state.get("search_mode_state", "Ask AI")
    
    # Live KPI Summary Row
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Indexed Sessions", str(total_meetings), "folder", "Meeting knowledge")
    with c2:
        metric_card("Knowledge Vectors", str(total_vectors), "network", "Embedded embeddings")
    with c3:
        metric_card("Active Engine", search_mode.upper(), "sparkles", "Query processing")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    # Segmented Control Bar
    col_tab1, col_tab2, _ = st.columns([1.3, 1.5, 3.2])
    with col_tab1:
        if st.button("✨ Grounded Ask AI", use_container_width=True, type="primary" if search_mode == "Ask AI" else "secondary"):
            st.session_state.search_mode_state = "Ask AI"
            st.rerun()
    with col_tab2:
        if st.button("🔎 Semantic Direct Search", use_container_width=True, type="primary" if search_mode == "Semantic" else "secondary"):
            st.session_state.search_mode_state = "Semantic"
            st.rerun()
            
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    if search_mode == "Ask AI":
        if "global_ask_ai_messages" not in st.session_state:
            st.session_state.global_ask_ai_messages = []

        if not st.session_state.global_ask_ai_messages:
            with st.container(border=True):
                st.markdown("""
                <div style="text-align: center; padding: 24px 16px;">
                    <div style="width: 44px; height: 44px; border-radius: 50%; background: var(--mt-primary-light); color: var(--mt-primary); display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto; font-size: 1.2rem;">✦</div>
                    <h3 style="color: var(--mt-text); font-weight: 700; margin-bottom: 6px; font-size: 1.25rem; letter-spacing: -0.015em;">Ask Your Enterprise Meeting Knowledge</h3>
                    <p style="color: var(--mt-text-secondary); max-width: 520px; margin: 0 auto 18px auto; font-size: 0.9rem; line-height: 1.5;">
                        Query across all indexed transcripts, decisions, and action items. MeetIntel synthesizes answers with verifiable meeting citations.
                    </p>
                    <div style="display: flex; flex-direction: column; gap: 8px; max-width: 440px; margin: 0 auto; text-align: left;">
                        <div style="background: var(--mt-surface-soft); border-radius: var(--mt-radius-sm); padding: 8px 14px; font-size: 0.86rem; color: var(--mt-text-secondary);">
                            💬 "What decisions were made regarding the Q3 product roadmap?"
                        </div>
                        <div style="background: var(--mt-surface-soft); border-radius: var(--mt-radius-sm); padding: 8px 14px; font-size: 0.86rem; color: var(--mt-text-secondary);">
                            💬 "Which meeting discussed database migrations and who was assigned?"
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Render chat history
        for message in st.session_state.global_ask_ai_messages:
            if message["role"] == "user":
                safe_user_content = safe_escape(message["content"])
                st.markdown(f"""
                <div style="display: flex; gap: 12px; margin-bottom: 16px; padding-left: 15%; justify-content: flex-end; align-items: flex-start;">
                    <div style="background: var(--mt-primary-light); padding: 12px 18px; border-radius: var(--mt-radius-lg); border-top-right-radius: 2px; border: 1px solid rgba(108, 77, 255, 0.2); line-height: 1.5; color: var(--mt-text); box-shadow: var(--mt-shadow-soft); font-size: 0.92rem;">
                        {safe_user_content}
                    </div>
                    <div style="flex-shrink: 0; width: 32px; height: 32px; background: var(--mt-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 0.82rem;">{user_initial}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                safe_ai_content = safe_escape(message["content"]).replace("\n", "<br>")
                st.markdown(f"""
                <div style="display: flex; gap: 12px; margin-bottom: 16px; padding-right: 15%; align-items: flex-start;">
                    <div style="flex-shrink: 0; width: 32px; height: 32px; background: var(--mt-surface); border-radius: 50%; border: 1px solid var(--mt-border); display: flex; align-items: center; justify-content: center; font-size: 1rem; color: var(--mt-primary); box-shadow: var(--mt-shadow-soft);">✧</div>
                    <div style="flex: 1;">
                        <div style="background: var(--mt-surface); border: 1px solid var(--mt-border); border-radius: var(--mt-radius-lg); border-top-left-radius: 2px; padding: 14px 18px; line-height: 1.6; color: var(--mt-text); font-size: 0.92rem; box-shadow: var(--mt-shadow-card);">
                            {safe_ai_content}
                        </div>
                """, unsafe_allow_html=True)
                
                if "sources" in message and message["sources"]:
                    st.markdown("""<div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; padding-left: 4px;">""", unsafe_allow_html=True)
                    for src in message["sources"]:
                        src_title = safe_escape(src.get('meeting_title', 'Meeting Source'))
                        st.markdown(f"""
                            <div style="background: var(--mt-surface-soft); border-radius: var(--mt-radius-pill); padding: 3px 10px; font-size: 0.74rem; color: var(--mt-text-secondary); display: inline-flex; align-items: center; gap: 5px;">
                                <span style="color: var(--mt-primary); font-weight: bold;">✦</span> {src_title}
                            </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
            if message.get("status") in ["LLM_UNAVAILABLE", "ERROR"]:
                if st.button("🔄 Retry Response", key=f"retry_global_{id(message)}"):
                    if st.session_state.global_ask_ai_messages and st.session_state.global_ask_ai_messages[-1]["role"] == "assistant":
                        st.session_state.global_ask_ai_messages.pop()
                    st.rerun()

        if prompt := st.chat_input("Ask anything across your meeting knowledge..."):
            if not prompt.strip():
                st.warning("Please enter a question.")
                return

            st.session_state.global_ask_ai_messages.append({"role": "user", "content": prompt})
            st.rerun()

        # If last message was user, generate response
        if st.session_state.global_ask_ai_messages and st.session_state.global_ask_ai_messages[-1]["role"] == "user":
            prompt = st.session_state.global_ask_ai_messages[-1]["content"]
            
            with st.spinner("✨ MeetIntel is synthesizing knowledge and analyzing meeting context..."):
                analyzer = MeetingAnalyzer()
                try:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                        future = executor.submit(analyzer.rag_ask, prompt, user_id=user_id, meeting_id=None)
                        response = future.result()
                    
                    answer = response.get("answer", "Error generating answer.")
                    sources = response.get("sources", [])
                    status = response.get("status", "UNKNOWN")
                    
                    if not response.get("generation_success", True):
                        answer = "Relevant meeting knowledge found.\n\nAI generation is temporarily busy, but you can explore the retrieved sources below."
                    
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
        # Semantic Direct Search Mode
        with st.container(border=True):
            col_inp, col_btn = st.columns([4, 1.2])
            with col_inp:
                query = st.text_input("Semantic Search Query", placeholder="e.g. Which meeting discussed the database migration and launch timeline?", label_visibility="collapsed")
            with col_btn:
                do_search = st.button("Search Knowledge", type="primary", use_container_width=True)

        if do_search or query:
            if not query.strip():
                st.warning("Please enter a search query.")
            else:
                with st.spinner("Searching semantic index across organizational knowledge..."):
                    try:
                        results = repo.semantic_search(query, user_id=user_id, top_k=10)
                        hits = results.get("results", [])
                        
                        if not hits:
                            empty_state("search", "No matching meeting knowledge found", "Try searching for a project milestone, key attendee, architecture decision, or date.")
                        else:
                            st.caption(f"Retrieved {len(hits)} grounded results in {results.get('search_time_ms', 0)}ms")
                            for idx, hit in enumerate(hits):
                                meta = hit.get("metadata", {})
                                title = meta.get("meeting_title", "Meeting Discussion")
                                date = meta.get("meeting_date", "Recent")
                                sim = hit.get("similarity", 0)
                                content = hit.get("content", "")
                                meeting_id = meta.get("meeting_id")
                                
                                rel_label = "High Relevance" if sim > 0.6 else "Medium Relevance" if sim > 0.4 else "Low Relevance"
                                
                                with st.container(border=True):
                                    col_k1, col_k2 = st.columns([3.5, 1.5])
                                    with col_k1:
                                        st.caption(f"SESSION • {safe_escape(str(date))} • {safe_escape(meta.get('content_type', 'transcript').upper())}")
                                        st.markdown(f"<h3 style='margin: 0 0 4px 0; font-size: 1.15rem; color: var(--mt-text); font-weight: 700;'>{safe_escape(title)}</h3>", unsafe_allow_html=True)
                                    with col_k2:
                                        st.markdown(f"<div style='text-align: right; margin-bottom: 6px;'>{render_status_badge(rel_label, 'status')}</div>", unsafe_allow_html=True)
                                        if meeting_id:
                                            if st.button("Open Dossier →", key=f"btn_hit_{idx}_{meeting_id}", use_container_width=True, type="secondary"):
                                                st.session_state['current_meeting_id'] = meeting_id
                                                st.session_state['current_page'] = "Meeting Results"
                                                st.rerun()
                                        
                                    st.markdown(f"""
                                        <div class="evidence-box">
                                            <div class="evidence-box-title">Grounded Evidence Excerpt</div>
                                            <div class="evidence-box-text">"{safe_escape(content)}"</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                    except Exception as e:
                        logger.error(f"Semantic search failed: {e}", exc_info=True)
                        st.error(f"Search service temporarily unavailable: {e}")
