import os
import uuid
import sqlite3
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from crack_logic import process_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'static/output'
app.config['DATABASE'] = 'database.db'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Create database table
def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_path TEXT,
                output_path TEXT,
                uploaded_at TEXT
            )
        ''')

@app.route('/', methods=['GET', 'POST'])
def index():
    output_filename = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_id + "_" + filename)
            file.save(input_path)

            output_filename = unique_id + "_result.png"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

            process_image(input_path, output_path)

            with sqlite3.connect(app.config['DATABASE']) as conn:
                conn.execute(
                    "INSERT INTO results (input_path, output_path, uploaded_at) VALUES (?, ?, ?)",
                    (os.path.basename(input_path), os.path.basename(output_path), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                )

            return render_template("index.html", output_image=output_filename, year=datetime.now().year)

    return render_template('index.html', output_image=None, year=datetime.now().year)

@app.route('/history')
def history():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT input_path, output_path, uploaded_at FROM results ORDER BY uploaded_at DESC")
        rows = cursor.fetchall()
    return render_template('history.html', history=rows)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
