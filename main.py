from fastapi import FastAPI
from pydantic import BaseModel
from release import Release

app = FastAPI()

# in memory database
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
        licenses = []
        for l in x['permissions']['licenses']:
            name = l['name']
            licenses.append(name)

        writer.writerow([x['organization'], x['laborHours'], x['status'], licenses, x['date']['created']])

class Release(BaseModel):
    organization: str
    release_count: int
    total_labor_hours: int
    all_in_production: bool
    licenses: list
    most_active_months: list[int] = []

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
