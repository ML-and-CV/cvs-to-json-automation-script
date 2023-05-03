import csv
import json

csv_file_path = "C:/Users/mousu/Desktop/text_file.csv"
json_file_path = "C:/Users/mousu/Desktop/output.json"

data = {}

with open(csv_file_path) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    count = 1
    for rows in csv_reader:
        id = str(count)
        data[id] = {}
        data[id]["symbol"] = rows["symbol"]
        data[id]["name"] = rows["name"]
        data[id]["inheritance"] = rows["inheritance"]
        data[id]["id_omim"] = rows["id_omim"]
        data[id]["tissues"] = rows["tissues"]
        data[id]["features"] = rows["features"]
        data[id]["remarks"] = rows["remarks"]
        data[id]["created_by"] = rows["created_by"]
        data[id]["created_date"] = rows["created_date"]
        data[id]["edited_by"] = rows["edited_by"]
        data[id]["edited_date"] = rows["edited_date"]
        count += 1

with open(json_file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)
