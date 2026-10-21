# Smart Honeypot Frontend — Docker

## Run the frontend container

From this directory (the folder containing `Dockerfile` and `docker-compose.yml`):

```bash
docker compose up --build -d
```

Open `http://localhost:3000`.

The frontend calls the backend through `/backend`, and Nginx forwards those requests to `BACKEND_UPSTREAM`. WebSocket requests to `/backend/ws` are proxied as well.

## Backend connection

By default, Docker expects FastAPI to be available on the host at port `8000`:

```bash
BACKEND_UPSTREAM=host.docker.internal:8000 docker compose up --build -d
```

On Linux, `host.docker.internal` is mapped to the Docker host through `extra_hosts`.

If the backend is another container on a shared Docker network, set `BACKEND_UPSTREAM` to its reachable service/container name and port, for example:

```bash
BACKEND_UPSTREAM=backend:8000 docker compose up --build -d
```

The `backend` container must actually be reachable on the same Docker network. This compose file intentionally does not start, rebuild, or modify the backend, Elasticsearch, or ML service.

## Useful commands

```bash
docker compose logs -f smart-honeypot-frontend
docker compose ps
docker compose down
```

The Orchestrator panel reads the real `GET /honeypots` endpoint and refreshes every 30 seconds. If the request fails, it displays `Orchestrator service is unavailable.` instead of stale cards.
