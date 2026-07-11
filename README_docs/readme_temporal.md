## Installing Temporal via Podman

This setup deploys a local Temporal development server inside a standalone Podman container, exposing the gRPC server and Web UI endpoints to your local machine.

### Prerequisites

Ensure your local Podman machine is running. On macOS, if you encounter connection issues, verify your virtualization backend is initialized (`podman machine start`).

### Deployment Steps

#### 1. Launch the Temporal Dev Server
Run the Temporal dev server container, explicitly binding the necessary runtime and UI ports to localhost:

```bash
podman run -d --name temporal-dev \
  -p 127.0.0.1:7233:7233 \
  -p 127.0.0.1:8233:8233 \
  docker.io/temporalio/admin-tools:latest \
  temporal server start-dev --ip 0.0.0.0
```

### Verifying the Launch

Check the runtime status of the container to ensure it is running properly:

```bash
podman ps --filter name=temporal-dev
```

### Interface Endpoints

Once initialized, the services are accessible via the following local endpoints:

* **Temporal gRPC Server (SDK Connection):** `127.0.0.1:7233`
* **Temporal Web UI:** **http://localhost:8233**
temporal-podman-setup.md
Displaying temporal-podman-setup.md.