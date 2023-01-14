import psycopg2 as pg2

from postgres_database_controller import PostgresDatabaseController
from utilities import Utils


def main():
    conn = pg2.connect(database='lxc_containers', user='postgres', password='kurzsql')
    conn.autocommit = True  # use transaction
    cursor = conn.cursor()
    database_controller = PostgresDatabaseController(cursor)

    # for testing
    database_controller.drop_all_tables()
    database_controller.create_all_tables()

    parsed_data = Utils.read_json_file()
    if parsed_data is not None:

        database_controller.iterate_containers(parsed_data)

        # selecting container info and it´s ip addresses
        database_controller.select_container_info()

    cursor.close()


if __name__ == "__main__":
    main()
