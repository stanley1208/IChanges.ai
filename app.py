from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
from external_api import get_weather, get_traffic  # Importing weather & traffic functions

app = Flask(__name__)


# Initialize Database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, name TEXT, travel_time TEXT, budget TEXT, 
                 transport TEXT, industry TEXT, single TEXT, scenarios TEXT, 
                 mbti TEXT, hobbies TEXT, indoor_outdoor TEXT, race TEXT, 
                 new_things TEXT, ai_scenario TEXT)''')
    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        travel_time = request.form['travel_time']
        budget = request.form['budget']
        transport = request.form['transport']
        industry = request.form['industry']
        single = request.form['single']
        scenarios = request.form['scenarios']
        mbti = request.form.get('mbti', 'Not provided')  # Optional field
        hobbies = request.form['hobbies']
        indoor_outdoor = request.form['indoor_outdoor']
        race = request.form['race']
        new_things = request.form['new_things']
        ai_scenario = request.form['ai_scenario']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''INSERT INTO users 
                     (name, travel_time, budget, transport, industry, single, scenarios, mbti, 
                     hobbies, indoor_outdoor, race, new_things, ai_scenario) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (name, travel_time, budget, transport, industry, single, scenarios, mbti,
                   hobbies, indoor_outdoor, race, new_things, ai_scenario))
        conn.commit()
        conn.close()

        return redirect(url_for('generate_routine', name=name))

    return render_template('register.html')


@app.route('/routine/<name>')
def generate_routine(name):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=?", (name,))
    user = c.fetchone()
    conn.close()

    if not user:
        return "User not found!", 404

    # Extract user data
    city = "San Francisco"  # You can update this dynamically later
    weather_condition = get_weather(city)
    traffic_status = get_traffic(city)

    # Get current time
    current_time = datetime.datetime.now().strftime("%H:%M")

    # Generate AI-driven routine
    routine = f"""
    Hello {user[1]}, based on your preference for {user[7]} and budget {user[3]}, 
    we suggest visiting a nearby {user[7]} location. The current time is {current_time}, 
    the weather in {city} is {weather_condition}, and the traffic status is {traffic_status}.
    """

    return render_template('routine.html', routine=routine)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
