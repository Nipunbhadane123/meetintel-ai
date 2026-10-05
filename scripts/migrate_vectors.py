import os
import sys

# Add root to pythonpath to import storage
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from storage.vector_store import VectorStore
from storage.database import SessionLocal
from storage.models import Meeting

def migrate_vector_metadata():
    print("Starting vector metadata migration...")
    store = VectorStore()
    
    # 1. Fetch all unique meeting_ids from sqlite to build a map
    db = SessionLocal()
    try:
        meetings = db.query(Meeting).all()
        meeting_to_user = {m.id: m.user_id for m in meetings}
        print(f"Loaded {len(meeting_to_user)} meeting ownership records from DB.")
    finally:
        db.close()
        
    # 2. Fetch all vectors from chroma collection
    # We can fetch everything without embeddings to be fast
    result = store.collection.get(include=["metadatas"])
    
    if not result or not result['ids']:
        print("No vectors found in ChromaDB.")
        return
        
    ids = result['ids']
    metadatas = result['metadatas']
    
    print(f"Found {len(ids)} vectors in ChromaDB.")
    
    ids_to_update = []
    metadatas_to_update = []
    
    for i, meta in enumerate(metadatas):
        if not meta:
            continue
            
        # Check if user_id is missing
        if "user_id" not in meta:
            meeting_id = meta.get("meeting_id")
            if meeting_id and meeting_id in meeting_to_user:
                new_meta = dict(meta)
                user_id = meeting_to_user[meeting_id]
                # ChromaDB metadatas cannot contain None. If user_id is None, it means the meeting has no owner.
                if user_id is not None:
                    new_meta["user_id"] = user_id
                    ids_to_update.append(ids[i])
                    metadatas_to_update.append(new_meta)
                
    if ids_to_update:
        print(f"Updating {len(ids_to_update)} vectors with missing user_id metadata...")
        # Update in batches of 1000 to be safe
        batch_size = 1000
        for i in range(0, len(ids_to_update), batch_size):
            store.collection.update(
                ids=ids_to_update[i:i+batch_size],
                metadatas=metadatas_to_update[i:i+batch_size]
            )
        print("Migration complete.")
    else:
        print("No vectors required updating. Migration skipped.")

if __name__ == "__main__":
    migrate_vector_metadata()
