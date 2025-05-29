# Base image
FROM python:3.10-slim

# Optional: Install Node.js if you want to build the frontend inside the container
# (You can skip this if you've already built the frontend locally)
# RUN apt update && apt install -y curl && \
#     curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
#     apt install -y nodejs

# Set working directory
WORKDIR /app

# Copy backend code
COPY backend/ ./backend/
COPY .env .env
COPY common/ ./common/
COPY startup.sh .


# Install backend dependencies
RUN pip install --upgrade pip
RUN pip install -r backend/requirements.txt

# Copy frontend build output (assumes it's built locally)
COPY frontend/build/ ./frontend/build/

# Make startup script executable and run it
RUN chmod +x startup.sh
CMD ["./startup.sh"]
