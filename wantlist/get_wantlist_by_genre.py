import argparse
import csv
import requests
from time import sleep

# /releases/{release_id}
base_url = 'https://api.discogs.com/releases/'

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'user-agent': "FooBarApp/3.0"}

# Dropped release_id, not sure it's useful
field_names = {"Catalog#", "Artist", "Title", "Label", "Format", "Rating", "Released", "Notes", "genres", "styles"}

parser = argparse.ArgumentParser(description='Expecting collection filename and Discogs token')
parser.add_argument("--file", required=True, type=str, help="Filename of the inventory export from Discogs to parse")
parser.add_argument("--token", required=True, type=str, help="Your personal access token to Discogs")

args = parser.parse_args()
filename = args.file
token = args.token
headers.update({'Authorization': 'Discogs token=' + token})
writerow = {}

with open(filename) as csv_file, open('results.csv', 'w') as results_file:

    # Read collection file
    csv_reader = csv.DictReader(csv_file)
    csv_writer = csv.DictWriter(results_file, field_names)
    csv_writer.writeheader()

    line_count = 0
    for row in csv_reader:

        # Reset current price
        price = 0

        # Skips headers
        if line_count == 0:
            # print(f'Column names are {", ".join(row)}')
            line_count += 1

        # Retrieve release
        url = base_url + row["release_id"]
        r = requests.get(url, headers=headers)

        # Check rate limiting
        rate_limit = r.headers['X-Discogs-Ratelimit']
        rate_limit_used = r.headers['X-Discogs-Ratelimit-Used']
        rate_remaining = r.headers['X-Discogs-Ratelimit-Remaining']
        print(f'Limit: {rate_limit} Used: {rate_limit_used} Remaining: {rate_remaining}')

        if rate_remaining is not None and int(rate_remaining) < 10:
            print('Sleep sleep sleeping')
            sleep(10)

        # print("Genres: ")
        # print(r.json().get("genres"))
        # print("Styles: ")
        # print(r.json().get("styles"))
 
        writerow["Catalog#"] = row["Catalog#"]
        writerow["Artist"] = row["Artist"]
        writerow["Title"] = row["Title"]
        writerow["Label"] = row["Label"]
        writerow["Format"] = row["Format"]
        writerow["Rating"] = row["Rating"]
        writerow["Released"] = row["Released"]
        writerow["Notes"] = row["Notes"] 
        writerow["genres"] = r.json().get("genres")
        writerow["styles"] = r.json().get("styles")
        # print(writerow)
        csv_writer.writerow(writerow)

        # Rewrite output
        line_count += 1

    print(f'Processed {line_count} lines.')
