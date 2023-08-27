import os
import json

command = f"""vastai show user --raw"""
output = os.popen(command).read()
output = json.loads(output[output.index("{"):])

print()
print(f"email: {output['email']}")
print(f"credit: {output['credit']:3.4f}$")
print()