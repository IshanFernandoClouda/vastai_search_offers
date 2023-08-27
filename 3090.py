import os
import json

GPU_TYPE = "RTX_3090"
GPU_COUNT = 1

DISK = 16
CPU_RAM = 8

INET_UP = 50
INET_DOWN = 100
INET_UP_PRICE = 2/1024
INET_DOWN_PRICE = 2/1024


command = f"""vastai search offers "disk_space >= {DISK} num_gpus = {GPU_COUNT} cpu_ram >= {CPU_RAM} inet_up >= {INET_UP} inet_down >= {INET_DOWN} inet_up_cost < {INET_UP_PRICE} inet_down_cost < {INET_DOWN_PRICE} gpu_name = {GPU_TYPE}" -o "dph" --on-demand --raw"""

output = json.loads(os.popen(command).read())
if len(output) > 0:
    first_instance = output[0]

    print(f"gpu_name: {first_instance['gpu_name']}")
    print(f"gpu_ram: {first_instance['gpu_ram']/1024} gb")
    print(f"num_gpus: {first_instance['num_gpus']}")
    print()
    print(f"cpu_ram: {first_instance['cpu_ram']/1024} gb")
    print(f"disk_space: {first_instance['disk_space']} gb")
    print()
    print(f"inet_up: {first_instance['inet_up']}")
    print(f"inet_up_billed: {first_instance['inet_up_billed']}")
    print()
    print(f"inet_down: {first_instance['inet_down']}")
    print(f"inet_down_billed: {first_instance['inet_down_billed']}")
    print()
    print(f"dlperf: {first_instance['dlperf']}")
    print()
    print(f"dph_total: {first_instance['dph_total']}")




    if input("Rent the instance? [y,N] :").lower() == "y":
        print("\nRenting instance")
        os.system(f"vastai create instance {first_instance['id']} --image pytorch/pytorch:latest --disk {DISK}")
    else:
        print("Did not rent instance")

else:
    print("No instances found.")



