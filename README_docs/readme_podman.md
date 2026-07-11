## Podman Installation & Setup for macOS

This guide covers installing Podman on macOS and properly initializing the virtual machine environment using Apple's native hypervisor to prevent common connection and virtualization errors.

### Step 1: Install Podman Packages
Use Homebrew to install the Podman CLI and Podman Desktop application:

```bash
brew install podman
brew install podman-desktop
```

### Step 2: Clean Existing VM States (If Upgrading/Resetting)
If you have a previously failed or partially configured machine instance, forcefully remove it to ensure a clean slate:

```bash
podman machine rm -f podman-machine-default
```

### Step 3: Initialize the Native Apple Hypervisor Machine
Initialize a brand new Linux virtual machine instance explicitly configured to utilize Apple's native hypervisor backend (`applehv`). This bypasses standard `libkrun` / `krunkit` binary environment bottlenecks:

```bash
podman machine init --provider applehv
```

### Step 4: Launch the Podman Engine
Spin up the freshly initialized environment to open the local Unix socket bridge:

```bash
podman machine start
```

### Step 5: Verify the Connection
Test the end-to-end connection between your Mac CLI and the lightweight Linux container backend:

```bash
podman info
```
If configured correctly, this will return a comprehensive system breakdown of your local environment instead of socket connection errors.
podman-macos-setup.md
Displaying podman-macos-setup.md.