import json

import dateutil.parser


class Utils:
    @staticmethod
    def read_dictionary(dictionary, key):
        if dictionary is None:
            return None
        return dictionary[key]

    @staticmethod
    def read_json_file():
        with open("sample-data.json") as x:
            data = json.load(x)
        return data

    @staticmethod
    def retrieve_time(date_string):
        date = dateutil.parser.parse(date_string)
        if date.year >= 1970:
            # if the year is less than 1970 it can not be timestamped
            created_at_ms = date.timestamp()
            return created_at_ms
        return None
