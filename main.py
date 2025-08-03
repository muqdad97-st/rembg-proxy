from flask import Flask, request, send_file
from flask_cors import CORS
import requests
from io import BytesIO

app = Flask(__name__)
CORS(app)

API_URL = 'https://api.rembg.com/rmbg'
API_KEY = '7fbf16b4-8b60-4dc2-8738-230be8d8b106'

@app.route('/')
def home():
    return '✅ Rembg Proxy is running! Use POST /remove-bg with image file.'

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return {'error': 'No image file'}, 400

    image = request.files['image']
    files = {'image': (image.filename, image.stream, image.content_type)}

    headers = {'x-api-key': API_KEY}

    response = requests.post(API_URL, files=files, headers=headers)

    if response.status_code != 200:
        return {'error': 'Failed to remove background'}, 500

    return send_file(BytesIO(response.content), mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
