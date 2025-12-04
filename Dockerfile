# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app

# Copy dependency file (even if empty)
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y tzdata cron && \
    ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy project code
COPY . .

# Set up volume mount points for persistence
VOLUME ["/data"]
VOLUME ["/cron"]

# Install cron job
RUN crontab /app/cron/2fa-cron

# Expose API port
EXPOSE 8080

# Start both cron and FastAPI server
CMD cron && uvicorn api:app --host 0.0.0.0 --port 8080
