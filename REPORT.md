# TP: Multi-Container FastAPI + Redis with Docker Compose

**Student:** <Your Name>  
**Date:** <Today’s Date>  
**Project:** DummyRequestCounter

> This report mirrors the structure and tone of the sample provided, step by step.

## Part 1: Setting Up a Simple Multi-Container Application (20 mins)

**1. Clone the git repo.**  
In this step, I initialized a local working folder and cloned the repository into it. I created a dedicated feature branch (`feature/tp`) to keep my changes separate from the class repository.

**2. Update .gitignore.**  
I added a `.gitignore` that excludes Python caches, virtual environments, logs, OS/IDE files, and local Docker artifacts. This keeps the commit history clean and focused on source files.

**3. Update Dockerfile and requirements.txt.**  
I wrote a `requirements.txt` for FastAPI, Uvicorn, and the Redis client, then created a slim `Dockerfile` to containerize the app and run Uvicorn on port 8000.

**4. Update docker-compose to orchestrate.**  
I created `docker-compose.yml` with two services: `web` (FastAPI) and `redis`. `web` builds from the local Dockerfile and exposes port 8000 on the host.

**5. Make Redis config overridable.**  
I updated the code to read `REDIS_HOST`, `REDIS_PORT`, and `REDIS_DB` from environment variables with sensible defaults. This allows configuration overrides at runtime without code changes.

**6. Run containers locally.**  
I built and started the stack with `docker compose up --build -d`. I confirmed both containers were healthy and reachable on the internal network, and that `web` was accessible on `http://localhost:8000`.

**7. Test the API.**  
I tested the root endpoint and the health probe using curl. The `hits` counter increased on each request, proving successful connectivity with Redis.

**8. Update README.**  
I documented prerequisites, run steps, environment overrides, testing methods, and troubleshooting commands.

## Part 2: Persistent Storage and Networks (15 mins)

**1. Add a volume for Redis data.**  
I mounted a named volume `redis_data` to `/data` in the Redis container and enabled append-only persistence. This preserves data across container restarts.

**2. Identify the communication network.**  
I observed that Docker Compose provides an isolated bridge network for this project. Both services are attached to it and can reach each other by service name (`redis`, `web`).

**3. Create a custom network.**  
I explicitly declared `app_net` in `docker-compose.yml` and attached both services to it. This makes networking configuration intentional and ready for future services like a proxy.

**4. Update README.**  
I added notes on the volume and the custom network.

## Part 3: Troubleshooting and Debugging (15 mins)

**1. View container logs.**  
I tailed logs using `docker compose logs -f` and filtered by service when necessary.

**2. Exec into containers.**  
I used `docker compose exec web sh` to open a shell in the web container, verified environment variables, and inspected the filesystem.

## Part 4: Clean-Up (10 mins)

**1. Stop and remove containers.**  
I ran `docker compose down` to stop and remove the containers and the network.

**2. Remove volumes and networks.**  
I used `docker compose down -v` to remove the `redis_data` volume as well, fully resetting the environment.

## Part 5: Multiple Web Instances with Load Balancing (5 mins)

**1. Push branch and open PR.**  
I committed all changes and pushed my `feature/tp` branch to GitHub, then opened a Pull Request for review.

**2. Load-balanced replicas (optional run-time).**  
I demonstrated horizontal scaling with `docker compose up -d --scale web=3`. I added an Nginx reverse proxy to expose a single entrypoint on `http://localhost:8080/`, which forwards traffic to all `web` replicas via Docker DNS.

---

## Evidence & Commands

- Start services:
  - `docker compose up --build -d`
- Test endpoints:
  - `curl http://localhost:8000/`
  - `curl http://localhost:8000/healthz`
- Logs:
  - `docker compose logs -f` (all)  
  - `docker compose logs -f web` / `redis`
- Exec:
  - `docker compose exec web sh`
- Scale:
  - `docker compose up -d --scale web=3`
- Load balancer:
  - `curl http://localhost:8080/`
- Clean-up:
  - `docker compose down`
  - `docker compose down -v`

## What to Submit
- Link to the PR (GitHub).
- This report (`REPORT.md`) or a copied version in your preferred format (e.g., .docx).
- Screenshots of successful runs/tests if your instructor requests them.
