## Deploying an Ansible Development Environment via Podman

This guide covers setting up a persistent local Ansible development environment container using Podman. It maps a local playbook directory into the container, allowing you to run, test, and write playbooks directly from your local IDE while executing them in a clean runtime environment.

### Prerequisites

Ensure your local Podman machine is running. On macOS, if you encounter connection issues, verify your virtualization backend is initialized (`podman machine start`).

### Deployment Steps

#### 1. Create a Project Directory (Local Host)
Create a directory on your local machine to store your Ansible configuration, inventories, and playbooks:

```bash
mkdir -p ~/ansible-dev/playbooks
cd ~/ansible-dev
```

#### 2. Launch the Ansible Container
Run the container in a detached interactive state. This command binds your local `~/ansible-dev` directory to the container's workspace and applies the correct SELinux/container volume flags (`:Z`):

```bash
podman run -d \
  --name ansible-dev \
  -v ~/ansible-dev:/workspace:Z \
  -w /workspace \
  docker.io/willhallonline/ansible:latest \
  sleep infinity
```

### Running Ansible Commands

Because the container runs persistently in the background, you can execute commands inside it directly from your terminal.

#### Verify the Installation
Check the installed Ansible version and its configuration paths:

```bash
podman exec -it ansible-dev ansible --version
```

#### Run a Playbook
To run a playbook (`site.yml`) located in your local directory, execute it through the container context:

```bash
podman exec -it ansible-dev ansible-playbook playbooks/site.yml -i playbooks/inventory.ini
```

### Managing the Container

* **Stop the container:** `podman stop ansible-dev`
* **Start the container:** `podman start ansible-dev`
* **Access the container shell:** `podman exec -it ansible-dev /bin/sh`
ansible-podman-setup.md
Displaying ansible-podman-setup.md.