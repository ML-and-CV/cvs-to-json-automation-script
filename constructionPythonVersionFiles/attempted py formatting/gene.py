import json

text_file_path = "C:/Users/mousu/Desktop/rs-database-creation/textToCSV/gene.txt"
json_file_path = "C:/Users/mousu/Desktop/output.json"

data = {}

with open(text_file_path) as text_file:
    # Skip the header row
    next(text_file)
    
    count = 1
    for line in text_file:
        row = line.strip().split('\t')
        id = str(count)
        data[id] = {}
        data[id]["gene_id"] = row[0]
        data[id]["gene_type"] = row[1]
        data[id]["name"] = row[2]
        data[id]["ncbi_mRNA_id"] = row[3]
        data[id]["id_protein_ncbi"] = row[4]
        data[id]["position_c_mrna_start"] = row[5]
        data[id]["position_c_mrna_end"] = row[6]
        data[id]["position_c_cds_end"] = row[7]
        data[id]["position_g_mrna_start"] = row[8]
        data[id]["position_g_mrna_end"] = row[9]
        data[id]["created_by"] = row[10]
        data[id]["created_date"] = row[11]
        data[id]["edited_by"] = row[12]
        data[id]["edited_date"] = row[13]
        count += 1

with open(json_file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)
