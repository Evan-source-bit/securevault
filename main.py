from flask import Flask, request
import os
from cryptography.fernet import Fernet

app = Flask(__name__)

os.makedirs('uploads', exist_ok=True)
key = Fernet.generate_key()
cipher = Fernet(key)


@app.route('/')
def index():
    return '''
    <form method="POST" action="/upload" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit">
    </form>
    '''


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    data = uploaded_file.read()
    encrypted = cipher.encrypt(data)
    with open('uploads/' + uploaded_file.filename + '.enc', 'wb') as f:
        f.write(encrypted)
    return 'File uploaded and encrypted.'


import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
