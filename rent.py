import os
import json

# Modify Start ---------------------------------------------------
# GPU options
GPU_TYPE = "RTX_3090"
GPU_COUNT = 1

# CPU options
DISK = 30
CPU_RAM = 20

# Network options
INET_UP = 10
INET_DOWN = 300
# price per tb transferred. 
# Change this to zero if you are going to be tranferring lots of files. 
# Usually the increase in per hour cost outweighs the cost of transferring files
# if the cost of tranferring is very high (or you are transferring lots of files - about more than 30gb)

PRICE = 3
# Modify END -----------------------------------------------------

# Do not modify below
INET_UP_PRICE = PRICE/1024
INET_DOWN_PRICE = PRICE/1024


command = f"""vastai search offers --storage {DISK} "disk_space >= {DISK} num_gpus = {GPU_COUNT} cpu_ram >= {CPU_RAM} inet_up >= {INET_UP} inet_down >= {INET_DOWN} inet_up_cost <= {INET_UP_PRICE} inet_down_cost <= {INET_DOWN_PRICE} gpu_name = {GPU_TYPE} rentable=true" -o "dph" --on-demand --raw """

output = json.loads(os.popen(command).read())

count = 0
for each in output:
    effectiveFactor = each["cpu_cores_effective"] / each["cpu_cores"]
    if effectiveFactor * each["cpu_ram"] >= CPU_RAM * 1024:
        each["cpu_ram"] = effectiveFactor * each["cpu_ram"]
    else:
        output.pop(count)
    count += 1

if len(output) > 0:
    first_instance = output[0]
    print(json.dumps(first_instance, indent=4))

    print(f"gpu_name: {first_instance['gpu_name']}")
    print(f"gpu_ram: {first_instance['gpu_ram']/1024} GB")
    print(f"num_gpus: {first_instance['num_gpus']}")
    print()
    print(f"cpu_ram: {first_instance['cpu_ram']/1024:3.2f} GB")
    print(f"disk_space: {first_instance['disk_space']:3.2f} GB available - {DISK}GB will be allocated for you")
    print()
    print(f"inet_up: {first_instance['inet_up']:3.2f}mbps")
    print(f"inet_up_cost: {first_instance['inet_up_cost']*1024:3.4f}$ per TB")
    print()
    print(f"inet_down: {first_instance['inet_down']:3.2f}mbps")
    print(f"inet_down_cost: {first_instance['inet_down_cost']*1024:3.4f}$ per TB")
    print()
    print(f"dlperf: {first_instance['dlperf']}")
    print()
    print(f"$/hr: {first_instance['dph_total']}$")


    if input("Rent the instance? [y,N] :").lower() == "y":
        print("\nRenting instance")
        os.system(f"vastai create instance {first_instance['id']} --image pytorch/pytorch:latest --disk {DISK}  --jupyter")
    else:
        print("Did not rent instance")

else:
    print("No instances found.")



