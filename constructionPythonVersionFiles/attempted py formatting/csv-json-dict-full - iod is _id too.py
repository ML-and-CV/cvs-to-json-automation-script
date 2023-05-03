import csv
import json
import os
import secrets
import datetime

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
        # Parse the data from the text file
        # Parse the data from the text file
        data = {}
        with open(txt_file_path, "r") as txt_file:
            txt_reader = csv.DictReader(txt_file, delimiter='\t')
            count = 1
            for row in txt_reader:
                id = str(count)
                data[id] = {"_id": {"$oid": secrets.token_hex(12)}}
                for key, value in row.items():
                    if not value:
                        continue
                    if key in ["gene_id", "created_date"]:
                        if value in column_oid_map:
                            oid_value = column_oid_map[value]
                        else:
                            oid_value = secrets.token_hex(12)
                            column_oid_map[value] = oid_value
                        data[id][f"{key}_oid"] = {"$oid": oid_value}
                    elif key in timestamp_columns:
                        data[id][key] = {"$date": value}
                    elif key in int32_columns:
                        data[id][key] = {"$numberInt": value}
                    elif key in float_columns:
                        data[id][key] = {"$numberDouble": value}
                    else:
                        data[id][key] = value
                count += 1

        # Write the data to the JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
