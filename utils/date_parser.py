import re
from datetime import datetime, date, timedelta
from typing import Optional, Tuple, Dict, Any

WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}

def parse_relative_deadline(
    deadline_str: Optional[str],
    reference_date: Optional[date] = None
) -> Dict[str, Any]:
    """
    Parses natural language meeting deadline expressions (e.g. 'by Friday',
    'tomorrow', 'in 3 days', 'end of month', 'sometime soon') into a structured
    target ISO date, urgency score, and human-friendly countdown label.
    """
    if not deadline_str or not deadline_str.strip():
        return {
            "raw": "",
            "normalized_date": None,
            "is_ambiguous": True,
            "countdown_label": "No deadline set",
            "urgency_score": 0,
            "days_remaining": None,
        }

    ref = reference_date or date.today()
    cleaned = deadline_str.strip().lower()
    
    # 1. Check for standard ISO format: YYYY-MM-DD
    iso_match = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", cleaned)
    if iso_match:
        try:
            target = date.fromisoformat(iso_match.group(0))
            return _format_result(deadline_str, target, ref, is_ambiguous=False)
        except ValueError:
            pass

    # 2. Check for standard MM/DD or DD/MM with year
    slash_match = re.search(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b", cleaned)
    if slash_match:
        try:
            parts = [int(p) for p in slash_match.groups()]
            year = parts[2] if parts[2] > 99 else 2000 + parts[2]
            target = date(year, parts[0], parts[1])
            return _format_result(deadline_str, target, ref, is_ambiguous=False)
        except ValueError:
            pass

    # 3. Relative terms: today, tomorrow, eod
    if "today" in cleaned or "eod" in cleaned or "end of day" in cleaned:
        return _format_result(deadline_str, ref, ref, is_ambiguous=False)

    if "tomorrow" in cleaned:
        target = ref + timedelta(days=1)
        return _format_result(deadline_str, target, ref, is_ambiguous=False)

    if "day after tomorrow" in cleaned:
        target = ref + timedelta(days=2)
        return _format_result(deadline_str, target, ref, is_ambiguous=False)

    # 4. In N days / N weeks
    in_days_match = re.search(r"in\s+(\d+)\s+day", cleaned)
    if in_days_match:
        n = int(in_days_match.group(1))
        target = ref + timedelta(days=n)
        return _format_result(deadline_str, target, ref, is_ambiguous=False)

    in_weeks_match = re.search(r"in\s+(\d+)\s+week", cleaned)
    if in_weeks_match:
        n = int(in_weeks_match.group(1))
        target = ref + timedelta(days=n * 7)
        return _format_result(deadline_str, target, ref, is_ambiguous=False)

    # 5. Day of week (e.g. "by friday", "this friday", "next monday")
    for name, target_wd in WEEKDAYS.items():
        pattern = rf"\b(by|this|next|coming)?\s*{name}\b"
        match = re.search(pattern, cleaned)
        if match:
            prefix = match.group(1) or ""
            current_wd = ref.weekday()
            diff = (target_wd - current_wd) % 7
            if diff == 0:
                diff = 7 if "next" in prefix else 0
            elif "next" in prefix:
                diff += 7
            target = ref + timedelta(days=diff)
            return _format_result(deadline_str, target, ref, is_ambiguous=False)

    # 6. End of week / End of month
    if "end of week" in cleaned or "end of the week" in cleaned:
        diff = (4 - ref.weekday()) % 7  # Friday
        target = ref + timedelta(days=diff if diff > 0 else 7)
        return _format_result(deadline_str, target, ref, is_ambiguous=False)

    if "end of month" in cleaned or "end of the month" in cleaned:
        # Last day of current month
        next_month = ref.month % 12 + 1
        year_bump = ref.year + (1 if ref.month == 12 else 0)
        first_of_next = date(year_bump, next_month, 1)
        target = first_of_next - timedelta(days=1)
        return _format_result(deadline_str, target, ref, is_ambiguous=False)

    # 7. Ambiguous expressions (e.g. "sometime soon", "later", "asap", "q4")
    return {
        "raw": deadline_str,
        "normalized_date": None,
        "is_ambiguous": True,
        "countdown_label": f"Ambiguous ({deadline_str.strip()})",
        "urgency_score": 2 if "asap" in cleaned else 1,
        "days_remaining": None,
    }

def _format_result(
    raw: str,
    target: date,
    ref: date,
    is_ambiguous: bool
) -> Dict[str, Any]:
    diff_days = (target - ref).days
    
    if diff_days < 0:
        label = f"Overdue by {-diff_days} day{'' if diff_days == -1 else 's'}"
        urgency = 5
    elif diff_days == 0:
        label = "Due today"
        urgency = 4
    elif diff_days == 1:
        label = "Due tomorrow"
        urgency = 3
    elif diff_days <= 7:
        label = f"Due in {diff_days} days"
        urgency = 2
    else:
        label = f"Due in {diff_days} days ({target.isoformat()})"
        urgency = 1

    return {
        "raw": raw,
        "normalized_date": target.isoformat(),
        "is_ambiguous": is_ambiguous,
        "countdown_label": label,
        "urgency_score": urgency,
        "days_remaining": diff_days,
    }

def get_deadline_sort_key(deadline_str: Optional[str]) -> Tuple[int, str]:
    """
    Returns a deterministic sort tuple (urgency_rank, date_str) for sorting tasks
    where overdue/urgent dates appear first, followed by upcoming, then ambiguous.
    """
    parsed = parse_relative_deadline(deadline_str)
    if parsed["normalized_date"]:
        return (0, parsed["normalized_date"])
    elif parsed["urgency_score"] > 1:
        return (1, "9999-12-31")
    else:
        return (2, "9999-12-31")
