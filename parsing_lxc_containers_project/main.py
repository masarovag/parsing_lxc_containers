import psycopg2 as pg2
import logging

from container_iterator import ContainerIterator
from postgres_database_controller import PostgresDatabaseController
from utilities import Utils


def main():
    try:
        conn = pg2.connect(database='lxc_containers', user='postgres', password='kurzsql')
    except:
        logging.error("Database not connected")
        return

    cursor = conn.cursor()
    database_controller = PostgresDatabaseController(cursor)
    container_iterator = ContainerIterator(database_controller)

    # for testing
    database_controller.drop_all_tables()
    database_controller.create_all_tables()

    try:
        parsed_data = Utils.read_json_file()
    except:
        logging.error("Error reading json file")
        cursor.close()
        return
    if parsed_data is not None:
        try:
            container_iterator.iterate_containers(parsed_data)
        # selecting container info and it´s ip addresses
        except:
            logging.error("Error iterating containers")
            cursor.close()
            return

        try:
            database_controller.select_container_info()
        except:
            logging.error("Error selecting info")
            cursor.close()
            return
    conn.commit()
    cursor.close()


if __name__ == "__main__":
    main()
