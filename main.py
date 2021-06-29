from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# in memory database
db = []

class Organizations(BaseModel):
    organization: str
    release_count: int
    total_labor_hours: int
    all_in_production: boolean
    licenses: list
    most_active_months: list

@app.get('/')
def index():
    return {'key' : 'value'}

@app.get('/organizations')
def get_organizations():
    return db

@app.post('/organizations')


@app.get('/sort_by/organizations')
def get_organizations_sorted():
    return db

# @app.get('/sort_by/')
# @app.get('/sort_by/')
