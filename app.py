from flask import Flask, render_template, request, redirect
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit

app = Flask(__name__)

tasks = []

# 🔁 This function checks for tasks due at the current time
def check_tasks():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"⏰ Checking tasks at {now}")
    for task in tasks:
        if not task['notified'] and task['datetime'] == now:
            print(f"🔔 Reminder: {task['title']} - {task['description']}")
            task['notified'] = True

# 🗓 Start background scheduler to run every 60 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_tasks, trigger="interval", seconds=60)
scheduler.start()

# 🔒 Ensure scheduler stops properly when app shuts down
atexit.register(lambda: scheduler.shutdown())

# 🌐 Main route for homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        description = request.form['description']
        datetime_input = request.form['datetime']  # Format: 2025-07-06T23:10

        # Convert to datetime and format properly
        datetime_obj = datetime.strptime(datetime_input, "%Y-%m-%dT%H:%M")
        formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M")

        # Store the task
        tasks.append({
            'title': title,
            'description': description,
            'datetime': formatted_datetime,
            'notified': False
        })

        return redirect('/')
    return render_template('index.html', tasks=tasks)

# ▶️ Start the Flask app
if __name__ == '__main__':
    print("🟢 Flask app and scheduler are running...")
    app.run(debug=True)
