"""Todo web interfaces module.

This module provides web-based interfaces for the todo application:
- Streamlit UI (streamlit)
- Flask UI (flask)
- Pure Python HTTP server (http_server)
"""

from .streamlit import main as run_streamlit

__all__ = ["run_streamlit"]
