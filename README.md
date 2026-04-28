# Meet Redirect Service

A lightweight Python web server that redirects all root traffic to a specified Google Meet URL. Designed to run behind Cloudflare or a similar proxy for the domain `meet.wehost.co.in`.

## Features

- **Automatic Redirect**: Redirects `GET /` to the URL configured in `MEET_URL`.
- **Health Endpoint**: `GET /health` returns a 200 OK for load balancer/service monitoring.
- **Dockerized**: Ready for containerized deployment.

## Configuration

The application is configured via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `MEET_URL` | The full Google Meet URL to redirect to. | (Required) |
| `PORT` | The port the server listens on inside the container. | `8080` |

## Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   export MEET_URL="https://meet.google.com/xxx-yyyy-zzz"
   python app.py
   ```

## Deployment with Docker

### Using Docker Compose (Recommended)

1. Create a `.env` file or export the variable:
   ```bash
   echo "MEET_URL=https://meet.google.com/xxx-yyyy-zzz" > .env
   ```

2. Start the container:
   ```bash
   docker-compose up -d
   ```

### Using Docker CLI

1. Build the image:
   ```bash
   docker build -t meet-redirect .
   ```

2. Run the container:
   ```bash
   docker run -d \
     -p 8080:8080 \
     -e MEET_URL="https://meet.google.com/xxx-yyyy-zzz" \
     --name meet-redirect \
     meet-redirect
   ```

## Cloudflare Setup

Ensure your Cloudflare DNS record for `meet.wehost.co.in` points to the IP address of the server running this container, and that "Proxy status" (the orange cloud) is enabled.
