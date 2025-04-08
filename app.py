from flask import Flask, render_template, request, redirect, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


USERS = {
    'admin': 'admin',
    'operator': 'admin'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def log():
    return render_template('login.html')

@app.route('/detect',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/detections', methods=['POST'])
def detections():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # In a real app, you would process the image here
        # For now, we'll just return the same image as "processed"
        processed_image = filename

        # Mock detection results
        results = {
            'image_path': os.path.join('uploads', filename),
            'confidence': '92%',
            'objects_count': '3'
        }

        return render_template('index.html', **results)

@app.route('/login_in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USERS and USERS[username] == password:
            return redirect('/detect')
        else:
            return "Invalid credentials", 401

    return render_template('login.html')


if __name__ == '__main__':
    app.run()