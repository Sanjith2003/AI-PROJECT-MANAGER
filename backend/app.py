import firebase_admin
from pdf_to_text import extract_pdf_text
from firebase_admin import credentials, storage, firestore
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('backend\\API_credentials.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'freesic-storage.appspot.com'
})

# Initialize Firestore client
db = firestore.client()

# Keep track of the latest uploaded file
latest_file = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global latest_file

    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    if file:
        # Upload file to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)

        # Save file metadata to Firestore
        doc_ref = db.collection('files').document()
        doc_ref.set({
            'filename': file.filename,
            'url': blob.public_url,
            'text_content': ''  # Placeholder for text content
        })

        # Update latest file
        latest_file = {
            'filename': file.filename,
            'url': blob.public_url,
            'text_content': ''  # Placeholder for text content
        }

        return redirect(url_for('manage'))

@app.route('/manage')
def manage():
    global latest_file

    if latest_file:
        files = [latest_file]
    else:
        files = []

    return render_template('manage.html', files=files)

@app.route('/view')
def view_file():
    global latest_file

    if not latest_file:
        return 'No file uploaded yet'

    # Retrieve text content if available
    text_content = latest_file.get('text_content', '')

    if not text_content:
        bucket = storage.bucket()
        blob = bucket.blob(latest_file['filename'])
        text_content = extract_pdf_text(blob)
        latest_file['text_content'] = text_content

    return render_template('view.html', file=latest_file)