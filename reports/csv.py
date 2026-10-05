import csv
import io

def generate_csv(meeting) -> io.StringIO:
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Meeting Details
    writer.writerow(["Meeting Details"])
    writer.writerow(["Title", meeting.title])
    date_str = meeting.date.strftime('%Y-%m-%d %H:%M') if meeting.date else "Unknown"
    writer.writerow(["Date", date_str])
    duration_str = f"{int(meeting.duration)//60}m {int(meeting.duration)%60}s" if meeting.duration else "N/A"
    writer.writerow(["Duration", duration_str])
    writer.writerow([])
    
    # Summary
    writer.writerow(["Executive Summary"])
    writer.writerow([meeting.executive_summary or "N/A"])
    writer.writerow([])
    
    # Participants
    writer.writerow(["Participants"])
    writer.writerow(["Name", "Speaker ID"])
    if meeting.participants:
        for p in meeting.participants:
            writer.writerow([p.name, p.speaker_id])
    else:
        writer.writerow(["None", "None"])
    writer.writerow([])
    
    # Action Items
    writer.writerow(["Action Items"])
    writer.writerow(["Task", "Assigned To", "Deadline", "Priority"])
    if meeting.action_items:
        for ai in meeting.action_items:
            writer.writerow([ai.task, ai.assigned_to, ai.deadline, ai.priority])
    else:
        writer.writerow(["None", "", "", ""])
    writer.writerow([])
    
    # Decisions
    writer.writerow(["Decisions"])
    writer.writerow(["Decision"])
    if meeting.decisions:
        for d in meeting.decisions:
            writer.writerow([d.decision])
    else:
        writer.writerow(["None"])
            
    output.seek(0)
    return output
