import os
from flask import Blueprint, current_app, jsonify, request, redirect, url_for
from PIL import Image, ImageEnhance, ImageFilter
from helpers import download_from_s3, get_secure_filename_filepath

bp = Blueprint('filters', __name__, url_prefix='/filters')


@bp.route('/blur', methods=["POST"])
def blur():
    filename = request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        radius = int(request.json['radius'])
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = image.filter(ImageFilter.GaussianBlur(radius))
        out.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', filename=filename)) 

    except FileNotFoundError:
        return jsonify({'message': "File not found"}), 404


@bp.route('/contrast', methods=["POST"])
def contrast():
    filename = request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        factor = float(request.json['factor'])
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = ImageEnhance.Contrast(image).enhance(factor)
        out.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', filename=filename)) 

    except FileNotFoundError:
        return jsonify({'message': "File not found"}), 404


@bp.route('/brightness', methods=["POST"])
def brightness():
    filename = request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        factor = float(request.json['factor'])
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream)
        out = ImageEnhance.Brightness(image).enhance(factor)
        out.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', filename=filename)) 

    except FileNotFoundError:
        return jsonify({'message': "File not found"}), 404