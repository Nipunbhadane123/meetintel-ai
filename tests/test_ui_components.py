from unittest.mock import MagicMock, patch
from ui.components import (
    render_status_badge,
    render_evidence_quote,
    metric_card,
    safe_escape,
    render_integration_card
)
from integrations.manager import IntegrationCenterManager
from storage import models

def test_safe_escape_none_and_types():
    # Test None handling (direct cause of AttributeError in html.escape)
    assert safe_escape(None) == ""
    assert safe_escape(None, default="N/A") == "N/A"
    assert safe_escape(None, default="<none>") == "&lt;none&gt;"
    
    # Test numeric types
    assert safe_escape(42) == "42"
    assert safe_escape(3.14159) == "3.14159"
    assert safe_escape(True) == "True"
    
    # Test arbitrary objects
    assert safe_escape({"key": "val"}) == "{&#x27;key&#x27;: &#x27;val&#x27;}"
    
    # Test XSS string
    raw_xss = '<script>alert("hacked")</script>'
    escaped = safe_escape(raw_xss)
    assert "<script>" not in escaped
    assert "&lt;script&gt;" in escaped

def test_render_status_badge_variants():
    # Green/Completed
    approved_badge = render_status_badge("Approved")
    assert "badge-completed" in approved_badge
    assert "✓" in approved_badge

    # Purple/Processing
    in_prog_badge = render_status_badge("In Progress")
    assert "badge-processing" in in_prog_badge
    assert "⚡" in in_prog_badge

    # Amber/Pending
    pending_badge = render_status_badge("Pending Approval")
    assert "badge-pending" in pending_badge
    assert "⏱" in pending_badge

    # Red/Blocked / Expired / Needs attention
    blocked_badge = render_status_badge("Blocked")
    assert "badge-failed" in blocked_badge
    assert "⚠️" in blocked_badge

    expired_badge = render_status_badge("Authentication expired")
    assert "badge-failed" in expired_badge
    assert "⚠️" in expired_badge

    needs_attn_badge = render_status_badge("Needs attention")
    assert "badge-failed" in needs_attn_badge

    # Demo
    demo_badge = render_status_badge("Connected — Demo")
    assert "badge-demo" in demo_badge
    assert "🧪" in demo_badge

    # Disconnected / Neutral
    disconnected_badge = render_status_badge("Not linked")
    assert "badge-neutral" in disconnected_badge

    # None handling
    none_badge = render_status_badge(None)
    assert "badge-neutral" in none_badge
    assert "Unknown" in none_badge

def test_evidence_quote_escaping():
    malicious_transcript = "<script>alert('xss')</script> & \"quote\" 'apostrophe'"
    safe_out = safe_escape(malicious_transcript)
    assert "<script>" not in safe_out
    assert "&lt;script&gt;" in safe_out
    assert "&amp;" in safe_out
    assert "&quot;" in safe_out

def test_integration_manager_build_status_dict():
    im = IntegrationCenterManager(org_id="org-default-001")
    
    # Case 1: No DB connection record
    status_none = im._build_status_dict(
        prov_key="google_calendar",
        name="Google Calendar",
        category="Calendar & Task Scheduling",
        conn=None,
        is_demo_mode=False,
        setup_guide="Setup guide test",
        default_demo_email="demo@acmeglobal.io"
    )
    assert status_none["status"] == "Not configured"
    assert status_none["account_email"] is None
    assert status_none["last_sync"] == "Never"
    assert status_none["last_result"] == "Connector not initialized."
    
    # Case 2: Connection with error and None last_import_result
    error_conn = models.IntegrationConnection(
        provider="google_calendar",
        connection_status="Needs attention",
        error_message="Refresh token expired",
        account_email=None,
        last_sync_at=None,
        last_import_result=None
    )
    status_err = im._build_status_dict(
        prov_key="google_calendar",
        name="Google Calendar",
        category="Calendar & Task Scheduling",
        conn=error_conn,
        is_demo_mode=False,
        setup_guide="Setup guide test",
        default_demo_email="demo@acmeglobal.io"
    )
    assert status_err["status"] == "Authentication expired"
    assert status_err["account_email"] is None
    assert status_err["last_sync"] == "Never"
    assert "Refresh token expired" in status_err["last_result"]
    assert status_err["last_result"] is not None

def test_render_integration_card_resilience_with_nones():
    """Ensure render_integration_card handles None values without raising AttributeError."""
    info_with_nones = {
        "name": "Google Calendar",
        "status": "Authentication expired",
        "account_email": None,
        "last_sync": None,
        "last_result": None,
        "setup_guide": None
    }
    
    def fake_cols(spec):
        count = len(spec) if isinstance(spec, list) else int(spec)
        return [MagicMock() for _ in range(count)]
    
    with patch("streamlit.container"), \
         patch("streamlit.columns", side_effect=fake_cols), \
         patch("streamlit.markdown") as mock_markdown, \
         patch("streamlit.caption"), \
         patch("streamlit.button", return_value=False):
        
        # Must execute without throwing AttributeError: 'NoneType' object has no attribute 'replace'
        render_integration_card("google_calendar", info_with_nones)
        assert mock_markdown.called

def test_get_icon_svg():
    from ui.components import get_icon_svg
    svg = get_icon_svg("target", size=20, color="#6C4DFF")
    assert "<svg" in svg
    assert 'xmlns="http://www.w3.org/2000/svg"' in svg
    assert 'width="20"' in svg
    assert 'height="20"' in svg
    assert 'stroke="#6C4DFF"' in svg
    assert 'lucide-target' in svg

    # Fallback lookup
    svg_fallback = get_icon_svg("unknown-icon-name")
    assert "<svg" in svg_fallback
    assert 'lucide-unknown-icon-name' in svg_fallback

def test_metric_card_renders():
    from ui.components import metric_card
    with patch("streamlit.markdown") as mock_markdown:
        metric_card("Test Metric", "42", "target", "Support text")
        assert mock_markdown.called
        rendered_html = mock_markdown.call_args[0][0]
        assert "Test Metric" in rendered_html
        assert "42" in rendered_html
        assert "Support text" in rendered_html
        assert "<svg" in rendered_html

def test_page_header_renders():
    from ui.components import page_header
    with patch("streamlit.markdown") as mock_markdown:
        page_header("Test Title", subtitle="Test Subtitle", category="Test Category", badge_text="Live", icon="sparkles")
        assert mock_markdown.called
        rendered_html = mock_markdown.call_args[0][0]
        assert "Test Title" in rendered_html
        assert "Test Subtitle" in rendered_html
        assert "Test Category" in rendered_html
        assert "<svg" in rendered_html

