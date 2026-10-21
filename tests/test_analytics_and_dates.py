import pytest
from datetime import date, timedelta
from utils.date_parser import parse_relative_deadline, get_deadline_sort_key
from utils.meeting_analytics import calculate_meeting_cost_roi, format_slack_executive_brief, format_markdown_executive_memo

def test_date_parser_iso_date():
    ref = date(2026, 10, 21)
    res = parse_relative_deadline("2026-10-24", reference_date=ref)
    assert res["normalized_date"] == "2026-10-24"
    assert res["is_ambiguous"] is False
    assert res["days_remaining"] == 3
    assert "Due in 3 days" in res["countdown_label"]

def test_date_parser_relative_terms():
    ref = date(2026, 10, 21)  # Wednesday
    
    # Tomorrow
    res_tomorrow = parse_relative_deadline("tomorrow", reference_date=ref)
    assert res_tomorrow["normalized_date"] == "2026-10-22"
    assert res_tomorrow["countdown_label"] == "Due tomorrow"

    # Today / EOD
    res_today = parse_relative_deadline("by EOD today", reference_date=ref)
    assert res_today["normalized_date"] == "2026-10-21"
    assert res_today["countdown_label"] == "Due today"

    # In 5 days
    res_in_days = parse_relative_deadline("in 5 days", reference_date=ref)
    assert res_in_days["normalized_date"] == "2026-10-26"
    assert res_in_days["days_remaining"] == 5

    # Day of week: "by Friday" (Wed + 2 days = Friday Oct 23)
    res_friday = parse_relative_deadline("by Friday", reference_date=ref)
    assert res_friday["normalized_date"] == "2026-10-23"

def test_date_parser_ambiguous_and_overdue():
    ref = date(2026, 10, 21)
    
    # Ambiguous phrase
    res_ambiguous = parse_relative_deadline("sometime soon next quarter", reference_date=ref)
    assert res_ambiguous["is_ambiguous"] is True
    assert res_ambiguous["normalized_date"] is None

    # Overdue date
    res_overdue = parse_relative_deadline("2026-10-18", reference_date=ref)
    assert res_overdue["days_remaining"] == -3
    assert "Overdue" in res_overdue["countdown_label"]

def test_deadline_sort_key():
    ref = date(2026, 10, 21)
    dates = ["sometime soon", "2026-10-25", "2026-10-22", "asap"]
    sorted_dates = sorted(dates, key=get_deadline_sort_key)
    # Concrete dates should sort before ambiguous ones
    assert sorted_dates[0] == "2026-10-22"
    assert sorted_dates[1] == "2026-10-25"

def test_meeting_cost_roi_calculation():
    # 30 minute meeting (1800s), 4 speakers, 4 actions, 2 decisions, $100/hr avg rate
    stats = calculate_meeting_cost_roi(
        duration_seconds=1800.0,
        speaker_count=4,
        action_items_count=4,
        decisions_count=2,
        avg_hourly_rate=100.0,
        blocked_count=0
    )
    
    assert stats["duration_minutes"] == 30.0
    assert stats["participants"] == 4
    # 0.5 hours * 4 participants * $100 = $200
    assert stats["estimated_total_cost_usd"] == 200.0
    assert stats["decisions_per_hour"] == 4.0
    assert stats["actions_per_hour"] == 8.0
    assert stats["efficiency_score"] >= 80
    assert "A" in stats["efficiency_grade"]

def test_meeting_cost_roi_penalty_for_blockers():
    # Meeting with high blockers penalty
    stats = calculate_meeting_cost_roi(
        duration_seconds=3600.0,
        speaker_count=5,
        action_items_count=3,
        decisions_count=0,
        avg_hourly_rate=75.0,
        blocked_count=3
    )
    assert stats["efficiency_score"] < 50
    assert "D" in stats["efficiency_grade"]

def test_format_slack_and_markdown_brief():
    decisions = [{"id": 1, "title": "Migrate to OAuth PKCE", "rationale": "Security compliance"}]
    actions = [{"task": "Deploy gateway", "assigned_to": "Alex", "deadline": "Friday", "priority": "High", "status": "In Progress"}]
    
    # Slack blocks
    slack_data = format_slack_executive_brief(
        meeting_title="Sprint Security Sync",
        date_str="2026-10-21",
        executive_summary="Team confirmed PKCE rollout timeline.",
        decisions=decisions,
        action_items=actions
    )
    assert "blocks" in slack_data
    assert len(slack_data["blocks"]) >= 4

    # Markdown memo
    memo = format_markdown_executive_memo(
        meeting_title="Sprint Security Sync",
        date_str="2026-10-21",
        executive_summary="Team confirmed PKCE rollout timeline.",
        decisions=decisions,
        action_items=actions
    )
    assert "# 📋 Executive Meeting Briefing" in memo
    assert "Migrate to OAuth PKCE" in memo
    assert "| Deploy gateway |" in memo
