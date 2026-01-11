import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the Streamlit app
from todo.web.streamlit import main

if __name__ == "__main__":
    main()