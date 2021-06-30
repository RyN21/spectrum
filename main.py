from fastapi import FastAPI
from collections import Counter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
import requests
import csv
import pandas as pd


app = FastAPI()


# CREATE RELEASE JSON FROM API REQUEST
r = requests.get("https://www.energy.gov/sites/prod/files/2020/12/f81/code-12-15-2020.json")
json = r.json()
json_releases = json["releases"]

# WRITE CSV FILE
with open('releases.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['organization', 'labor_hours', 'status', 'licenses', 'date_created'])

    for x in json_releases:
        licenses = x['permissions']['licenses'][0]['name'] if  x['permissions']['licenses'] != [] else 'N/A'

        writer.writerow([x['organization'], x['laborHours'], x['status'], licenses, x['date']['created']])


# FILL DATABASE FROM CSV FILE
# IN MEMORY DATABASE
db = {}

with open('releases.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        if row[0] in db:

            db[row[0]]['release_count'] += 1
            db[row[0]]['total_labor_hours'] += float(row[1])
            db[row[0]]['status'].append(row[2])
            db[row[0]]['status'] = list(set(db[row[0]]['status']))
            db[row[0]]['licenses'].append(row[3])
            db[row[0]]['licenses'] = list(set(db[row[0]]['licenses']))
            db[row[0]]['most_active_months'].append(int(row[4].split("-")[1]))
            # db[row[0]]['most_active_months'] = list(set(db[row[0]]['most_active_months']))
            db[row[0]]['all_in_production'] = False if 'Development' in db[row[0]]['status'] else True
        else:
            status = row[2]
            db[row[0]] = {'organization': row[0],
                        'release_count': 1,
                        'total_labor_hours': float(row[1]),
                        'status': [row[2]],
                        'all_in_production': bool(True if status == 'Production' else False),
                        'licenses': [row[3]],
                        'most_active_months': [int(row[4].split("-")[1])]
                        }

releases = list(db.values())

# FUNCTION TO RETURN TOP 3 MOST ACTIVE MONTHS AND POP STATUS FROM DICTIONARY
def most_frequent(List):
    occurance_count = Counter(List)
    top3 = occurance_count.most_common(3)
    return [item[0] for item in top3]

for r in releases:
    r['most_active_months'] = most_frequent(r['most_active_months'])
    r.pop("status")


# API ROUTES
@app.get('/releases')
def get_releases():
    json_object = jsonable_encoder({'organization': releases})
    return json_object

@app.get('/releases/sort_by/organizations')
def get_releases_sorted_by_organizations():
    sorted_by_organization = sorted(releases, key = lambda item: item['organization'])
    json_object = jsonable_encoder({'organization': sorted_by_organization})
    return json_object

@app.get('/releases/sort_by/release_count/desc')
def get_releases_sorted_by_count():
    sorted_by_release_count = sorted(releases, key = lambda item: item['release_count'], reverse = True)
    json_object = jsonable_encoder({'organization': sorted_by_release_count})
    return json_object

@app.get('/releases/sort_by/release_count/asc')
def get_releases_sorted_by_count():
    sorted_by_release_count = sorted(releases, key = lambda item: item['release_count'])
    json_object = jsonable_encoder({'organization': sorted_by_release_count})
    return json_object

@app.get('/releases/sort_by/total_labor_hours/desc')
def get_releases_sorted_by_labor_hours():
    sorted_by_labor_hours = sorted(releases, key = lambda item: item['total_labor_hours'], reverse = True)
    json_object = jsonable_encoder({'organization': sorted_by_labor_hours})
    return json_object

@app.get('/releases/sort_by/total_labor_hours/asc')
def get_releases_sorted_by_labor_hours():
    sorted_by_labor_hours = sorted(releases, key = lambda item: item['total_labor_hours'])
    json_object = jsonable_encoder({'organization': sorted_by_labor_hours})
    return json_object

@app.get('/releases/csv', response_class=HTMLResponse)
async def get_release_csv():
    # WRITE CSV FILE
    with open('releases_new.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['organization', 'release_count', 'total_labor_hours', 'all_in_production', 'licenses', 'most_active_months'])

        for x in releases:
            writer.writerow([x['organization'], x['release_count'], x['total_labor_hours'], x['all_in_production'], x['licenses'], x['most_active_months']])

    with open('releases_new.csv', 'r') as file:
        read_releases = csv.reader(file, delimiter=' ')

        for row in read_releases:
            print(', '.join(row))

    a = pd.read_csv("releases_new.csv")
    a.to_html("Table.html")
    html_file = a.to_html()

    return html_file


# Add Readme
# Provide live URL of hosted API
# dockerize API
