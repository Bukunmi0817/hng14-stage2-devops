# HNG Stage 2 DevOps — Containerized Microservices

A job processing system with three services containerized with Docker and deployed via a full CI/CD pipeline.

## Services

- **Frontend** (Node.js/Express) — Job submission UI on port 3000
- **API** (Python/FastAPI) — Creates and serves job status on port 8000
- **Worker** (Python) — Processes jobs from Redis queue
- **Redis** — Shared message queue between API and Worker

## Prerequisites

- Docker and Docker Compose installed
- Git

## How to Run Locally

1. Clone the repository:
   git clone https://github.com/Bukunmi0817/hng14-stage2-devops.git
   cd hng14-stage2-devops

2. Create a .env file from the example:
   cp api/.env.example .env

3. Edit .env and set your values:
   REDIS_PASSWORD=yourpassword
   APP_ENV=production

4. Start the full stack:
   docker compose up --build

5. Open your browser at http://localhost:3000

## Successful Startup

You should see all services healthy:

   Container hng14-stage2-devops-redis-1    Healthy
   Container hng14-stage2-devops-api-1      Healthy
   Container hng14-stage2-devops-worker-1   Started
   Container hng14-stage2-devops-frontend-1 Started

## Stopping the Stack

   docker compose down

## CI/CD Pipeline

GitHub Actions pipeline runs on every push to main:

lint → test → build → security scan → integration test → deploy

- Lint: flake8 (Python), eslint (JavaScript), hadolint (Dockerfiles)
- Test: pytest with Redis mocked, coverage report uploaded as artifact
- Build: Images built and pushed to local registry, tagged with git SHA and latest
- Security: Trivy scans all images, fails on CRITICAL CVEs
- Integration: Full stack spun up, job submitted and polled until completed
- Deploy: Rolling update to production server with health check gate

## Environment Variables

See api/.env.example for all required variables.

## Architecture

All services communicate over a named internal Docker network.
Redis is not exposed on the host machine.
Services only start after dependencies are confirmed healthy.
