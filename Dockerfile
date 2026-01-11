# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory in container
WORKDIR /app

# Copy project files
COPY . .

# Install uv package manager
RUN pip install --no-cache-dir uv

# Install project dependencies using uv
RUN uv sync

# Expose port 8501 for Streamlit
EXPOSE 8501

# Command to run the Streamlit app
CMD ["uv", "run", "streamlit", "run", "src/todo/web/streamlit.py", "--server.address", "0.0.0.0", "--server.port", "8501"]