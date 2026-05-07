from pathlib import Path


def test_app_file_exists():
    """Ensure the Flask application file is present."""
    assert Path("app.py").is_file(), "app.py must exist for the Flask app."
