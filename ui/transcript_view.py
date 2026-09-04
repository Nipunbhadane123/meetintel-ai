import streamlit as st
import pandas as pd
from storage.database import get_db
from storage.models import TranscriptSegment

def render_transcript_tab(meeting_id):
    st.header("Transcript")
    
    db = next(get_db())
    segments = db.query(TranscriptSegment).filter(TranscriptSegment.meeting_id == meeting_id).order_by(TranscriptSegment.start).all()
    
    if not segments:
        st.info("No transcript found.")
        return
        
    search = st.text_input("Search Transcript", "")
    
    transcript_text = "\n".join([f"[{int(seg.start)//3600:02d}:{(int(seg.start)%3600)//60:02d}:{int(seg.start)%60:02d}] {seg.speaker}: {seg.text}" for seg in segments])
    st.download_button(
        label="Download Transcript (TXT)",
        data=transcript_text,
        file_name=f"Transcript_Meeting_{meeting_id}.txt",
        mime="text/plain"
    )
    
    st.markdown("---")
    
    for seg in segments:
        if search and search.lower() not in seg.text.lower():
            continue
            
        # Format Timestamp
        m, s = divmod(int(seg.start), 60)
        h, m = divmod(m, 60)
        if h > 0:
            ts = f"[{h:02d}:{m:02d}:{s:02d}]"
        else:
            ts = f"[{m:02d}:{s:02d}]"
            
        st.markdown(f"**{ts} {seg.speaker}**")
        st.write(seg.text)
        st.markdown("<br>", unsafe_allow_html=True)
        
    st.markdown("---")
    with st.expander("Evaluate Accuracy (WER)"):
        st.write("Compare this generated transcript against a reference transcript to calculate the Word Error Rate (WER) and Accuracy.")
        reference = st.text_area("Paste Reference Transcript Here:")
        if st.button("Calculate Accuracy"):
            if reference.strip():
                try:
                    import jiwer
                    generated_text = " ".join([s.text for s in segments])
                    
                    # Normalize texts
                    ref = jiwer.RemovePunctuation()(reference.lower().strip())
                    hyp = jiwer.RemovePunctuation()(generated_text.lower().strip())
                    
                    wer = jiwer.wer(ref, hyp)
                    accuracy = max(0.0, 1.0 - wer)
                    
                    st.success(f"**Accuracy:** {accuracy:.2%} (WER: {wer:.3f})")
                except ImportError:
                    st.error("jiwer is not installed.")
                except Exception as e:
                    st.error(f"Error calculating accuracy: {str(e)}")
            else:
                st.warning("Please paste a reference transcript first.")
