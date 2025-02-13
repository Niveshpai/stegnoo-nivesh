import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ENCRYPTED_FOLDER'] = 'encrypted'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ENCRYPTED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def encode_message(img, msg, password):
    d = {}
    c = {}
    for i in range(255):
        d[chr(i)] = i
        c[i] = chr(i)

    m = 0
    n = 0
    z = 0

    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    return img

def decode_message(img, msg_length):
    c = {}
    for i in range(255):
        c[i] = chr(i)

    message = ""
    n = 0
    m = 0
    z = 0

    for i in range(msg_length):
        message += c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    return message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(request.url)

    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    return render_template('encode.html', filename=file.filename)

@app.route('/encode', methods=['POST'])
def encode():
    if 'file' not in request.files:
        return redirect(request.url)

    img_path = os.path.join(app.config['UPLOAD_FOLDER'], request.form['filename'])
    img = cv2.imread(img_path)

    msg = request.form['message']
    password = request.form['password']

    encoded_img = encode_message(img, msg, password)

    encoded_filename = os.path.join(app.config['ENCRYPTED_FOLDER'], 'encrypted_' + request.form['filename'])
    cv2.imwrite(encoded_filename, encoded_img)

    return send_from_directory(app.config['ENCRYPTED_FOLDER'], 'encrypted_' + request.form['filename'], as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_file = request.files['file']
    if encrypted_file.filename == '' or not allowed_file(encrypted_file.filename):
        return redirect(request.url)

    filename = os.path.join(app.config['ENCRYPTED_FOLDER'], encrypted_file.filename)
    encrypted_file.save(filename)

    img = cv2.imread(filename)

    msg_length = len(request.form['message'])
    decrypted_message = decode_message(img, msg_length)

    return render_template('decrypt.html', message=decrypted_message)

if __name__ == '__main__':
    app.run(debug=True)
