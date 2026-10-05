import sqlite3
import os

db_path = "meetintel.db"

if not os.path.exists(db_path):
    print("Database not found!")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    
    # Get all meetings
    cursor.execute("SELECT id, title, user_id FROM meetings")
    meetings = cursor.fetchall()
    
    user_map = {u[0]: {'username': u[1], 'email': u[2], 'meetings': []} for u in users}
    
    unassigned_meetings = []
    
    for m in meetings:
        m_id, title, user_id = m
        if user_id is None:
            unassigned_meetings.append(title)
        elif user_id in user_map:
            user_map[user_id]['meetings'].append(title)
        else:
            # Owned by a user that doesn't exist?
            unassigned_meetings.append(f"{title} (Orphaned user_id: {user_id})")
            
    print("User ID | Username/Email | Meeting Count | Meeting Titles")
    print("-" * 80)
    for u_id, info in user_map.items():
        count = len(info['meetings'])
        titles = ", ".join(info['meetings'])
        print(f"{u_id} | {info['username']} / {info['email']} | {count} | {titles}")
        
    print(f"\nUnassigned/NULL owner | N/A | {len(unassigned_meetings)} | {', '.join(unassigned_meetings)}")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
