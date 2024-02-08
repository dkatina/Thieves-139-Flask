from flask import request, render_template
import requests
from app import app
from .forms import LoginForm, SignUpForm


# / route is your home route
@app.route('/')
def hello_world():
    return render_template('home.html')

#routes taking in URL parameter "name"
@app.route('/user/<name>')
def user(name):
    return f'Hello {name}'

#HTTP methods, having to specifiy what kind of request is being sent to the route
#GET is the default route, POST says im sending info to the route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        return f'{email} {password}'
    else:
        return render_template('login.html', form=form)
    
@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        return f'{username} {email} {password}'
    else:
        return render_template('signup.html', form=form)
    

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
    
@app.route('/ergast', methods=['GET', 'POST'])
def ergast():
    if request.method == 'POST':
        year = request.form.get('year')
        rnd = request.form.get('round')
        drivers = driver_info_year_rnd(year, rnd)
        return render_template('ergast.html', drivers=drivers)
    else:
        return render_template('ergast.html')