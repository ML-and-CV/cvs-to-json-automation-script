import csv
import json
import os

# Set the path to the folder that contains the text files
txt_folder_path = "C:/Users/mousu/Desktop/rs-database-creation/textToCSV/"

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
                data[id] = {}
                for key, value in row.items():
                    if not value:
                        continue
                    data[id][key] = value
                count += 1

        # Write the data to the JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
