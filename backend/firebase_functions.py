import firebase_admin
from pdf_to_text import extract_pdf_text
from flask import request, redirect, url_for, render_template
from firebase_admin import credentials, storage, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('backend\\API_credentials.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'freesic-storage.appspot.com'
})

# Initialize Firestore client
db = firestore.client()

# Keep track of the latest uploaded file
latest_file = None

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
            'text_content': '',  # Placeholder for text content
            'id': doc_ref.id
        })

        # Update latest file
        latest_file = {
            'filename': file.filename,
            'url': blob.public_url,
            'text_content': '',  # Placeholder for text content
            'id': doc_ref.id
        }

        return redirect(url_for('manage'))

def manage_file():
    global latest_file

    if latest_file:
        files = [latest_file]
    else:
        files = []

    return render_template('manage.html', files=files)

def view_file(file_id):
    # Retrieve the specific document from Firestore
    doc_ref = db.collection('files').document(file_id)
    file = doc_ref.get().to_dict()

    if not file:
        return 'File not found', 404

    text_content = file.get('text_content', '')

    if not text_content:
        bucket = storage.bucket()
        blob = bucket.blob(file['filename'])
        text_content = extract_pdf_text(blob)
        file['text_content'] = text_content
        doc_ref.update({'text_content': text_content})

    return render_template('view.html', file=file)
