from flask import Flask, render_template
from firebase_functions import upload_file, view_file

app = Flask(__name__)

# Keep track of the latest uploaded file
latest_file = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    upload_file()

@app.route('/manage')
def manage():
    global latest_file

    if latest_file:
        files = [latest_file]
    else:
        files = []

    return render_template('manage.html', files=files)

@app.route('/view')
def view():
    view_file()
