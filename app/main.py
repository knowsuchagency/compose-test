from flask import render_template, request
from app import app
from app.tasks import get_weather

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    if request.method == 'POST':
        location = request.form['location']
        weather_task = get_weather(location)
        weather = weather_task.get(blocking=True)
    return render_template('index.html', weather=weather)
