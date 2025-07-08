from flask import Flask, render_template, request, redirect
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import threading

app = Flask(__name__)
tasks = []

def check_tasks():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    for task in tasks:
        if not task['notified'] and task['datetime'] == now:
            print(f"🔔 Reminder: {task['title']} - {task['description']}")
            task['notified'] = True

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_tasks, trigger="interval", seconds=60)
scheduler.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        datetime_input = request.form['datetime']
        tasks.append({
            'title': title,
            'description': description,
            'datetime': datetime_input,
            'notified': False
        })
        return redirect('/')
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
