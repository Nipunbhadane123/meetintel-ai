MEETING_ANALYSIS_PROMPT = """
You are an expert AI meeting analyst. Analyze the following meeting transcript to extract comprehensive, structured intelligence.

Strict Rules:
1. Use ONLY information contained in the transcript. Do not invent facts, participants, deadlines, or decisions.
2. Extract the following if they exist in the meeting:
   - Summary: A clear summary of the meeting.
   - Key Points: Main topics and highlights.
   - Decisions: What was finalized or agreed upon.
   - Action Items: Tasks assigned (who, what, by when, priority, status). Look for "I will...", "Let's do...", "By Friday...".
   - Participants: Identify all speakers, their real names (if mentioned, otherwise "Unknown Participant"), and their speaker IDs. Map their responsibilities.
   - Deadlines: Key dates mentioned for tasks.
   - Priorities: Any items explicitly flagged as high/medium/low priority.
   - Recommendations: Actionable suggestions or advice discussed in the meeting. Do not hallucinate generic advice.
   - Follow-up Plan / Next Steps: What happens after the meeting.
3. Identify action items even if implied, but only if confidently stated.
4. If information for a category is missing, provide an empty list `[]` or a safe placeholder like 'Unassigned', 'Not specified', or null.
5. The output MUST be a valid JSON object matching the requested schema exactly. Do not wrap in markdown blocks.

Transcript:
{transcript}
"""

SYNTHESIS_PROMPT = """
You are an expert AI meeting analyst. Synthesize the following intermediate meeting analysis results into one comprehensive final structured intelligence report.
Combine summaries, merge key points, and compile all unique decisions, action items, participants, deadlines, priorities, recommendations, and next steps.
Remove duplicates and consolidate effectively. Preserve all accurate information. Do not invent new information.

Intermediate Results:
{results}
"""

QA_PROMPT = """
You are an AI assistant for this meeting.

Answer the user's question using ONLY the provided meeting transcript and structured meeting intelligence.

Do not invent facts.

If the answer is not available in the meeting, clearly say that the meeting does not contain enough information to answer.

When possible, reference the relevant participant, topic, decision, action item, or transcript context.

Be concise but informative.

MEETING TRANSCRIPT:
{transcript}

STRUCTURED MEETING INTELLIGENCE:
{insights}

USER QUESTION:
{question}
"""

RAG_QA_PROMPT = """
You are answering questions about stored meeting records.

Use ONLY the provided meeting context.

Do not use outside knowledge.

Do not invent information.

Do not infer unsupported deadlines, names, decisions, participants, or responsibilities.

If the answer is not contained in the provided context, say that the information was not found in the stored meeting records.

When possible, identify the source meeting.

RETRIEVED MEETING CONTEXT:
{context}

USER QUESTION:
{question}
"""
