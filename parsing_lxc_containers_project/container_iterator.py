from utilities import Utils


class ContainerIterator:

    def __init__(self, postgres_database_controller):
        self.postgres_database_controller = postgres_database_controller
        self.ip_address_inc_id = 0
        self.network_inc_id = 0

    def iterate_containers(self, parsed_data):
        for container in parsed_data:
            if container is None:
                continue
            created_at = Utils.retrieve_time(container["created_at"])
            state = container["state"]
            if state is None:
                self.postgres_database_controller.insert_container_data(container["name"], created_at,
                                                                        container["status"], None,
                                                                        None)
            else:
                self.postgres_database_controller.insert_container_data(container["name"], created_at,
                                                                        container["status"],
                                                                        Utils.read_dictionary(state["cpu"], "usage"),
                                                                        Utils.read_dictionary(state["memory"], "usage"))
                if state["network"] is None:
                    continue
                self.retrieve_network_id(state["network"], container["name"])

    def retrieve_network_id(self, network, container_name):
        for network_id in network:
            self.postgres_database_controller.insert_network_data(self.network_inc_id, network_id, container_name)
            network_element = network[network_id]
            if network_element is None:
                continue
            self.retrieve_addresses(network_element["addresses"])
            self.network_inc_id += 1

    def retrieve_addresses(self, network_addresses):
        for address in network_addresses:
            if address is None:
                continue
            self.postgres_database_controller.insert_ip_address_data(self.ip_address_inc_id, address["address"],
                                                                     self.network_inc_id)
            self.ip_address_inc_id += 1
