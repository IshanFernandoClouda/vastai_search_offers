import os
import json

command = f"""vastai show instances --raw"""
output = os.popen(command).read()
output = json.loads(output)

if len(output) == 0:
    print("No current running instances")
    quit()

for each in output:
    url = f"https://jupyter.vast.ai/jm/{each['ssh_idx']}/{each['ssh_port']}/?token={each['jupyter_token']}"
    print("ID: " , each['id'] ,"GPU: " , each['gpu_name'] ," - ", end="")
    print(url)