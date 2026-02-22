# ☁️ Private Cloud Auto-Scaling Infrastructure (AWS EC2 Simulation)

A production-style **Auto-Scaling Infrastructure System** built using:

* 🐍 Python (Monitoring + Automation)
* 🖥 KVM Hypervisor
* 🔌 Libvirt
* 💽 QCOW2 Linked Clones
* 🌐 Virtual Networking (virbr0)

This project simulates **AWS EC2 Auto Scaling Groups** in a private cloud environment.

Based on system CPU load, new Virtual Machines are automatically provisioned from a Golden Image.

---

## 📌 Use Cases

* 🏥 Hospital On-Premise Cloud
* 🧠 Distributed Medical AI
* 🌐 IoMT Edge Cloud
* 🤖 Federated Learning Clients
* 🛡 Intrusion Detection Training Nodes

---

## 🏗 Architecture

```
CPU Monitor (psutil)
        │
        ▼
Python Autoscaler
        │
 ┌──────┼────────┐
 ▼      ▼        ▼
autoscale1 autoscale2 autoscaleN
        │
        ▼
Linked Clone from base-vm.qcow2
        │
        ▼
Libvirt → KVM → Host OS
```

---

## ⚙️ Installation Guide

### 1️⃣ Install Required Packages

```bash
sudo apt update
sudo apt install qemu-kvm libvirt-daemon-system virtinst bridge-utils python3-psutil
```

Enable services:

```bash
sudo systemctl enable libvirtd
sudo systemctl start libvirtd
```

---

### 2️⃣ Create Golden Base Image

```bash
qemu-img create -f qcow2 base-vm.qcow2 10G
```

---

### 3️⃣ Create Base VM

```bash
virt-install \
--name base-vm \
--ram 2048 \
--vcpus 2 \
--disk path=base-vm.qcow2,format=qcow2 \
--os-variant ubuntu22.04 \
--network network=default \
--graphics none \
--console pty,target_type=serial \
--cdrom ubuntu-22.04.iso
```

Inside VM install:

```bash
sudo apt install openssh-server stress
sudo shutdown now
```

---

## 🚀 Running AutoScaler

```bash
python3 autoscaler.py
```

### Scaling Condition

* CPU Usage > 50%
* Maximum 5 VMs allowed

---

## 🔍 Monitor Running VMs

```bash
virsh list --all
```

---

## ❌ Destroy Instance

```bash
virsh destroy autoscale-vm1
virsh undefine autoscale-vm1
rm autoscale-vm1.qcow2
```

---

## 🛑 Stop Entire Environment

```bash
sudo systemctl stop libvirtd.service \
libvirtd.socket \
libvirtd-ro.socket \
libvirtd-admin.socket
```

---

## 🔁 Restart Later

```bash
sudo systemctl start libvirtd
sudo virsh net-start default
```

---

## 🧠 How It Works

1. Python continuously monitors CPU usage
2. When CPU > 50%
3. System creates linked QCOW2 clone
4. VM is automatically provisioned using virt-install
5. Instances scale dynamically

---

## 📊 Features

* AWS EC2-like Auto Scaling
* Linked Clone Optimization
* CPU Threshold-based Scaling
* Private Cloud Deployment
* Real IaaS Simulation

---

## 🔒 Production Ready Enhancements (Optional)

* Add Scale-Down Logic
* Add Prometheus Monitoring
* Add Web Dashboard
* Add Multi-node cluster support
* Add Kubernetes orchestration

---

## 👨‍💻 Author

Prateek Choudhary

---
