def create_database(cursor):
    # cursor.execute(''' DROP DATABASE IF EXISTS lxc_containers''')
    cursor.execute(''' CREATE DATABASE lxc_containers ''')


def create_table(cursor):
    command = (
        """
        CREATE TABLE IF NOT EXISTS containers (
            name VARCHAR(200) PRIMARY KEY,
            cpu VARCHAR(200),
            memory_usage VARCHAR(200),
            created_at BIGINT,
            status VARCHAR(200)
        )
        """)
    cursor.execute(command)


def drop_table(cursor):
    drop = ("""
        DROP TABLE containers
        """)
    cursor.execute(drop)


def insert_container_data(cursor, name, created_at, status, cpu, memory_usage):
    data_insert = """ INSERT INTO containers(name, created_at, status, cpu, memory_usage) VALUES (%s,%s,%s,%s,%s)"""
    container_record = name, created_at, status, cpu, memory_usage
    cursor.execute(data_insert, container_record)
