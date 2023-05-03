import csv
import json
import os
import secrets
from datetime import datetime

# Define a Node class for the linked list
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.oid_value = None
        self.next = None

# Set the path to the folder that contains the text files
txt_folder_path = "C:/Users/mousu/Desktop/rs-database-creation/textToCSV/"

# Define a dictionary to store the mapping of column values to OID values
column_oid_map = {}

# Define a list of columns that should be treated as timestamps
timestamp_columns = ["created_date"]

# Define a list of columns that should be treated as int32
int32_columns = ["total_reads", "total_writes"]

# Define a list of columns that should be treated as float
float_columns = ["float_column"]

# Loop through each file in the folder
for txt_file_name in os.listdir(txt_folder_path):
    if txt_file_name.endswith(".txt"):
        # Construct the path to the text file and the output JSON file
        txt_file_path = os.path.join(txt_folder_path, txt_file_name)
        json_file_path = os.path.join(txt_folder_path, txt_file_name.replace(".txt", ".json"))

        # Parse the data from the text file
        data = {}
        with open(txt_file_path, "r") as txt_file:
            txt_reader = csv.DictReader(txt_file, delimiter='\t')
            count = 1
            for row in txt_reader:
                id = str(count)
                data[id] = Node("id", id)
                current_node = data[id]
                for key, value in row.items():
                    if not value:
                        continue
                    if key in ["gene_id"]:
                        if value in column_oid_map:
                            oid_value = column_oid_map[value]
                        else:
                            oid_value = secrets.token_hex(12)
                            column_oid_map[value] = oid_value
                        current_node.next = Node(f"{key}_oid", {"$oid": oid_value})
                        current_node.next.oid_value = value
                        current_node = current_node.next
                    elif key in timestamp_columns:
                        try:
                            timestamp = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                            current_node.next = Node(key, {"$date": timestamp.isoformat()})
                            current_node.next.oid_value = value
                            current_node = current_node.next
                        except ValueError:
                            # Skip this row if the date cannot be parsed
                            break
                    elif key in int32_columns:
                        current_node.next = Node(key, int(value))
                        current_node.next.oid_value = value
                        current_node = current_node.next
                    elif key in float_columns:
                        current_node.next = Node(key, float(value))
                        current_node.next.oid_value = value
                        current_node = current_node.next
                    else:
                        current_node.next = Node(key, value)
                        current_node.next.oid_value = value
                        current_node = current_node.next
                count += 1

        # Write the data to the JSON file
        with open(json_file_path, "w") as json_file:
            json_data = {}
            for id, node in data.items():
                json_node = {}
                while node:
                    if node.key.endswith("_oid"):
                        json_node[node.key] = node.value
                        json_node[node.key[:-4]] = node.oid_value
                    else:
                        json_node[node.key] = node.value
                    node = node.next
                json_data[id] = json_node
            json.dump(json_data, json_file, indent=4)
