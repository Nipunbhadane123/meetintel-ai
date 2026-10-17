import streamlit as st
import pandas as pd
from storage.database import SessionLocal
from storage.models import TranscriptSegment
from ui.components import transcript_message, empty_state, safe_escape, get_icon_svg

def render_transcript_tab(meeting_id):
    db = SessionLocal()
    try:
        segments = db.query(TranscriptSegment).filter(TranscriptSegment.meeting_id == meeting_id).order_by(TranscriptSegment.start).all()
    finally:
        db.close()
    
    if not segments:
        empty_state("file-text", "No transcript segments found", "The transcript for this meeting has not been processed or is empty.")
        return
        
    with st.container(border=True):
        col_s, col_d = st.columns([3.2, 1.3])
        with col_s:
            search = st.text_input("Search Transcript Dialogue", placeholder="Search keywords across speaker dialogue...", label_visibility="collapsed")
        with col_d:
            transcript_text = "\n".join([f"[{int(seg.start)//3600:02d}:{(int(seg.start)%3600)//60:02d}:{int(seg.start)%60:02d}] {seg.speaker}: {seg.text}" for seg in segments])
            st.download_button(
                label="↓ Download TXT",
                data=transcript_text,
                file_name=f"Transcript_Meeting_{meeting_id}.txt",
                mime="text/plain",
                type="secondary",
                use_container_width=True
            )
        
        st.markdown("<hr style='border: 0; border-top: 1px solid var(--mt-border); margin: 8px 0 12px 0;'>", unsafe_allow_html=True)
        
        matched_segments = []
        for seg in segments:
            if search and search.lower() not in seg.text.lower():
                continue
            matched_segments.append(seg)
            
        if search:
            st.caption(f"Showing {len(matched_segments)} matching segments of {len(segments)} total dialogue turns.")
        else:
            st.caption(f"{len(segments)} verified speaker dialogue turns.")
            
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        
        for seg in matched_segments:
            m, s = divmod(int(seg.start), 60)
            h, m = divmod(m, 60)
            ts = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
            transcript_message(seg.speaker, ts, seg.text)
            
        if search and not matched_segments:
            st.info(f"No dialogue segments matched '{search}'.")
            
    with st.expander("📊 Speech Recognition Accuracy Assessment (WER / Ground-Truth Evaluation)", expanded=False):
        st.markdown("""
        <p style="color: var(--mt-text-secondary); font-size: 0.88rem; margin-bottom: 12px;">
            Benchmarking tool for evaluation reviews: Compare this AI-transcribed dialogue against a reference ground-truth text to calculate Word Error Rate (WER) and Word Recognition Accuracy.
        </p>
        """, unsafe_allow_html=True)
        reference = st.text_area("Paste Ground-Truth Reference Dialogue:", placeholder="Paste verbatim ground-truth transcript here...", label_visibility="collapsed")
        if st.button("Evaluate Accuracy & WER", type="primary"):
            if reference.strip():
                try:
                    import jiwer
                    generated_text = " ".join([s.text for s in segments])
                    ref = jiwer.RemovePunctuation()(reference.lower().strip())
                    hyp = jiwer.RemovePunctuation()(generated_text.lower().strip())
                    wer = jiwer.wer(ref, hyp)
                    accuracy = max(0.0, 1.0 - wer)
                    
                    c_m1, c_m2 = st.columns(2)
                    with c_m1:
                        st.metric("Word Recognition Accuracy", f"{accuracy:.1%}")
                    with c_m2:
                        st.metric("Word Error Rate (WER)", f"{wer:.3f}")
                except ImportError:
                    st.error("jiwer library is not installed in the environment.")
                except Exception as e:
                    st.error(f"Error calculating accuracy metrics: {str(e)}")
            else:
                st.warning("Please paste a reference transcript to compare against.")
