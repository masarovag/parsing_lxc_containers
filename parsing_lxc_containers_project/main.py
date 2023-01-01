import json
import psycopg2 as pg2
import dateutil.parser

from manipulate_database import drop_all_tables, create_all_tables, insert_container_data, \
    insert_network_data, insert_ip_address_data, select_container_info

conn = pg2.connect(database='lxc_containers', user='postgres', password='kurzsql')
conn.autocommit = True
cur = conn.cursor()

# for testing
drop_all_tables(cur)
create_all_tables(cur)


def read_json_from_file():
    with open("sample-data.json") as x:
        data = json.load(x)
    return data


parsed_data = read_json_from_file()

ip_address_id = 0
network_id = 0

for container in parsed_data:

    cpu = None
    memory_usage = None
    created_at = None
    container_created_at = dateutil.parser.parse(container["created_at"])
    if container_created_at.year >= 1970:
        # if the year is less than 1970 it can not be timestamp
        created_at = container_created_at.timestamp()

    state = container["state"]

    if state is None:
        insert_container_data(cur, container["name"], created_at, container["status"], None, None)

    else:

        cpu = state["cpu"]["usage"]
        memory_usage = state["memory"]["usage"]
        insert_container_data(cur, container["name"], created_at, container["status"], cpu, memory_usage)
        for i in state["network"]:
            insert_network_data(cur, network_id, i, container["name"])
            network = state["network"][i]
            for address in network["addresses"]:
                insert_ip_address_data(cur, ip_address_id, address["address"], network_id)
                ip_address_id += 1
            network_id += 1

# selecting container info and it´s ip addresses
select_container_info(cur)

cur.close()
