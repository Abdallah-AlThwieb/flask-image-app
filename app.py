import os
from dotenv import load_dotenv, dotenv_values
from flask import Flask, current_app, jsonify, request, send_from_directory
from PIL import Image
from actions import bp as actionsbp
from filters import bp as filtersbp
from android import bp as androidbp
from helpers import allowed_extension, get_secure_filename_filepath, upload_to_s3
import boto3, botocore  

load_dotenv()

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
DOWNLOAD_FOLDER = os.getenv('DOWNLOAD_FOLDER')
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS')

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['S3_BUCKET'] = os.getenv('S3_BUCKET')
app.config['S3_KEY'] = os.getenv('S3_KEY')
app.config['S3_SECRET'] = os.getenv('S3_SECRET')
app.config['S3_LOCATION'] = os.getenv('S3_LOCATION')


app.register_blueprint(actionsbp)
app.register_blueprint(filtersbp)
app.register_blueprint(androidbp)


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to Image API'})


@app.route('/images', methods=['GET', 'POST'])
def images():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file was selected.'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file was selected.'}), 400
        
        if not allowed_extension(file.filename):
            return jsonify({'error': 'The extension is not supported.'}), 400
        
        #filename, filepath = get_secure_filename_filepath(file.filename)

        output = upload_to_s3(file, app.config['S3_BUCKET'])
        #file.save(filepath)
        return jsonify({
            'message': 'File successfuly uploaded',
            'filename': output,
        }), 201
    
    images = []
    s3_resource = boto3.resource('s3', aws_access_key_id=current_app.config['S3_KEY'], aws_secret_access_key=current_app.config['S3_SECRET'])
    s3_bucket = s3_resource.Bucket(current_app.config['S3_BUCKET'])
    for obj in s3_bucket.objects.filter(Prefix='uploads/'):
        if obj.key == 'uploads/':
            continue
        images.append(obj.key)
    return jsonify({'data': images}), 200
    

@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)