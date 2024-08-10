import os
from flask import Blueprint, current_app, jsonify, request, redirect, url_for
from PIL import Image
from helpers import download_from_s3, get_secure_filename_filepath

bp = Blueprint('actions', __name__, url_prefix='/actions')


@bp.route('/resize', methods=["POST"])
def resize():
    filename = request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        width, height = int(request.json['width']), int(request.json['height'])
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = image.resize((width, height))
        out.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', filename=filename)) 

    except FileNotFoundError:
        return jsonify({'message': "File not found"}), 404


@bp.route('/presets/<preset>', methods=["POST"])
def presets(preset):
    presets = {'small': (640, 400), 'medium': (1200, 960), 'large': (1600, 1200)}

    if preset not in presets:
        return jsonify({'message': "The preset is not avaliable"}), 400
    
    filename = request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        size = presets[preset]
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = image.resize(size)
        out.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', filename=filename)) 

    except FileNotFoundError:
        return jsonify({'message': "File not found"}), 404


@bp.route('/rotate', methods=["POST"])
def rotate():
    filename = request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        degree = float(request.json['degree'])
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = image.rotate(degree)
        out.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', filename=filename)) 

    except FileNotFoundError:
        return jsonify({'message': "File not found"}), 404


@bp.route('/flip', methods=["POST"])
def flip():
    filename = request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = None
        if request.json['direction'] == 'horizontal':
            out = image.transpose(Image.FLIP_TOP_BOTTOM)            
        else:
            out = image.transpose(Image.FLIP_LEFT_RIGHT)
        out.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', filename=filename)) 

    except FileNotFoundError:
        return jsonify({'message': "File not found"}), 404