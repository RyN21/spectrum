from fastapi import FastAPI
from pydantic import BaseModel
import requests
import csv

app = FastAPI()

# IN MEMORY DATABASE
db = []

# CREATE RELEASE JSON FROM API REQUEST
r = requests.get("https://www.energy.gov/sites/prod/files/2020/12/f81/code-12-15-2020.json")
json = r.json()
releases = json["releases"]

# WRITE CSV FILE
with open('releases.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['organization', 'labor_hours', 'status', 'licenses', 'date_created'])

    for x in releases:
        licenses = x['permissions']['licenses'][0]['name'] if  x['permissions']['licenses'] != [] else None

        writer.writerow([x['organization'], x['laborHours'], x['status'], licenses, x['date']['created']])

with open('releases.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        db.append({'organization': row[0],
                   'total_labor_hours': row[1],
                   'all_in_production': bool(True if row[2] == "Production" else False),
                   'licenses': row[3],
                   'month_created': row[4]
                   })


class Release(BaseModel):
    organization: str
    labor_hours: int
    status: str
    licenses: str
    date_created: str



@app.get('/')
def index():
    return {'key' : 'value'}

@app.get('/releases')
def get_releases():
    return Release

@app.post('/organizations')


@app.get('releases/sort_by/organizations')
def get_releases_sorted_by_organizations():
    return db

@app.get('releases/sort_by/release_count')
def get_releases_sorted_by_count():
    return db

@app.get('releases/sort_by/total_labor_hours')
def get_releases_sorted_by_labor_hours():
    return db
