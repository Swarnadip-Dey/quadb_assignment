# Backend Dockerfile

# Stage 1: Build Stage
FROM python:3.9-slim AS backend-build

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app/

# Stage 2: Final image (for running the app)
FROM python:3.9-slim

WORKDIR /app

# Copy files from the build stage
COPY --from=backend-build /app /app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Install necessary dependencies again in final stage (if needed)
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["flask", "run"]
