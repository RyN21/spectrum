# Spectrum API

Spectrum API is an API written in Python on fhte FastAPI framework. 
This is my first build in Python. When deciding which framework I would use between Django, Flask, and FastAPI, it really came down to Flask and FastAPI for their simplicity. I favored FastAPI for being the newer of the two, and the hype around it. 

## Instructions to get started

The instructions are quite simple. 
- Clone this repository to your computer
- Make sure to have the following installed:
  - pip install fastapi
  - pip install hypercorn
  - pip install pandas
- run `$ hypercorn main:app`

Once it is up and running, you can make a few different calls to your localhost to get back JSON responses.
  - http://localhost:8000/releases : gets all the releases in no particular order
  - http://localhost:8000/releases/sort_by/organizations : gets all the releases sorted by organizations alphabetically. 
  - http://localhost:8000/releases/sort_by/release_count/desc : gets all the releases sorted by the count of releases per organization starting with the most. 
  - http://localhost:8000/releases/sort_by/release_count/asc : gets all the releases sorted by the count of releases per organization starting with the least.
  - http://localhost:8000/releases/sort_by/total_labor_hours/desc : gets all the releases sorted by the total labor hours per organization starting with the most.
  - http://localhost:8000/releases/sort_by/total_labor_hours/asc : gets all the releases sorted by the total labor hours per organization starting with the least.
  - http://localhost:8000/releases/csv : gets all the release data in csv format and puts in into a table.

## Design and build

Being new to Python and FastAPI, I took the simplist approach and created everytihng on one file, 'main.py'

I started by  

## 
