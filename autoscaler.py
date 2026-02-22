import psutil
import time
import subprocess
import os

CPU_THRESHOLD = 50
MAX_VMS = 5
CHECK_INTERVAL = 5
BASE_IMAGE = "base-vm.qcow2"

vm_count = 0

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_running_vms():
    result = subprocess.run(["virsh", "list", "--name"], capture_output=True, text=True)
    vms = result.stdout.strip().split("\n")
    return [vm for vm in vms if vm.startswith("autoscale-vm")]

def create_vm():
    global vm_count
    vm_count += 1
    vm_name = f"autoscale-vm{vm_count}"
    disk_name = f"{vm_name}.qcow2"

    print(f"[+] Creating VM: {vm_name}")

    # Create linked clone
    subprocess.run([
        "qemu-img", "create",
        "-f", "qcow2",
        "-b", BASE_IMAGE,
        disk_name
    ])

    # Define and start VM
    subprocess.run([
        "virt-install",
        "--name", vm_name,
        "--ram", "1024",
        "--vcpus", "1",
        "--disk", f"path={disk_name},format=qcow2",
        "--network", "network=default",
        "--import",
        "--noautoconsole"
    ])

def main():
    print("🚀 Auto-Scaler Started...")

    while True:
        cpu = get_cpu_usage()
        running_vms = get_running_vms()

        print(f"CPU Usage: {cpu}% | Running Autoscale VMs: {len(running_vms)}")

        if cpu > CPU_THRESHOLD and len(running_vms) < MAX_VMS:
            create_vm()

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()