import os
import sys
import logging
import json
from ai.rag import RAGService, QueryRouter

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def test_rag():
    print("====================================")
    print("RAG SYSTEM TEST SUITE")
    print("====================================\n")
    
    service = RAGService()
    
    queries = [
        "What was decided about the mobile app?",  # Semantic / Decisions
        "Which is the largest meet?",          # Aggregation
        "What was the last meeting?",              # Metadata Last
        "What action items were assigned?",        # Actions
        "What was decided about the Mars mission?", # Irrelevant
        "Which meeting discussed database migration?", # Semantic 
    ]
    
    for q in queries:
        print(f"\n[TEST] Question: {q}")
        mode = QueryRouter.classify(q)
        print(f"[TEST] Mode Classified: {mode}")
        
        result = service.ask(q)
        
        print(f"[TEST] Status: {result.get('status')}")
        print(f"[TEST] Answer: {result.get('answer')}")
        print(f"[TEST] Retrieval Time: {result.get('retrieval_time_ms')} ms")
        print(f"[TEST] Generation Time: {result.get('generation_time_ms')} ms")
        
        sources = result.get('sources', [])
        print(f"[TEST] Sources Found: {len(sources)}")
        for i, s in enumerate(sources[:2]):
            print(f"       - Source {i+1}: {s.get('meeting_title')} ({s.get('content_type')}) - {s.get('excerpt', '')[:50]}...")
            
    print("\n[TEST] All tests completed.")

if __name__ == "__main__":
    test_rag()
