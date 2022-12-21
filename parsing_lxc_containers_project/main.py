import json

def read_json_from_file():
    with open("sample-data.json") as x:
        data = json.load(x)
    return data


parsed_data = read_json_from_file()
for container in parsed_data:
    print("-------------------------")
    print(container["name"])
    print(container["created_at"])
    print(container["status"])
    if container["state"] is not None:
        print(container["state"]["cpu"])
        print(container["state"]["memory"]["usage"])
        for i in container["state"]["network"]:
            network = container["state"]["network"][i]
            for address in network["addresses"]:
                print(address["address"])


