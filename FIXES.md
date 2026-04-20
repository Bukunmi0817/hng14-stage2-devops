# FIXES.md

## Bug 1 — api/main.py, line 9
**Problem:** Redis connection hardcoded to `localhost` — fails inside Docker where services communicate by service name.
**Fix:** Changed to `os.environ.get("REDIS_HOST", "redis")` to read host from environment variable.

## Bug 2 — api/main.py, line 9
**Problem:** Redis connection had no password authentication despite REDIS_PASSWORD being defined in .env.
**Fix:** Added `password=os.environ.get("REDIS_PASSWORD", "")` to Redis connection.

## Bug 3 — api/main.py, line 9
**Problem:** Redis port hardcoded to 6379 instead of reading from environment.
**Fix:** Changed to `int(os.environ.get("REDIS_PORT", 6379))`.

## Bug 4 — api/main.py
**Problem:** No /health endpoint — required for Docker HEALTHCHECK.
**Fix:** Added `GET /health` endpoint returning `{"status": "ok"}`.

## Bug 5 — api/main.py, line 12
**Problem:** Queue name was "job" in the API but needed to be consistent.
**Fix:** Renamed queue to "jobs" consistently across API and worker.

## Bug 6 — api/main.py, line 20
**Problem:** `r.hget()` returns bytes — calling `.decode()` would fail with decode_responses=True.
**Fix:** Added `decode_responses=True` to Redis client, removed manual `.decode()` call.

## Bug 7 — worker/worker.py, line 6
**Problem:** Redis connection hardcoded to `localhost` — fails inside Docker.
**Fix:** Changed to `os.environ.get("REDIS_HOST", "redis")`.

## Bug 8 — worker/worker.py, line 6
**Problem:** No password authentication on Redis connection.
**Fix:** Added `password=os.environ.get("REDIS_PASSWORD", "")`.

## Bug 9 — worker/worker.py
**Problem:** `signal` module imported but never used — no graceful shutdown handler.
**Fix:** Added SIGTERM and SIGINT handlers to allow graceful container shutdown.

## Bug 10 — worker/worker.py
**Problem:** Infinite `while True` loop with no way to stop cleanly.
**Fix:** Changed to `while running` with signal handler setting `running = False`.

## Bug 11 — frontend/app.js, line 6
**Problem:** API_URL hardcoded to `http://localhost:8000` — fails inside Docker.
**Fix:** Changed to `process.env.API_URL || "http://api:8000"` to read from environment.

## Bug 12 — frontend/app.js
**Problem:** No /health endpoint for Docker HEALTHCHECK.
**Fix:** Added `GET /health` endpoint returning `{"status": "ok"}`.

## Bug 13 — api/.env
**Problem:** Real credentials committed to the repository — critical security violation.
**Fix:** Added api/.env to .gitignore, removed from git tracking, created api/.env.example with placeholder values.

## Bug 14 — api/requirements.txt
**Problem:** No version pinning on dependencies — breaks reproducible builds.
**Fix:** Pinned all dependencies to specific versions.

## Bug 15 — worker/requirements.txt
**Problem:** No version pinning on redis dependency.
**Fix:** Pinned redis to specific version.

## Bug 16 — frontend/package.json
**Problem:** No eslint dependency defined — CI/CD pipeline requires linting.
**Fix:** Added eslint to devDependencies and added lint script.
