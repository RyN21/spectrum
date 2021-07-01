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

I started by first, converting the API call 'https://www.energy.gov/sites/prod/files/2020/12/f81/code-12-15-2020.json' to JSON for me to use.
Next I converted that to a csv file called 'releases.csv'.
Keeping simplicity in mind, I decided to create an in memory database and created it as a dictionary. This would allow me to add new releases to the "database" as well as add to already exisitng releases that contained the same organization, and add to the releases of that said organization, along with updating the total_labor_hours, the release_count, and the all_in_production item withing the organizations' releases. 

After all the data was added, I needed to fine tune the dictionary a bit to output the correct data. I collected data on the status of each release to determine whether all of an organization's releases where in development or production, this would be removed for the final output. In regards to the 'most_active_months', I decided to stick with a top 3 count. I collected the most 3 most frequent months, and saved a list of those 3. After the fine tuning was complete, I saved the dictionary as 'releases'.

The final step was creating the routes for the API. This step was simply taking the releases dictionary, converting it into a JSON object, and the returning that object based on the URL. I was able to sort the releases through a simple sorted function, and could sort in ascending or descending order, based on the way the user calls the API in the URL. 
For the CSV file that was to be returned, I converted the releases dictionary to csv and saved it as 'releases_new.csv'. I then used a package called 'pandas' to read the csv fil and convert it to a table within an html file. Thus, the returned file provided the csv data in table format within an HTML file. 


## Thoughts

This challenge, I must admit was more challenging than I thought. This was due to the fact that I have never written a line of Python in my past. Ruby is the language I am most familiar with and Rails is the framework I enjoy using. Using FastAPI was also something I was not used to. FastAPI, though simple, really did not provide and file structure. I would like to have designed a place to perfom tasks, such as creating a creace_csv file or function, as it is being done twice, and this goes against the DRY principle. I also would like to have broken the main.py file into other files, ss this is violating the Single-Responsibility design principle. However, given the amount of time this has taken me, and it being a new languege, I thought simplicity would be best to complete this challenge. 

In the end, I reallly enjoyed learning some Python and working with something new. I enjoyed the entire process of researching, implementing, and troubleshooting the many errors I did came across. I am eager to learn and this was a great experience. 

I look forward to the next stage in this interviewing process. 
