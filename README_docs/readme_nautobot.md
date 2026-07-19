## Installing Nautobot via Podman

This setup deploys Nautobot, PostgreSQL, and Redis within a unified Pod structure. Because containers inside the same Pod share a network namespace, they communicate over `127.0.0.1` natively.

### Prerequisites

Ensure your local Podman machine is running. On macOS, if you encounter connection issues, verify your virtualization backend is initialized (`podman machine start`).

### Deployment Steps

#### 1. Create the Unified Pod
Create a single Pod wrapper named `nautobot-pod` and explicitly expose Nautobot's web interface port (`8000`) to your local machine:

```bash
podman pod create --name nautobot-pod -p 8000:8000
```

#### 2. Start Redis Inside the Pod
Spin up the Redis cache container directly inside the Pod using a persistent volume:

```bash
podman run -d --pod nautobot-pod --name nautobot-redis   -v nautobot-redis-data:/data:Z   docker.io/library/redis:6-alpine redis-server --appendonly yes
```

#### 3. Start PostgreSQL Inside the Pod
Inject the database container into the same Pod with local data persistence:

```bash
podman run -d --pod nautobot-pod --name nautobot-db \
  -e POSTGRES_DB=nautobot \
  -e POSTGRES_USER=nautobot \
  -e POSTGRES_PASSWORD=nautobotpass \
  -v nautobot-db-data:/var/lib/postgresql/data:Z \
  docker.io/library/postgres:14-alpine
```

#### 4. Start Nautobot
Launch the Nautobot application container inside the Pod. Point the database and Redis configuration variables directly to localhost (`127.0.0.1`):

```bash
podman run -d --pod nautobot-pod --name nautobot-web \
-e NAUTOBOT_DB_HOST=127.0.0.1   \
-e NAUTOBOT_DB_NAME=nautobot   \
-e NAUTOBOT_DB_USER=nautobot   \
-e NAUTOBOT_DB_PASSWORD=nautobot   \
-e NAUTOBOT_REDIS_HOST=127.0.0.1   \
-e NAUTOBOT_REDIS_PORT=6379   \
-e NAUTOBOT_SECRET_KEY=nautobot   \
docker.io/networktocode/nautobot:stable-py3.13
```

### Verifying the Launch

Give the environment roughly 10 to 15 seconds to execute the initial database migrations, then check the runtime status:

```bash
podman ps --filter pod=nautobot-pod
```

All three containers (`nautobot-web`, `nautobot-db`, and `nautobot-redis`) should display a status of **Up**. 

Access the Nautobot web UI locally by navigating to: **http://localhost:8000**
nautobot-podman-setup.md
Displaying nautobot-podman-setup.md.