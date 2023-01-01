def create_database(cursor):
    # cursor.execute(''' DROP DATABASE IF EXISTS lxc_containers''')
    cursor.execute(''' CREATE DATABASE lxc_containers ''')


def create_all_tables(cursor):
    create_table_containers(cursor)
    create_table_network(cursor)
    create_table_ip_addresses(cursor)


def drop_all_tables(cursor):
    # easier than to use DROP CASCADE
    drop = ("""
        DROP TABLE ip_addresses;
        DROP TABLE network;
        DROP TABLE containers;
        """)
    cursor.execute(drop)


def create_table_containers(cursor):
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
    cursor.execute(command)


def create_table_network(cursor):
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
    cursor.execute(command)


def create_table_ip_addresses(cursor):
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
    cursor.execute(command)


def insert_container_data(cursor, container_name, created_at, status, cpu, memory_usage):
    data_container_insert = """INSERT INTO containers(container_name, created_at, status, cpu, memory_usage) VALUES (
    %s,%s,%s,%s,%s) """
    container_record = container_name, created_at, status, cpu, memory_usage
    cursor.execute(data_container_insert, container_record)


def insert_network_data(cursor, network_id, network_name, container_name):
    data_network_insert = """ INSERT INTO network(network_id, network_name, container_name) VALUES (%s,%s,%s)"""
    network_record = network_id, network_name, container_name
    cursor.execute(data_network_insert, network_record)


def insert_ip_address_data(cursor, ip_address_id, ip_address, network_id):
    data_network_insert = """ INSERT INTO ip_addresses(ip_address_id,ip_address, network_id) VALUES (%s,%s,%s)"""
    network_record = ip_address_id, ip_address, network_id
    cursor.execute(data_network_insert, network_record)
