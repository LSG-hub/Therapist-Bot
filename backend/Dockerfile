# Multi-stage Dockerfile for Therapist Bot Backend with RAG
# Optimized for production deployment with minimal size and security

# ===============================================
# Stage 1: Build Dependencies (Build Stage)
# ===============================================
FROM python:3.12.8-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies needed for building
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies in virtual environment
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ===============================================
# Stage 2: Production Runtime (Runtime Stage)  
# ===============================================
FROM python:3.12.8-slim as runtime

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000 \
    HOST=0.0.0.0

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y \
    # Required for some Python packages
    libgomp1 \
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get autoclean

# Create non-root user for security
RUN groupadd -r therapist && useradd -r -g therapist therapist

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create app directory
WORKDIR /app

# Copy application code
COPY app/ ./app/

# Create necessary directories for RAG data and model cache
RUN mkdir -p /app/data/chroma_data /app/data/sqlite /app/cache && \
    chown -R therapist:therapist /app

# Set Hugging Face cache directory to app-controlled location
ENV HF_HOME=/app/cache \
    TRANSFORMERS_CACHE=/app/cache \
    SENTENCE_TRANSFORMERS_HOME=/app/cache

# Switch to non-root user
USER therapist

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health', timeout=5.0)" || exit 1

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "app.main"]

# ===============================================
# Build Information
# ===============================================
LABEL maintainer="Therapist Bot Team" \
      description="CBT Therapist Bot with RAG capabilities" \
      version="1.0.0" \
      python.version="3.12.8" \
      architecture="RAG-enabled"