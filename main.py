from fastapi import FastAPI
import requests
import csv


app = FastAPI()


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

releases = list(db.values())
# print(sorted_by_organization)



@app.get('/releases')
def get_releases():
    return releases

@app.get('/releases/sort_by/organizations')
def get_releases_sorted_by_organizations():
    sorted_by_organization = sorted(releases, key = lambda item: item['organization'])
    return sorted_by_organization

@app.get('/releases/sort_by/release_count/desc')
def get_releases_sorted_by_count():
    sorted_by_release_count = sorted(releases, key = lambda item: item['release_count'], reverse = True)
    return sorted_by_release_count

@app.get('/releases/sort_by/release_count/asc')
def get_releases_sorted_by_count():
    sorted_by_release_count = sorted(releases, key = lambda item: item['release_count'])
    return sorted_by_release_count

@app.get('/releases/sort_by/total_labor_hours/desc')
def get_releases_sorted_by_labor_hours():
    sorted_by_labor_hours = sorted(releases, key = lambda item: item['total_labor_hours'], reverse = True)
    return sorted_by_labor_hours

@app.get('/releases/sort_by/total_labor_hours/asc')
def get_releases_sorted_by_labor_hours():
    sorted_by_labor_hours = sorted(releases, key = lambda item: item['total_labor_hours'])
    return sorted_by_labor_hours




Add a top 3 or 5 to most active months
Add Restful API that retruns data in CSV format
Add Readme
Provide live URL of hosted API
dockerize API
