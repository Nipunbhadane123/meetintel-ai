import os
import sys
import argparse
import logging
from tqdm import tqdm

# Ensure the parent directory is in the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from storage.database import SessionLocal
from storage.models import Meeting
from storage.knowledge import get_knowledge_repository

logging.basicConfig(level=logging.INFO, format='%(message)s')

def main():
    parser = argparse.ArgumentParser(description="Backfill vector DB with existing meetings.")
    parser.add_argument("--all", action="store_true", help="Index all meetings")
    parser.add_argument("--meeting_id", type=str, help="Index a specific meeting by ID")
    args = parser.parse_args()
    
    db = SessionLocal()
    repo = get_knowledge_repository()
    
    meetings_to_index = []
    
    if args.meeting_id:
        meeting = db.query(Meeting).filter(Meeting.id == args.meeting_id).first()
        if meeting:
            meetings_to_index.append(meeting)
        else:
            print(f"Meeting {args.meeting_id} not found.")
            sys.exit(1)
    elif args.all:
        meetings_to_index = db.query(Meeting).all()
    else:
        # Default to all if no args provided
        meetings_to_index = db.query(Meeting).all()
        
    if not meetings_to_index:
        print("No meetings found to index.")
        sys.exit(0)
        
    print(f"Found {len(meetings_to_index)} meetings to index.")
    
    success_count = 0
    fail_count = 0
    
    for meeting in tqdm(meetings_to_index, desc="Indexing Meetings"):
        try:
            success = repo.index_meeting(meeting.id)
            if success:
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"\nFailed to index meeting {meeting.id}: {e}")
            fail_count += 1
            
    print(f"\nIndexing complete!")
    print(f"Successfully indexed: {success_count}")
    print(f"Failed to index: {fail_count}")

if __name__ == "__main__":
    main()
