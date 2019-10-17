import argparse
import csv
import requests
from time import sleep

base_url = 'https://api.discogs.com//marketplace/price_suggestions/'

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'user-agent': "FooBarApp/3.0"}

field_names = {"Catalog#", "Artist", "Title", "Label", "Format", "Rating", "Released", "release_id",
                "CollectionFolder", "Date Added", "Collection Media Condition", "Collection Sleeve Condition",
                "Collection Notes", "Collection Location", "Expected Replacement Price"}

parser = argparse.ArgumentParser(description='Expecting collection filename and Discogs token')
parser.add_argument("--file", required=True, type=str, help="Filename of the inventory export from Discogs to parse")
parser.add_argument("--token", required=True, type=str, help="Your personal access token to Discogs")

args = parser.parse_args()
filename = args.file
token = args.token
headers.update({'Authorization': 'Discogs token=' + token})

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

        # Filter only on Flood Damage for this current use case
        # TODO: Run this to check arbitrage opportunities?
        if row["CollectionFolder"] != "Flood Damage":
            print("Not Flood Damage - skipping!")
            continue;

        # Check for set media and sleeve condition
        if (row["Collection Media Condition"] == "") or (row["Collection Sleeve Condition"] == ""):
            print(f'Invalid Catalog Item: {row["Artist"]} {row["Title"]} Media : {row["Collection Media Condition"]}. '
                  f'Sleeve : {row["Collection Sleeve Condition"]} ')
            continue

        # Retrieve suggested pricing
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

        result = r.json().get(row["Collection Media Condition"])
        if result is None:
            print(f'\t{row["Artist"]} {row["Title"]} Media : {row["Collection Media Condition"]}. Price : UNKNOWN')
            continue
        elif result.get('currency') == 'USD':
            price = result.get('value')
        else:
            print(f"Non USD Currency! {result}")

        row["Expected Replacement Price"] = round(price, 2)
        print(row)
        csv_writer.writerow(row)

        # Rewrite output
        line_count += 1
    print(f'Processed {line_count} lines.')
