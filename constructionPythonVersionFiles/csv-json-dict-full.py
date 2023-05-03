'''
This is my own code:
I used the following libraries used to help me buiold the code:
https://docs.python.org/3/library/csv.html
https://docs.python.org/3/library/json.html
https://docs.python.org/3/library/os.html
https://docs.python.org/3/library/secrets.html
https://www.geeksforgeeks.org/linked-lists-python/
https://realpython.com/linked-lists-python/
https://www.askpython.com/python/list/convert-list-to-json
https://stackoverflow.com/questions/3171470/python-convert-linked-list-to-json
'''

import csv
import json
import os
import secrets
import datetime

# Set the path to the folder that contains the text files
txt_folder_path = "C:/Users/mousu/Desktop/rs-database-creation/textToCSV/"

# Define a dictionary to store the mapping of column values to OID values
column_oid_map = {}

# Define a list of columns that should be treated as oid
oid_columns = ["gene_id", "mRNA_id", "protien_id", "Individual_id", "COL1A2_disease_type_id", "individual_id",
               "disease_id", "screening_id", "variants_on_genome_id", "variants_on_transcripts_id",
               "transcript_id", "FBN1_disease_type_id", "edited_by", "user_id", "staff_id"]

# Define a list of columns that should be treated as timestamps
timestamp_columns = ["created_date", "edited_date","signup_date"]

# Define a list of columns that should be treated as int32
int32_columns = ["position_c_mrna_start", "position_c_mrna_end", "position_c_cds_end", "position_g_mrna_start",
                 "position_g_mrna_end", "Owned_by", "Individual_id", "mRNA_id", "protien_id", "gene_id",
                 "created_by", "edited_by","COL1A2_disease_type_id", "individual_id", "disease_id", "screening_id",
                 "variants_on_genome_id", "allele", "effect_id", "chromosome", "position_g_start",
                 "position_g_end", "VariantOnGenome_VIP", "position_c_start", "position_c_start_intron", "position_c_end",
                 "position_c_end_intron", "user_id", "staff_id"]

# Define a list of columns that should be treated as float
float_columns = ["average_frequency"]

# Define a list of columns that should be treated as boolean
bool_columns = ["approved_for_db_edit", "approved_for_db_edit", "newsletter", "admin"]

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
                data[id] = {"_id": count}
                for key, value in row.items():
                    if not value:
                        continue
                    if key in oid_columns:
                        if value in column_oid_map:
                            oid_value = column_oid_map[value]
                        else:
                            oid_value = secrets.token_hex(12)
                            column_oid_map[value] = oid_value
                        data[id][f"{key}_oid"] = {"$oid": oid_value}
                        data[id][key] = value
                    elif key in timestamp_columns:
                        try:
                            timestamp = datetime.datetime.strptime(value, "%d-%m-%Y %H:%M")
                            data[id][key] = {"$date": timestamp.isoformat()}
                        except ValueError:
                            # Skip the row if the timestamp is invalid
                            #print("Timestap ignored")
                            continue
                    elif key in int32_columns:
                        data[id][key] = {"$numberInt": value}
                    elif key in float_columns:
                        data[id][key] = {"$numberDouble": value}
                    elif key in bool_columns:
                        if value.lower() == "true":
                            data[id][key] = True
                        elif value.lower() == "false":
                            data[id][key] = False
                    else:
                        data[id][key] = value
                count += 1

        # Write the data to the JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
