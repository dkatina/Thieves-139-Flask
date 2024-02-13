from . import main
from flask import render_template, request
import requests


# / route is your home route
@main.route('/')
def home():
    return render_template('home.html')

#routes taking in URL parameter "name"
@main.route('/user/<name>')
def user(name):
    return f'Hello {name}'

#useing my API helper functions
def getDriverInfo(driver):
    driver_info = {
        'position': driver['position'],
        'first_name': driver['Driver']['givenName'],
        'last_name': driver['Driver']['familyName'],
        'DOB': driver['Driver']['dateOfBirth'],
        'wins': driver['wins'],
        'team': driver['Constructors'][0]['name']
    }
    return driver_info

def driver_info_year_rnd(year, rnd):
    url = f'https://ergast.com/api/f1/{year}/{rnd}/driverStandings.json'
    response = requests.get(url)
    output = []
    if response.ok:
        data = response.json()
        driver_standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        for driver in driver_standings:
            driver_dict = getDriverInfo(driver)
            output.append(driver_dict)
    return output
    
@main.route('/ergast', methods=['GET', 'POST'])
def ergast():
    if request.method == 'POST':
        year = request.form.get('year')
        rnd = request.form.get('round')
        drivers = driver_info_year_rnd(year, rnd)
        return render_template('ergast.html', drivers=drivers)
    else:
        return render_template('ergast.html')