from flask import Flask, render_template, request, redirect, url_for
from firebase_functions import upload_file, manage_file, view_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    return upload_file()

@app.route('/manage')
def manage():
    return manage_file()

@app.route('/view/<file_id>')
def view(file_id):
    # Call view_file to get the file content
    model_response = view_file(file_id)
    return render_template('view.html', response=model_response)

if __name__ == '__main__':
    app.run(debug=True)
