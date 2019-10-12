import csv
import jq
import requests

url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere'
with open('neilepalmer-collection-20191011-1851.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:

        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1

        if (row["CollectionFolder"] == "Flood Damage"):
            if (row["Collection Media Condition"] == "") or (row["Collection Sleeve Condition"] == ""):
                print(f'\t{row["Artist"]} {row["Title"]} Media : {row["Collection Media Condition"]}. Sleeve : {row["Collection Sleeve Condition"]} ')

            # print(f'\t{row["Artist"]} {row["Title"]} Media : {row["Collection Media Condition"]}. Sleeve : {row["Collection Sleeve Condition"]} ')

        # payload = open("request.json")
        # headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        # r = requests.post(url, data=payload, headers=headers)

        line_count += 1
    print(f'Processed {line_count} lines.')
