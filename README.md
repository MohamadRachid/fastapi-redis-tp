# FastAPI + Redis with Docker Compose

A minimal multi-container application demonstrating FastAPI (web) and Redis (data) with persistence, custom networks, troubleshooting, cleanup, and optional load balancing across multiple web replicas.

## Prerequisites
- Docker Desktop or Docker Engine + Docker Compose V2
- Git

## Part 1 — Setup (20 min)

### 1) Clone
```bash
git clone <your-fork-or-repo-url> fastapi-redis-tp
cd fastapi-redis-tp
git checkout -b feature/tp
```

### 2) .gitignore
A `.gitignore` is provided to keep the repo clean from caches, venvs, logs, etc.

### 3) Dockerfile & requirements
- `requirements.txt` lists FastAPI, Uvicorn, Redis client.
- Dockerfile builds a slim Python image and starts Uvicorn on port 8000.

### 4) docker-compose.yml
- Defines `web` (FastAPI) and `redis` services.
- Exposes `web` on port `8000`.

### 5) Environment overrides
The app reads env vars:
- `REDIS_HOST` (default `redis`)
- `REDIS_PORT` (default `6379`)
- `REDIS_DB` (default `0`)
- `APP_MESSAGE` (optional)

Override via:
```bash
REDIS_PORT=6380 docker compose up -d   # example
```

### 6) Run locally
```bash
docker compose up --build -d
docker compose ps
```

### 7) Test the API
```bash
curl http://localhost:8000/
curl http://localhost:8000/healthz
```
You should see a JSON response and an incrementing `hits` counter.

### 8) Update README
You're reading it.

---

## Part 2 — Persistence & Networks (15 min)

### 1) Redis persistence
Compose mounts a named volume `redis_data` at `/data`. Redis appends to AOF (`--appendonly yes`) so data survives restarts.

### 2) Default network
Docker Compose creates a project-scoped bridge network automatically. Verify:
```bash
docker network ls
# then inspect:
docker network inspect <project>_app_net
```

### 3) Custom network
`app_net` is defined explicitly so services share a known network for inter-communication and future growth.

### 4) README update
This file documents volumes and networks.

---

## Part 3 — Troubleshooting (15 min)

### Logs
```bash
docker compose logs -f           # all
docker compose logs -f web       # web only
docker compose logs -f redis     # redis only
```

### Exec into containers
```bash
docker compose exec web sh
env | grep REDIS_
apk add curl  # if you used alpine base image
exit
```

---

## Part 4 — Clean-Up (10 min)
```bash
docker compose down              # stop & remove containers + network
docker compose down -v           # also remove volumes (including redis_data)
# Optional: prune leftover resources
docker volume ls
docker network ls
```

---

## Part 5 — Multiple web instances + Load Balancing (5 min)

1) Scale web:
```bash
docker compose up -d --scale web=3 --build
docker compose ps
```
2) Use Nginx (already included) as a simple load balancer:
```bash
curl http://localhost:8080/
```
Nginx uses Docker DNS to route traffic to the `web` service. You can vary `APP_MESSAGE` per replica if you customize the service definitions.

---

## Project Structure
```
app/main.py
Dockerfile
docker-compose.yml
requirements.txt
nginx/nginx.conf
.gitignore
.dockerignore
README.md
REPORT.md
```

## Endpoints
- `GET /` — increments and returns `hits`
- `GET /healthz` — health check & Redis info
