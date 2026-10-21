export type UserRole = "Admin" | "Team Lead" | "Employee";

export type TaskStatus =
  | "Draft"
  | "Pending"
  | "In Progress"
  | "Completed"
  | "Blocked"
  | "Rejected";

export type ApprovalStatus =
  | "Draft"
  | "Pending Approval"
  | "Approved"
  | "Rejected";

export interface User {
  id: string;
  username: string;
  email: string;
  role: UserRole;
  full_name: string;
  department: string;
  timezone: string;
}

export interface ActionItem {
  id: number;
  meeting_id: string;
  meeting_title: string;
  task: string;
  description?: string;
  assigned_to: string;
  assigned_user_id: string;
  deadline: string;
  priority: "Low" | "Medium" | "High" | "Urgent";
  status: TaskStatus;
  approval_status: ApprovalStatus;
  evidence_excerpt: string;
  estimated_hours: number;
  is_blocked: boolean;
  blocker_reason: string | null;
  calendar_synced?: boolean;
}

export interface Decision {
  id: number;
  meeting_id: string;
  meeting_title: string;
  title: string;
  status: "Approved" | "Proposed" | "Rejected";
  rationale: string;
  alternatives: string;
  confidence: number;
  evidence_excerpt?: string;
}

export interface TranscriptSegment {
  id: string;
  speaker: string;
  start: number;
  end: number;
  text: string;
  confidence?: number;
}

export interface Participant {
  id: string;
  name: string;
  speaker_id: string;
  attendance_status?: string;
  responsibilities: string[];
}

export interface Meeting {
  id: string;
  title: string;
  filename?: string;
  date: string;
  duration: number;
  speaker_count: number;
  processing_status: "Completed" | "Processing" | "Pending" | "Failed";
  source_platform: "upload" | "google_meet" | "zoom";
  executive_summary?: string;
  meeting_objective?: string;
  meeting_plan?: string;
  emotional_analysis?: string;
  key_topics?: string[];
  key_points?: string[];
  risks?: Array<{ risk: string; impact: string; mitigation: string }>;
  recommendations?: string[];
  next_steps?: string[];
  segments?: TranscriptSegment[];
  participants?: Participant[];
  deadlines?: Array<{ description: string; date: string; related_task?: string }>;
  priorities?: Array<{ item: string; priority: string }>;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  target_date: string;
  status: "Active" | "At Risk" | "Completed";
  action_items_count: number;
  completed_items_count: number;
}

export interface IntegrationStatus {
  id: string;
  provider: "google_meet" | "google_calendar" | "zoom" | "email_smtp";
  name: string;
  display_name: string;
  account_email: string;
  status: "Connected" | "Needs attention" | "Disconnected";
  connection_status?: "Connected" | "Needs attention" | "Disconnected";
  last_sync: string;
  last_sync_at: string;
  features: string[];
  error_message?: string;
  sync_count: number;
}

export interface WorkflowRule {
  id: string;
  name: string;
  description: string;
  trigger_event: string;
  action_type: string;
  condition_json?: string;
  is_enabled: boolean;
  is_active: boolean;
  last_triggered_at: string;
  execution_count: number;
  success_count: number;
}

export interface AuditEvent {
  id: string;
  action: "APPROVE" | "CREATE" | "UPDATE" | "SYNC" | "TRIGGER" | "SEND" | "REJECT" | "REASSIGN";
  actor: string;
  entity_type: string;
  entity_id: string;
  details: string;
  timestamp: string;
}

export interface Followup {
  id: string;
  recipient_name: string;
  recipient_email: string;
  subject: string;
  meeting_title: string;
  status: "Drafted" | "Sent" | "Pending Review";
  channel: "Email" | "Calendar" | "Slack";
  summary: string;
  summary_preview: string;
  action_items_count: number;
  sent_at?: string;
}

export interface KnowledgeSearchResult {
  results: Array<{
    id: string;
    title: string;
    type: string;
    excerpt: string;
    content: string;
    date: string;
    relevance: number;
    similarity: number;
  }>;
  search_time_ms: number;
}
