import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import uuid

# Vector DB configuration
DB_DIR = os.getenv("VECTOR_DB_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage", "vector_db"))
COLLECTION_NAME = "meetintel_knowledge"

class VectorStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
        
    def _initialize(self):
        os.makedirs(DB_DIR, exist_ok=True)
        self.client = chromadb.PersistentClient(path=DB_DIR, settings=Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        
    def insert_vectors(self, ids: List[str], embeddings: List[List[float]], documents: List[str], metadatas: List[Dict[str, Any]]):
        """Insert or update vectors."""
        if not ids:
            return
            
        # chromadb requires IDs to be strings
        str_ids = [str(id) for id in ids]
        
        self.collection.upsert(
            ids=str_ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        
    def delete_meeting_vectors(self, meeting_id: str):
        """Delete all vectors associated with a meeting."""
        self.collection.delete(
            where={"meeting_id": meeting_id}
        )
        
    def search(self, query_embedding: List[float], user_id: Optional[str] = None, meeting_id: Optional[str] = None, content_type: Optional[str] = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search vectors."""
        where_clause = {}
        if user_id:
            where_clause["user_id"] = user_id
        if meeting_id:
            where_clause["meeting_id"] = meeting_id
        if content_type:
            where_clause["content_type"] = content_type
            
        if len(where_clause) > 1:
            # ChromaDB uses $and for multiple conditions
            and_conditions = [{k: v} for k, v in where_clause.items()]
            where = {"$and": and_conditions}
        elif where_clause:
            where = where_clause
        else:
            where = None
            
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        
        formatted_results = []
        if not results or not results['ids'] or not results['ids'][0]:
            return formatted_results
            
        for i in range(len(results['ids'][0])):
            distance = results['distances'][0][i]
            # Convert cosine distance to similarity score
            similarity = 1.0 - distance
            
            formatted_results.append({
                "id": results['ids'][0][i],
                "content": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "similarity": similarity
            })
            
        return formatted_results
