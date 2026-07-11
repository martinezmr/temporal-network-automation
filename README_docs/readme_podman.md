### Start Temporal Server in Podman
```
podman run -d --name temporal-dev \
  -p 127.0.0.1:7233:7233 \
  -p 127.0.0.1:8233:8233 \
  docker.io/temporalio/admin-tools:latest \
  temporal server start-dev --ip 0.0.0.0
```