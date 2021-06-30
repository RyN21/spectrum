from fastapi import FastAPI
import requests
import csv


app = FastAPI()

# IN MEMORY DATABASE
db = {}

# CREATE RELEASE JSON FROM API REQUEST
r = requests.get("https://www.energy.gov/sites/prod/files/2020/12/f81/code-12-15-2020.json")
json = r.json()
releases = json["releases"]

# WRITE CSV FILE
with open('releases.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['organization', 'labor_hours', 'status', 'licenses', 'date_created'])

    for x in releases:
        licenses = x['permissions']['licenses'][0]['name'] if  x['permissions']['licenses'] != [] else 'N/A'

        writer.writerow([x['organization'], x['laborHours'], x['status'], licenses, x['date']['created']])

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
            db[row[0]]['most_active_months'] = list(set(db[row[0]]['most_active_months']))
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
print(db)



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
