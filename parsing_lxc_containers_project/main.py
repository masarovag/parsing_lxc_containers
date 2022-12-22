import json
import psycopg2 as pg2
import dateutil.parser

from manipulate_database import drop_table, create_table, insert_container_data

conn = pg2.connect(database='lxc_containers', user='postgres', password='kurzsql')
conn.autocommit = True
cur = conn.cursor()

#for testing
drop_table(cur)
create_table(cur)


def read_json_from_file():
    with open("sample-data.json") as x:
        data = json.load(x)
    return data


parsed_data = read_json_from_file()
#todo create as a function
for container in parsed_data:
    cpu = None
    memory_usage = None
    created_at = None
    container_created_at = dateutil.parser.parse(container["created_at"])
    if container_created_at.year >= 1970:
        # if the year is less than 1970 it can not be timestamp
        created_at = container_created_at.timestamp()

    if container["state"] is not None:
        cpu = container["state"]["cpu"]["usage"]
        memory_usage = container["state"]["memory"]["usage"]
        for i in container["state"]["network"]:
            network = container["state"]["network"][i]
            for address in network["addresses"]:
                print(address["address"])
                #todo add addresses to the postgre

    insert_container_data(cur, container["name"], created_at, container["status"], cpu, memory_usage)

cur.close()
