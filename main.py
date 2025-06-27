from flask import Flask, render_template, request, redirect, url_for
import requests
import datetime
import os

app = Flask(__name__)

tasks = []
notes = []

# Insert your real API key here
WEATHER_API_KEY = 'YOUR_WEATHER_API_KEY'
QUOTE_API_URL = 'https://api.quotable.io/random'

@app.route('/')
def home():
    city = 'Chennai'
    weather = get_weather(city)
    quote = get_quote()
    return render_template("index.html", tasks=tasks, notes=notes, weather=weather, quote=quote)

@app.route('/add-task', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks.append({'task': task, 'time': datetime.datetime.now().strftime('%H:%M')})
    return redirect(url_for('home'))

@app.route('/delete-task/<int:index>')
def delete_task(index):
    if 0 <= index < len(tasks):
        del tasks[index]
    return redirect(url_for('home'))

@app.route('/add-note', methods=['POST'])
def add_note():
    note = request.form.get('note')
    if note:
        notes.append({'note': note, 'date': datetime.date.today().strftime('%Y-%m-%d')})
    return redirect(url_for('home'))

@app.route('/delete-note/<int:index>')
def delete_note(index):
    if 0 <= index < len(notes):
        del notes[index]
    return redirect(url_for('home'))

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        weather = {
            'city': city,
            'temp': data['main']['temp'],
            'description': data['weather'][0]['description'].capitalize(),
            'icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }
        return weather
    except Exception as e:
        print("Weather Error:", e)
        return {
            'city': city,
            'temp': '',
            'description': '',
            'icon': ''
        }

def get_quote():
    try:
        response = requests.get(QUOTE_API_URL).json()
        return {'content': response['content'], 'author': response['author']}
    except:
        return {'content': 'Be your best self.', 'author': 'Anonymous'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
