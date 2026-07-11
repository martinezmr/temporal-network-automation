## Deploying Containerlab via Podman

This guide details how to set up Containerlab inside a Podman environment on macOS. Containerlab allows you to spin up containerized network topologies (using Arista cEOS, Nokia SR-OS, Cisco XRD, FRR, etc.) orchestration-style.

### Prerequisites & Limitations on macOS

Because Containerlab relies heavily on native Linux kernel networking features (such as veth pairs, Linux bridges, and netns manipulation), running it on a macOS host requires specific considerations:

1. **VM Root Privileges:** You must execute Containerlab commands inside the Podman Linux VM using root access, as rootless Podman cannot manipulate system network namespaces.
2. **Apple Hypervisor Setup:** Ensure your Podman machine was initialized using the standard native hypervisor framework (`podman machine init --provider applehv`).

---

### Step-by-Step Deployment

#### 1. SSH into the Podman Linux VM
Instead of running Containerlab directly from the macOS terminal prompt, you need to execute it within the underlying Linux VM environment where the container engines reside:

```bash
podman machine ssh
```

#### 2. Install Containerlab inside the Linux VM
Once inside the VM prompt, run the official automated script to fetch and install the latest Containerlab binary:

```bash
curl -sL https://containerlab.dev/setup | sudo bash
```

#### 3. Create a Basic Topology File
Create a workspace directory and define a basic topology (e.g., using standard FRR or native network routing images) inside a file named `lab.clab.yml`:

```bash
mkdir -p ~/my-first-lab && cd ~/my-first-lab
cat <<EOF > lab.clab.yml
name: mini-lab

topology:
  nodes:
    router1:
      kind: linux
      image: frrouting/frr:v8.4.0
    router2:
      kind: linux
      image: frrouting/frr:v8.4.0

  links:
    - endpoints: ["router1:eth1", "router2:eth1"]
EOF
```

#### 4. Deploy the Topology
Deploy the network topology using root privileges inside the VM. Containerlab will pull the images, construct the virtual interfaces, and configure the interconnects automatically:

```bash
sudo containerlab deploy --topo lab.clab.yml
```

#### 5. Verify and Inspect Running Nodes
Review the state of your running network nodes and their mapped IP addresses:

```bash
sudo containerlab inspect --topo lab.clab.yml
```

---

### Managing the Lab Topology

* **Access a Node Shell:** `sudo podman exec -it clab-mini-lab-router1 vtysh`
* **Destroy the Lab:** `sudo containerlab destroy --topo lab.clab.yml`
* **Exit the Podman VM:** `exit`
containerlab-podman-setup.md
Displaying containerlab-podman-setup.md.