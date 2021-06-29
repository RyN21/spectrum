from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# in memory database
db = []

class Release(BaseModel):
    organization: str
    release_count: int
    total_labor_hours: int
    all_in_production: boolean
    licenses: list
    most_active_months: list

@app.get('/')
def index():
    return {'key' : 'value'}

@app.get('/releases')
def get_releases():
    return db

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
