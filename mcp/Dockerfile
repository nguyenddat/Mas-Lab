FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /mcp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

# Expose port if needed, but for stdio/sse it depends on runner.
# Assuming this might be run via some other connector or just standalone.
# If it's a server that listens, we might need EXPOSE.
# Based on FastMCP default, it might run on a port or stdio.
# The user didn't specify, but `mcp.run()` often defaults to stdio or acts as a server.
# Let's assume standard python run for now.