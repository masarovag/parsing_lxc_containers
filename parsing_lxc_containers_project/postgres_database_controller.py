from utilities import Utils


class PostgresDatabaseController:

    def __init__(self, cursor):
        self.cursor = cursor

    def create_database(self):
        self.cursor.execute(''' CREATE DATABASE lxc_containers ''')

    def create_all_tables(self):
        self.create_table_containers()
        self.create_table_network()
        self.create_table_ip_addresses()

    def drop_all_tables(self):
        # easier than to use DROP CASCADE
        drop = ("""
            DROP TABLE ip_addresses;
            DROP TABLE network;
            DROP TABLE containers;
            """)
        self.cursor.execute(drop)

    def create_table_containers(self):
        command = (
            """
            CREATE TABLE IF NOT EXISTS containers (
                container_name VARCHAR(200) PRIMARY KEY,
                cpu VARCHAR(200),
                memory_usage VARCHAR(200),
                created_at BIGINT,
                status VARCHAR(200)
            )
            """)
        self.cursor.execute(command)

    def create_table_network(self):
        command = (
            """
            CREATE TABLE IF NOT EXISTS network (
                network_id SMALLINT PRIMARY KEY,
                network_name VARCHAR(200), 
                container_name VARCHAR(200),
                CONSTRAINT fk_container
                  FOREIGN KEY(container_name) 
                    REFERENCES containers(container_name)
            )
            """)
        self.cursor.execute(command)

    def create_table_ip_addresses(self):
        command = (
            """
            CREATE TABLE IF NOT EXISTS ip_addresses (
                ip_address_id INT PRIMARY KEY,
                ip_address VARCHAR(200), 
                network_id SMALLINT,
                CONSTRAINT fk_networks
                  FOREIGN KEY(network_id) 
                    REFERENCES network(network_id)
            )
            """)
        self.cursor.execute(command)

    def insert_container_data(self, container_name, created_at, status, cpu, memory_usage):
        data_container_insert = """INSERT INTO containers(container_name, created_at, status, cpu, memory_usage) VALUES (
        %s,%s,%s,%s,%s) """
        container_record = container_name, created_at, status, cpu, memory_usage
        self.cursor.execute(data_container_insert, container_record)

    def insert_network_data(self, network_id, network_name, container_name):
        data_network_insert = """ INSERT INTO network(network_id, network_name, container_name) VALUES (%s,%s,%s)"""
        network_record = network_id, network_name, container_name
        self.cursor.execute(data_network_insert, network_record)

    def insert_ip_address_data(self, ip_address_id, ip_address, network_id):
        data_network_insert = """ INSERT INTO ip_addresses(ip_address_id,ip_address, network_id) VALUES (%s,%s,%s)"""
        network_record = ip_address_id, ip_address, network_id
        self.cursor.execute(data_network_insert, network_record)

    # possible improvement: make blank repeating container info
    def select_container_info(self):
        command = (
            """
            SELECT c.container_name, c.cpu, c.memory_usage, c.created_at, c.status, i.ip_address
            FROM containers AS c
            INNER JOIN network AS n
            ON c.container_name = n.container_name
            INNER JOIN ip_addresses AS i
            ON n.network_id = i.network_id
            """)
        self.cursor.execute(command)

    def iterate_containers(self, parsed_data, database_controller):
        ip_address_inc_id = 0
        network_inc_id = 0
        for container in parsed_data:
            created_at = Utils.retrieve_time(container["created_at"])
            state = container["state"]
            if state is None:
                database_controller.insert_container_data(container["name"], created_at, container["status"], None,
                                                          None)
            else:
                database_controller.insert_container_data(container["name"], created_at, container["status"],
                                                          state["cpu"]["usage"], state["memory"]["usage"])
                for network_id in state["network"]:
                    database_controller.insert_network_data(network_inc_id, network_id, container["name"])
                    network = state["network"][network_id]
                    for address in network["addresses"]:
                        database_controller.insert_ip_address_data(ip_address_inc_id, address["address"],
                                                                   network_inc_id)
                        ip_address_inc_id += 1
                    network_inc_id += 1
