from flask import Flask, render_template, request, jsonify, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Path to attendance records file
ATTENDANCE_FILE = 'attendance_records.csv'

# Initialize CSV file if it doesn't exist
def init_attendance_file():
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Roll Number', 'Date', 'Time', 'Status'])

init_attendance_file()

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

@app.route("/mark-attendance", methods=['POST'])
def mark_attendance():
    data = request.json
    name = data.get('name')
    roll_number = data.get('roll_number')
    status = data.get('status', 'Present')
    
    if not name or not roll_number:
        return jsonify({'error': 'Name and Roll Number are required'}), 400
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # Append to CSV file
    with open(ATTENDANCE_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, roll_number, current_date, current_time, status])
    
    return jsonify({'success': True, 'message': f'Attendance marked for {name}'}), 201

@app.route("/view-attendance")
def view_attendance():
    records = []
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as f:
            reader = csv.DictReader(f)
            records = list(reader)
    
    return render_template("view_attendance.html", records=records)

@app.route("/api/attendance-records")
def get_attendance_records():
    records = []
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as f:
            reader = csv.DictReader(f)
            records = list(reader)
    
    return jsonify(records)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)