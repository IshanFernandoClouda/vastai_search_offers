import os

GPU_TYPE = "RTX_3090"
GPU_COUNT = 1

DISK = 16
CPU_RAM = 8

INET_UP = 50
INET_DOWN = 100
INET_UP_PRICE = 1
INET_DOWN_PRICE = 1


command = f"""vastai search offers "disk_space >= {DISK} num_gpus = {GPU_COUNT} cpu_ram >= {CPU_RAM} inet_up >= {INET_UP} inet_down >= {INET_DOWN} inet_up_cost < {INET_UP_PRICE} inet_down_cost < {INET_DOWN_PRICE} gpu_name = {GPU_TYPE}" -o "dph" --on-demand """

output = os.popen(command).read()
print(output)
lines = output.strip().replace("NV Driver", "NV_Driver").split('\n')

if len(lines) >= 2:
    headers = lines[0].split()
    first_instance = lines[1].split()

    instance_info = {}
    for i, header in enumerate(headers):
        instance_info[header] = first_instance[i]

    print("Instance Information:")
    for key, value in instance_info.items():
        print(f"{key}: {value}")

    # os.system(f"vastai create instance {instance_info['ID']} --image pytorch/pytorch:latest --disk {DISK}")
else:
    print("No instances found.")