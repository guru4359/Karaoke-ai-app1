from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
import uuid
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio_file' in request.files:
        file = request.files['audio_file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
            file.save(filepath)
            return send_file(filepath, as_attachment=True)
    elif 'youtube_url' in request.form:
        yt_url = request.form['youtube_url']
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            subprocess.run(['yt-dlp', '-x', '--audio-format', 'mp3', '-o', filepath, yt_url], check=True)
            return send_file(filepath, as_attachment=True)
        except Exception as e:
            return f"Failed to download: {str(e)}"
    return redirect(url_for('index'))
