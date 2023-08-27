import os
import json

command = f"""vastai show instances --raw"""
output = os.popen(command).read()
output = json.loads(output)

if len(output) == 0:
    print("No current running instances")
    quit()

count = 1
for each in output:
    print(f"{count}) GPU: {each['gpu_name']}, num_gpus: {each['num_gpus']}, cpu_name: {each['cpu_name']}, duration: {each['duration']/60:3.2f}mins")
    count += 1

index = input("Which instane number to delete ? (Example: '1')\n")
if len(index) == 0:
    print("No instance specified. Not deleting any instances")
else:
    print(f"Deleting instance number {index}")
    os.system(f"vastai destroy instance {output[int(index)-1]['id']}")
