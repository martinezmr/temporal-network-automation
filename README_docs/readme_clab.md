## Deploying ContainerLab via Podman on macOS

This guide provides step-by-step instructions for setting up ContainerLab in a Podman-based environment on macOS. ContainerLab lets you deploy and manage containerized network topologies such as Arista cEOS, Nokia SR-OS, Cisco XRD, and FRR.

### Objective

By the end of this process, you should be able to:
- install the required tools on macOS and the Ubuntu VM
- import the Arista cEOS image
- deploy a ContainerLab topology
- access the lab devices from your Mac through a jump host

### Prerequisites and limitations on macOS

macOS does not include all of the Linux components required to run ContainerLab natively. The recommended approach is to use OrbStack to run an Ubuntu Linux virtual machine.

#### 1. Install OrbStack on your Mac

Run the following command:

```bash
brew install orbstack
```

After installation:
- open OrbStack
- create an Ubuntu Linux virtual machine
- open the VM and set a password for your user account

```bash
orb sudo passwd $USER
```

### 2. Install OpenSSH in the Ubuntu VM

Run the following commands inside the Ubuntu VM:

```bash
sudo apt update
sudo apt install openssh-server -y
```

Start the SSH service:

```bash
sudo systemctl enable --now ssh
```

### 3. Install ContainerLab and Docker

Install ContainerLab with the official setup script:

```bash
curl -sL https://containerlab.dev/setup | sudo -E bash -s "all"
```

Log out and log back in, or restart your shell session. Then verify that Docker is working:

```bash
sudo docker run hello-world
```

If the command fails, install Docker manually:

```bash
sudo apt install ca-certificates curl gnupg -y

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

sudo docker run hello-world
sudo usermod -aG docker $USER
```

After the Docker installation completes, log out and back in again. Verify once more:

```bash
sudo docker run hello-world
```

### 4. Prepare the cEOS image

You need to upload the cEOS image file named cEOS64-lab-4.32.0F.tar.xz to your Ubuntu VM.

1. Download the image from the Arista software download portal:
   https://www.arista.com/en/support/software-download
2. Create a lab directory on the Ubuntu VM.
3. Copy the repository's clab folder to the VM if you have not already done so.
4. Copy the image file from your Mac to the Ubuntu VM.

Example import command:

```bash
docker import cEOS64-lab-4.32.0F.tar.xz ceos:4.32.0F
```

### 5. Deploy the ContainerLab topology

From the Ubuntu VM, run:

```bash
sudo containerlab deploy --topo ceos-lab.clab.yml
```

You should see output similar to the following:

```bash
manny@containerlab:~/clab$ sudo containerlab deploy --topo ceos-lab.clab.yml
18:10:13 INFO Containerlab started version=0.77.0
18:10:13 INFO Parsing & checking topology file=ceos-lab.clab.yml
18:10:13 INFO Creating lab directory path=/home/manny/clab/clab-ceos-lab
18:10:13 INFO Creating container name=bos-acc-01
18:10:13 INFO Creating container name=bos-rtr-01
18:10:13 INFO Creating container name=nyc-acc-01
18:10:13 INFO Creating container name=nyc-rtr-01
18:10:13 INFO Created link: bos-acc-01:eth1 ▪┄┄▪ bos-rtr-01:eth1
18:10:13 INFO Running postdeploy actions for Arista cEOS 'bos-acc-01' node
18:10:13 INFO Running postdeploy actions for Arista cEOS 'bos-rtr-01' node
18:10:13 INFO Created link: bos-acc-01:eth2 ▪┄┄▪ nyc-rtr-01:eth2
18:10:13 INFO Running postdeploy actions for Arista cEOS 'nyc-rtr-01' node
18:10:13 INFO Created link: bos-rtr-01:eth2 ▪┄┄▪ nyc-acc-01:eth2
18:10:13 INFO Created link: nyc-acc-01:eth1 ▪┄┄▪ nyc-rtr-01:eth1
18:10:13 INFO Running postdeploy actions for Arista cEOS 'nyc-acc-01' node
18:11:04 INFO Adding host entries path=/etc/hosts
18:11:05 INFO Adding SSH config for nodes path=/etc/ssh/ssh_config.d/clab-ceos-lab.conf
╭────────────┬──────────────┬─────────┬────────────────╮
│    Name    │  Kind/Image  │  State  │ IPv4/6 Address │
├────────────┼──────────────┼─────────┼────────────────┤
│ bos-acc-01 │ ceos         │ running │ 172.17.0.2     │
│            │ ceos:4.32.0F │         │ N/A            │
├────────────┼──────────────┼─────────┼────────────────┤
│ bos-rtr-01 │ ceos         │ running │ 172.17.0.3     │
│            │ ceos:4.32.0F │         │ N/A            │
├────────────┼──────────────┼─────────┼────────────────┤
│ nyc-acc-01 │ ceos         │ running │ 172.17.0.5     │
│            │ ceos:4.32.0F │         │ N/A            │
├────────────┼──────────────┼─────────┼────────────────┤
│ nyc-rtr-01 │ ceos         │ running │ 172.17.0.4     │
│            │ ceos:4.32.0F │         │ N/A            │
╰────────────┴──────────────┴─────────┴────────────────╯
manny@containerlab:
```

### 6. Access the devices from your Mac

You can reach the devices from the Ubuntu VM using SSH with the username admin and password admin. However, you cannot directly ping or reach them from your Mac. To solve this, use the Ubuntu VM as a jump host.

Update your SSH config on your Mac with the following entries:

```bash
Host containerlab
    Hostname 192.168.139.37
    User manny

Host 172.17.0.*
    ProxyJump containerlab
    User admin
```

Replace the IP address in the Hostname line with the actual IP address of your Ubuntu VM.

### 7. Configure SSH keys for passwordless access

To avoid being prompted to log in to the Ubuntu VM every time, generate SSH keys on your Mac:

```bash
ssh-keygen -t ed25519
```

Then copy the public key to the Ubuntu VM:

```bash
ssh-copy-id manny@192.168.139.37
```

After this, you should be able to connect directly to the routers and switches through your Ubuntu VM as a proxy jump host.

### References

- https://containerlab.dev/install/
