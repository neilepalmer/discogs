import csv
import requests

url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere'
with open('neilepalmer-collection-20190930-1715.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:

        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1

        print(f'\t{row["Artist"]} {row["Title"]} Media : {row["Collection Media Condition"]}. Media : {row["Collection Sleeve Condition"]} ')

        # payload = open("request.json")
        # headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        # r = requests.post(url, data=payload, headers=headers)

        line_count += 1
    print(f'Processed {line_count} lines.')
