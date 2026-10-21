import {
  UserRole,
  User,
  ActionItem,
  Decision,
  Meeting,
  Project,
  IntegrationStatus,
  WorkflowRule,
  AuditEvent,
  Followup,
  TaskStatus,
  KnowledgeSearchResult,
} from "./types";

let currentUser: User = {
  id: "user-sarah-002",
  username: "sarah_lead",
  email: "sarah.jenkins@acme.corp",
  role: "Team Lead",
  full_name: "Sarah Jenkins",
  department: "Platform Engineering",
  timezone: "America/New_York",
};

const users: User[] = [
  {
    id: "user-admin-001",
    username: "admin",
    email: "admin@acme.corp",
    role: "Admin",
    full_name: "Alexander Vance",
    department: "Executive Operations",
    timezone: "America/New_York",
  },
  currentUser,
  {
    id: "user-alex-003",
    username: "alex_eng",
    email: "alex.chen@acme.corp",
    role: "Employee",
    full_name: "Alex Chen",
    department: "Backend Infrastructure",
    timezone: "America/Los_Angeles",
  },
  {
    id: "user-priya-004",
    username: "priya_qa",
    email: "priya.sharma@acme.corp",
    role: "Employee",
    full_name: "Priya Sharma",
    department: "Quality Assurance",
    timezone: "Europe/London",
  },
  {
    id: "user-elena-005",
    username: "elena_rostova",
    email: "elena.rostova@acme.corp",
    role: "Employee",
    full_name: "Elena Rostova",
    department: "Security Architecture",
    timezone: "Europe/Berlin",
  },
];

let meetings: Meeting[] = [
  {
    id: "demo-meeting-q3-security",
    title: "Q3 Architecture & Security Alignment",
    filename: "Q3_Architecture_and_Security.wav",
    date: "2026-10-20",
    duration: 1840.0,
    speaker_count: 3,
    processing_status: "Completed",
    source_platform: "google_meet",
    executive_summary:
      "The engineering leadership aligned on the Q3 security roadmap. Key focus areas include enforcing OAuth 2.0 PKCE, resolving database pooling bottlenecks, and establishing a 90-day compliance retention policy.",
    meeting_objective:
      "Finalize authentication architecture and assign sprint deliverables.",
    meeting_plan:
      "Review architecture -> Assess security blockers -> Assign sprint tasks -> Confirm deadlines.",
    emotional_analysis: "Constructive, decisive, and focused.",
    key_topics: [
      "OAuth 2.0 Migration",
      "Database Pooling",
      "Audit Trail Compliance",
      "Release Timeline",
    ],
    key_points: [
      "Agreed to mandate PKCE flow for all clients",
      "Database pool must be increased to 50 connections",
      "Elena Rostova excused due to client deployment",
    ],
    risks: [
      {
        risk: "Database latency spike during peak loads",
        impact: "High",
        mitigation: "Alex Chen will optimize index pooling",
      },
      {
        risk: "Client SDK backward incompatibility",
        impact: "Medium",
        mitigation: "Provide 30-day deprecated fallback gateway",
      },
    ],
    recommendations: [
      "Conduct automated regression test before Monday deployment",
      "Trigger calendar reminders 24h prior to sprint cutoff",
    ],
    next_steps: [
      "Review PKCE prototype by Friday",
      "Dispatch meeting brief to Elena Rostova",
    ],
    participants: [
      {
        id: "part-001",
        name: "Sarah Jenkins",
        speaker_id: "SPEAKER_01",
        attendance_status: "Present",
        responsibilities: ["Review PKCE prototype", "Sign off security policy"],
      },
      {
        id: "part-002",
        name: "Alex Chen",
        speaker_id: "SPEAKER_02",
        attendance_status: "Present",
        responsibilities: ["Complete OAuth 2.0 PKCE integration", "Tune DB pool"],
      },
      {
        id: "part-003",
        name: "Priya Sharma",
        speaker_id: "SPEAKER_03",
        attendance_status: "Present",
        responsibilities: ["Validate auth test suite", "Verify token revocation"],
      },
      {
        id: "part-004",
        name: "Elena Rostova",
        speaker_id: "SPEAKER_04",
        attendance_status: "Excused",
        responsibilities: ["Review audit compliance logs"],
      },
    ],
    deadlines: [
      {
        description: "OAuth 2.0 PKCE integration completion",
        date: "2026-10-24",
        related_task: "Complete OAuth 2.0 PKCE integration",
      },
      {
        description: "Auth test suite verification",
        date: "2026-10-27",
        related_task: "Validate auth test suite",
      },
    ],
    priorities: [
      { item: "OAuth 2.0 PKCE Implementation", priority: "Urgent" },
      { item: "Database Pool Resizing", priority: "High" },
      { item: "E2E Authentication Test Suite", priority: "Medium" },
    ],
    segments: [
      {
        id: "seg-001",
        speaker: "Sarah Jenkins",
        start: 0.0,
        end: 15.0,
        text: "Welcome everyone to our Q3 Architecture and Security review.",
        confidence: 0.98,
      },
      {
        id: "seg-002",
        speaker: "Sarah Jenkins",
        start: 16.0,
        end: 35.0,
        text: "Elena is excused today as she is onsite with a client. We will send her an approved follow-up summary.",
        confidence: 0.97,
      },
      {
        id: "seg-003",
        speaker: "Alex Chen",
        start: 36.0,
        end: 65.0,
        text: "I will complete the OAuth 2.0 PKCE integration by this Friday. We need to prevent authorization code interception.",
        confidence: 0.96,
      },
      {
        id: "seg-004",
        speaker: "Priya Sharma",
        start: 66.0,
        end: 95.0,
        text: "I will validate the authentication test suite once Alex deploys the prototype to staging.",
        confidence: 0.95,
      },
      {
        id: "seg-005",
        speaker: "Sarah Jenkins",
        start: 96.0,
        end: 120.0,
        text: "Approved. All clients must mandate PKCE by Q4. Let's make sure tasks are synced to Google Calendar.",
        confidence: 0.99,
      },
    ],
  },
  {
    id: "demo-meeting-sprint-retro",
    title: "Sprint 42 Retrospective & Velocity Review",
    filename: "Sprint_42_Retrospective.wav",
    date: "2026-10-18",
    duration: 2100.0,
    speaker_count: 4,
    processing_status: "Completed",
    source_platform: "zoom",
    executive_summary:
      "Team analyzed Sprint 42 sprint burndown, identified test suite flakiness as primary blocker, and committed to dedicated reliability refactor.",
    meeting_objective: "Assess sprint velocity and unblock CI pipeline delays.",
    key_topics: ["Burndown Chart", "CI Flakiness", "Worker Backoff Retry"],
  },
  {
    id: "demo-meeting-exec-sync",
    title: "Executive Product & Roadmap Steering",
    filename: "Executive_Steering_Sync.wav",
    date: "2026-10-15",
    duration: 2700.0,
    speaker_count: 3,
    processing_status: "Completed",
    source_platform: "upload",
    executive_summary:
      "Q4 budget expansion approved for generative AI meeting synthesis and enterprise SAML single-sign-on.",
    meeting_objective: "Secure Q4 feature roadmap commitments and enterprise SLA tiers.",
    key_topics: ["SAML SSO", "SaaS Pricing Model", "Customer Retention"],
  },
];

let actionItems: ActionItem[] = [
  {
    id: 101,
    meeting_id: "demo-meeting-q3-security",
    meeting_title: "Q3 Architecture & Security Alignment",
    task: "Complete OAuth 2.0 PKCE integration across microservice gateways",
    description: "Complete OAuth 2.0 PKCE integration across microservice gateways",
    assigned_to: "Alex Chen",
    assigned_user_id: "user-alex-003",
    deadline: "2026-10-24",
    priority: "Urgent",
    status: "In Progress",
    approval_status: "Approved",
    evidence_excerpt:
      "Alex Chen: 'I will complete the OAuth 2.0 PKCE integration by this Friday.'",
    estimated_hours: 12,
    is_blocked: false,
    blocker_reason: null,
    calendar_synced: true,
  },
  {
    id: 102,
    meeting_id: "demo-meeting-q3-security",
    meeting_title: "Q3 Architecture & Security Alignment",
    task: "Validate authentication test suite and token revocation endpoints",
    description: "Validate authentication test suite and token revocation endpoints",
    assigned_to: "Priya Sharma",
    assigned_user_id: "user-priya-004",
    deadline: "2026-10-27",
    priority: "High",
    status: "Pending",
    approval_status: "Pending Approval",
    evidence_excerpt:
      "Priya Sharma: 'I will validate the authentication test suite once Alex deploys the prototype.'",
    estimated_hours: 8,
    is_blocked: false,
    blocker_reason: null,
    calendar_synced: false,
  },
  {
    id: 103,
    meeting_id: "demo-meeting-q3-security",
    meeting_title: "Q3 Architecture & Security Alignment",
    task: "Optimize connection pooling parameters to prevent database bottleneck",
    description: "Optimize connection pooling parameters to prevent database bottleneck",
    assigned_to: "Alex Chen",
    assigned_user_id: "user-alex-003",
    deadline: "2026-10-29",
    priority: "High",
    status: "Blocked",
    approval_status: "Approved",
    evidence_excerpt:
      "Sarah Jenkins: 'Alex Chen will optimize index pooling to resolve latency spikes.'",
    estimated_hours: 16,
    is_blocked: true,
    blocker_reason: "Awaiting DBA approval on RDS PostgreSQL pool size increase",
    calendar_synced: true,
  },
  {
    id: 104,
    meeting_id: "demo-meeting-sprint-retro",
    meeting_title: "Sprint 42 Retrospective",
    task: "Implement persistent background worker with exponential backoff & jitter",
    description: "Implement persistent background worker with exponential backoff & jitter",
    assigned_to: "Elena Rostova",
    assigned_user_id: "user-elena-005",
    deadline: "2026-11-02",
    priority: "Medium",
    status: "Completed",
    approval_status: "Approved",
    evidence_excerpt:
      "Elena Rostova: 'I have verified idempotent background task queue retries.'",
    estimated_hours: 14,
    is_blocked: false,
    blocker_reason: null,
    calendar_synced: true,
  },
];

let decisions: Decision[] = [
  {
    id: 201,
    meeting_id: "demo-meeting-q3-security",
    meeting_title: "Q3 Architecture & Security Alignment",
    title: "Mandate OAuth 2.0 with PKCE for all client authentication",
    status: "Approved",
    rationale:
      "Eliminates vulnerable implicit flow and provides cryptographic authorization code verification for single-page and mobile clients.",
    alternatives:
      "Retaining shared client secrets in client configurations (rejected due to audit vulnerability).",
    confidence: 0.99,
    evidence_excerpt:
      "Sarah Jenkins: 'The team decided to mandate OAuth 2.0 with PKCE and retain audit logs for 90 days.'",
  },
  {
    id: 202,
    meeting_id: "demo-meeting-q3-security",
    meeting_title: "Q3 Architecture & Security Alignment",
    title: "Enforce 90-day immutable compliance audit trail retention",
    status: "Approved",
    rationale:
      "SOC-2 and ISO 27001 regulatory readiness requiring tamper-evident chronological event records.",
    alternatives:
      "30-day default rotation (failed compliance audit standard).",
    confidence: 0.98,
    evidence_excerpt:
      "Sarah Jenkins: 'Audit event retention is set to 90 days with tamper-evident hashing.'",
  },
];

let projects: Project[] = [
  {
    id: "proj-001",
    name: "Enterprise Security & IAM Hardening",
    description:
      "Implementation of OAuth 2.0 PKCE, session rotation, and multi-tenant isolation.",
    target_date: "2026-11-15",
    status: "Active",
    action_items_count: 6,
    completed_items_count: 4,
  },
  {
    id: "proj-002",
    name: "Autonomous Meeting Intelligence & MoM Automation",
    description:
      "End-to-end pipeline: Whisper speech transcription, Pyannote diarization, and RAG knowledge search.",
    target_date: "2026-11-30",
    status: "Active",
    action_items_count: 8,
    completed_items_count: 7,
  },
  {
    id: "proj-003",
    name: "Real-time Two-Way Calendar & Absentee Dispatch",
    description:
      "Automated attendance-aware follow-up briefings and Google Calendar task synchronizer.",
    target_date: "2026-10-31",
    status: "At Risk",
    action_items_count: 5,
    completed_items_count: 2,
  },
];

let integrations: IntegrationStatus[] = [
  {
    id: "int-001",
    provider: "google_meet",
    name: "Google Meet & Drive Cloud Ingestion",
    display_name: "Google Meet & Drive",
    account_email: "workspace-admin@acme.corp",
    status: "Connected",
    connection_status: "Connected",
    last_sync: "Just now",
    last_sync_at: "Just now",
    features: ["Auto Transcript Ingestion", "Drive Folder Scanning", "Dual Recording Detection"],
    sync_count: 48,
  },
  {
    id: "int-002",
    provider: "google_calendar",
    name: "Google Calendar Two-Way Synchronization",
    display_name: "Google Calendar",
    account_email: "calendar-sync@acme.corp",
    status: "Connected",
    connection_status: "Connected",
    last_sync: "5 minutes ago",
    last_sync_at: "5 minutes ago",
    features: ["Idempotent Event Sync", "24h & 1h Reminder Notifications", "Attendee Presence Matching"],
    sync_count: 142,
  },
  {
    id: "int-003",
    provider: "zoom",
    name: "Zoom Cloud Recording HMAC Webhook",
    display_name: "Zoom Cloud Recording",
    account_email: "zoom-integrations@acme.corp",
    status: "Connected",
    connection_status: "Connected",
    last_sync: "1 hour ago",
    last_sync_at: "1 hour ago",
    features: ["HMAC-SHA256 Signed Webhook", "Replay Protection", "Multi-Language Diarization"],
    sync_count: 29,
  },
  {
    id: "int-004",
    provider: "email_smtp",
    name: "Attendance-Aware Email Dispatcher",
    display_name: "Enterprise Email / SMTP",
    account_email: "notifications@acme.corp",
    status: "Connected",
    connection_status: "Connected",
    last_sync: "12 minutes ago",
    last_sync_at: "12 minutes ago",
    features: ["Absentee Executive Briefing", "Review-Before-Send Gating", "Daily Digest Delivery"],
    sync_count: 85,
  },
];

let workflowRules: WorkflowRule[] = [
  {
    id: "rule-001",
    name: "Auto-Sync Approved Deliverables to Google Calendar",
    description: "Whenever a deliverable receives team lead sign-off, provision calendar event with automated reminders.",
    trigger_event: "TASK_APPROVED",
    action_type: "GOOGLE_CALENDAR_CREATE_EVENT",
    condition_json: '{"approval_status": "Approved", "has_deadline": true}',
    is_enabled: true,
    is_active: true,
    last_triggered_at: "2026-10-21 04:30:12",
    execution_count: 124,
    success_count: 122,
  },
  {
    id: "rule-002",
    name: "Dispatch Executive Briefing to Excused Absentee Attendees",
    description: "Compile personalized executive memo highlighting missed decisions for excused team members.",
    trigger_event: "MEETING_ANALYZED",
    action_type: "EMAIL_ABSENTEE_SUMMARY",
    condition_json: '{"attendance_status": "Excused"}',
    is_enabled: true,
    is_active: true,
    last_triggered_at: "2026-10-21 04:15:00",
    execution_count: 36,
    success_count: 36,
  },
  {
    id: "rule-003",
    name: "Escalate Critical Blocker to Team Lead Slack Channel",
    description: "Trigger immediate high-priority alert when an action item is marked as blocked.",
    trigger_event: "TASK_STATUS_BLOCKED",
    action_type: "SLACK_WEBHOOK_ALERT",
    condition_json: '{"priority": ["High", "Urgent"]}',
    is_enabled: true,
    is_active: true,
    last_triggered_at: "2026-10-20 18:22:45",
    execution_count: 15,
    success_count: 15,
  },
];

let auditEvents: AuditEvent[] = [
  {
    id: "aud-001",
    action: "APPROVE",
    actor: "Sarah Jenkins (Team Lead)",
    entity_type: "ActionItem",
    entity_id: "101",
    details: "Approved task 'Complete OAuth 2.0 PKCE integration' for sprint scheduling.",
    timestamp: new Date(Date.now() - 1000 * 60 * 18).toISOString(),
  },
  {
    id: "aud-002",
    action: "SYNC",
    actor: "PersistentBackgroundWorker",
    entity_type: "CalendarEvent",
    entity_id: "cal-ev-101",
    details: "Synchronized deliverable #101 to Google Calendar with 24h reminder notification.",
    timestamp: new Date(Date.now() - 1000 * 60 * 17).toISOString(),
  },
  {
    id: "aud-003",
    action: "CREATE",
    actor: "MeetingAnalyzer (AI)",
    entity_type: "Meeting",
    entity_id: "demo-meeting-q3-security",
    details: "Extracted 3 action items and 2 decisions with verbatim dialogue grounding.",
    timestamp: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
  },
  {
    id: "aud-004",
    action: "TRIGGER",
    actor: "RuleAutomationEngine",
    entity_type: "WorkflowRule",
    entity_id: "rule-002",
    details: "Generated personalized briefing email for absent attendee Elena Rostova.",
    timestamp: new Date(Date.now() - 1000 * 60 * 40).toISOString(),
  },
];

let followups: Followup[] = [
  {
    id: "fol-001",
    recipient_name: "Elena Rostova",
    recipient_email: "elena.rostova@acme.corp",
    subject: "Executive Briefing: Q3 Architecture & Security Alignment Decisions",
    meeting_title: "Q3 Architecture & Security Alignment",
    status: "Drafted",
    channel: "Email",
    summary:
      "Hi Elena, you were excused from today's Q3 Architecture review. The team approved mandatory OAuth 2.0 PKCE by Q4. Sarah Jenkins requested your feedback on the 90-day audit retention policy by Friday.",
    summary_preview: "Hi Elena, you were excused from today's Q3 Architecture review. The team approved mandatory OAuth 2.0 PKCE...",
    action_items_count: 1,
  },
  {
    id: "fol-002",
    recipient_name: "Marcus Vance",
    recipient_email: "marcus.vance@acme.corp",
    subject: "Sprint 42 Retrospective Outcome & Burndown Velocity Notes",
    meeting_title: "Sprint 42 Retrospective",
    status: "Sent",
    channel: "Email",
    summary:
      "Sprint burndown velocity summary and reliability refactoring priorities for Sprint 43.",
    summary_preview: "Sprint burndown velocity summary and reliability refactoring priorities for Sprint 43...",
    action_items_count: 2,
    sent_at: "2026-10-19 10:15 AM",
  },
];

export const api = {
  getCurrentUser: (): User => currentUser,
  
  setRole: (role: UserRole): User => {
    currentUser = { ...currentUser, role };
    return currentUser;
  },

  getUsers: (): User[] => users,

  getMeetings: (): Meeting[] => meetings,

  getMeetingById: (id: string): Meeting | undefined => {
    return meetings.find((m) => m.id === id);
  },

  getActionItems: (filters?: { status?: string; user_id?: string }): ActionItem[] => {
    let res = [...actionItems];
    if (filters?.status) {
      res = res.filter((a) => a.status === filters.status);
    }
    if (filters?.user_id) {
      res = res.filter((a) => a.assigned_user_id === filters.user_id);
    }
    return res;
  },

  approveActionItem: (taskId: number, actorId: string): ActionItem | null => {
    const task = actionItems.find((t) => t.id === taskId);
    if (task) {
      task.approval_status = "Approved";
      task.calendar_synced = true;
      auditEvents.unshift({
        id: `aud-${Date.now()}`,
        action: "APPROVE",
        actor: currentUser.full_name,
        entity_type: "ActionItem",
        entity_id: String(taskId),
        details: `Approved task '${task.task}' and triggered calendar synchronization.`,
        timestamp: new Date().toISOString(),
      });
      return task;
    }
    return null;
  },

  rejectActionItem: (taskId: number, actorId: string, reason: string): ActionItem | null => {
    const task = actionItems.find((t) => t.id === taskId);
    if (task) {
      task.approval_status = "Rejected";
      task.status = "Rejected";
      auditEvents.unshift({
        id: `aud-${Date.now()}`,
        action: "REJECT",
        actor: currentUser.full_name,
        entity_type: "ActionItem",
        entity_id: String(taskId),
        details: `Rejected deliverable #${taskId}. Reason: ${reason}`,
        timestamp: new Date().toISOString(),
      });
      return task;
    }
    return null;
  },

  updateActionItemStatus: (taskId: number, newStatus: TaskStatus): ActionItem | null => {
    const task = actionItems.find((t) => t.id === taskId);
    if (task) {
      task.status = newStatus;
      if (newStatus === "Blocked") {
        task.is_blocked = true;
        task.blocker_reason = "Flagged as blocked during active sprint execution.";
      } else if (newStatus === "Completed") {
        task.is_blocked = false;
        task.blocker_reason = null;
      }
      auditEvents.unshift({
        id: `aud-${Date.now()}`,
        action: "UPDATE",
        actor: currentUser.full_name,
        entity_type: "ActionItem",
        entity_id: String(taskId),
        details: `Status updated to '${newStatus}'.`,
        timestamp: new Date().toISOString(),
      });
      return task;
    }
    return null;
  },

  reassignActionItem: (taskId: number, newUserId: string): ActionItem | null => {
    const task = actionItems.find((t) => t.id === taskId);
    const targetUser = users.find((u) => u.id === newUserId);
    if (task && targetUser) {
      const priorOwner = task.assigned_to;
      task.assigned_to = targetUser.full_name;
      task.assigned_user_id = targetUser.id;
      auditEvents.unshift({
        id: `aud-${Date.now()}`,
        action: "REASSIGN",
        actor: currentUser.full_name,
        entity_type: "ActionItem",
        entity_id: String(taskId),
        details: `Reassigned task from ${priorOwner} to ${targetUser.full_name}.`,
        timestamp: new Date().toISOString(),
      });
      return task;
    }
    return null;
  },

  getDecisions: (): Decision[] => decisions,

  getProjects: (): Project[] => projects,

  createProject: (name: string, description: string, targetDate: string): Project => {
    const newProj: Project = {
      id: `proj-${Date.now()}`,
      name,
      description,
      target_date: targetDate,
      status: "Active",
      action_items_count: 0,
      completed_items_count: 0,
    };
    projects.push(newProj);
    auditEvents.unshift({
      id: `aud-${Date.now()}`,
      action: "CREATE",
      actor: currentUser.full_name,
      entity_type: "Project",
      entity_id: newProj.id,
      details: `Created new project '${name}'.`,
      timestamp: new Date().toISOString(),
    });
    return newProj;
  },

  getIntegrations: (): IntegrationStatus[] => integrations,

  testIntegration: (provider: string): { status: string; message: string; latency_ms: number } => {
    const int = integrations.find((i) => i.provider === provider);
    if (int) {
      int.status = "Connected";
      int.connection_status = "Connected";
      int.last_sync = "Just now";
      int.last_sync_at = "Just now";
      int.sync_count += 1;
    }
    return {
      status: "success",
      message: `${provider.toUpperCase()} handshake and OAuth token verification verified successfully.`,
      latency_ms: Math.floor(Math.random() * 80) + 45,
    };
  },

  getWorkflowRules: (): WorkflowRule[] => workflowRules,

  toggleWorkflowRule: (id: string): WorkflowRule | null => {
    const rule = workflowRules.find((r) => r.id === id);
    if (rule) {
      rule.is_enabled = !rule.is_enabled;
      rule.is_active = rule.is_enabled;
      return rule;
    }
    return null;
  },

  triggerWorkflowRule: (id: string): { status: string; message: string } => {
    const rule = workflowRules.find((r) => r.id === id);
    if (rule) {
      rule.execution_count += 1;
      rule.success_count += 1;
      rule.last_triggered_at = new Date().toISOString();
      auditEvents.unshift({
        id: `aud-${Date.now()}`,
        action: "TRIGGER",
        actor: currentUser.full_name,
        entity_type: "WorkflowRule",
        entity_id: rule.id,
        details: `Manually triggered automation rule '${rule.name}'.`,
        timestamp: new Date().toISOString(),
      });
      return { status: "success", message: `Rule '${rule.name}' executed successfully.` };
    }
    return { status: "error", message: "Rule not found." };
  },

  getAuditEvents: (limit: number = 50): AuditEvent[] => {
    return auditEvents.slice(0, limit);
  },

  getFollowups: (): Followup[] => followups,

  sendFollowup: (id: string): Followup | null => {
    const fol = followups.find((f) => f.id === id);
    if (fol) {
      fol.status = "Sent";
      fol.sent_at = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      auditEvents.unshift({
        id: `aud-${Date.now()}`,
        action: "SEND",
        actor: currentUser.full_name,
        entity_type: "Followup",
        entity_id: fol.id,
        details: `Dispatched meeting briefing to ${fol.recipient_name} (${fol.recipient_email}).`,
        timestamp: new Date().toISOString(),
      });
      return fol;
    }
    return null;
  },

  searchKnowledge: (query: string): KnowledgeSearchResult => {
    const qLower = query.toLowerCase();
    const results = [];
    
    for (const m of meetings) {
      if (m.title.toLowerCase().includes(qLower) || m.executive_summary?.toLowerCase().includes(qLower)) {
        results.push({
          id: m.id,
          title: m.title,
          type: "Meeting Dossier",
          excerpt: m.executive_summary || m.title,
          content: m.executive_summary || m.title,
          date: m.date,
          relevance: 0.94,
          similarity: 0.94,
        });
      }
    }
    
    for (const d of decisions) {
      if (d.title.toLowerCase().includes(qLower) || d.rationale.toLowerCase().includes(qLower)) {
        results.push({
          id: `dec-${d.id}`,
          title: d.title,
          type: "Decision Register",
          excerpt: d.rationale,
          content: `${d.title} - ${d.rationale}`,
          date: "2026-10-20",
          relevance: 0.98,
          similarity: 0.98,
        });
      }
    }

    if (results.length === 0) {
      results.push({
        id: "demo-meeting-q3-security",
        title: "Q3 Architecture & Security Alignment",
        type: "Transcript Segment",
        excerpt: "Sarah Jenkins: 'The team decided to mandate OAuth 2.0 with PKCE and retain audit logs for 90 days.'",
        content: "Sarah Jenkins: 'The team decided to mandate OAuth 2.0 with PKCE and retain audit logs for 90 days.'",
        date: "2026-10-20",
        relevance: 0.88,
        similarity: 0.88,
      });
    }

    return {
      results,
      search_time_ms: 38,
    };
  },

  askAI: (question: string): { answer: string; confidence: string; sources: Array<{ title: string; excerpt: string }> } => {
    const qLower = question.toLowerCase();
    if (qLower.includes("oauth") || qLower.includes("pkce") || qLower.includes("auth")) {
      return {
        answer:
          "During the Q3 Architecture & Security Alignment review, engineering leadership unanimously approved mandatory migration to OAuth 2.0 with PKCE for all client authentication by Q4. Alex Chen is assigned to complete the microservice gateway integration by Friday, Oct 24th.",
        confidence: "High",
        sources: [
          {
            title: "Q3 Architecture & Security Alignment",
            excerpt: "Alex Chen: 'I will complete the OAuth 2.0 PKCE integration by this Friday.'",
          },
          {
            title: "Executive Decision Register #201",
            excerpt: "Mandate OAuth 2.0 with PKCE for all client authentication.",
          },
        ],
      };
    } else if (qLower.includes("decision") || qLower.includes("decide")) {
      return {
        answer:
          "Key decisions confirmed across recent sessions include: 1) Mandating OAuth 2.0 with PKCE for all client authentication, and 2) Enforcing a 90-day immutable compliance audit trail retention policy.",
        confidence: "High",
        sources: [
          {
            title: "Decision Register #201",
            excerpt: "Mandate OAuth 2.0 with PKCE for all client authentication.",
          },
          {
            title: "Decision Register #202",
            excerpt: "Enforce 90-day immutable compliance audit trail retention.",
          },
        ],
      };
    } else if (qLower.includes("task") || qLower.includes("action") || qLower.includes("commit")) {
      return {
        answer:
          "Current high-priority commitments include: 1) Alex Chen completing OAuth 2.0 PKCE integration by Friday Oct 24th, 2) Priya Sharma validating the authentication test suite by Oct 27th, and 3) Resolving the PostgreSQL RDS connection pool bottleneck.",
        confidence: "High",
        sources: [
          {
            title: "Action Item #101",
            excerpt: "Complete OAuth 2.0 PKCE integration across microservice gateways.",
          },
          {
            title: "Action Item #103",
            excerpt: "Optimize connection pooling parameters to prevent database bottleneck.",
          },
        ],
      };
    }

    return {
      answer:
        "Based on cross-meeting organizational synthesis, engineering deliverables are aligned toward the Q4 security and reliability milestones. Key commitments are assigned with calendar synchronization enabled.",
      confidence: "Medium",
      sources: [
        {
          title: "Q3 Architecture & Security Alignment",
          excerpt: "Sarah Jenkins: 'All clients must mandate PKCE by Q4. Let's make sure tasks are synced to Google Calendar.'",
        },
      ],
    };
  },
};
