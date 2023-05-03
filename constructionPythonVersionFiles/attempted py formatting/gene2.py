import csv
import json

txt_file_path = "C:/Users/mousu/Desktop/rs-database-creation/textToCSV/gene.txt"
json_file_path = "C:/Users/mousu/Desktop/output2.json"

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

with open(json_file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)
