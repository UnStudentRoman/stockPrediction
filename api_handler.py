from flask import Blueprint, request, jsonify
import pandas as pd
import os
import random
from db_handler import save_csv_metadata
from logging_handler import logger
from config import UPLOAD_FOLDER


# Create API Blueprint for modularity.
api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/upload', methods=['POST'])
def upload_csv():
    """
    Expect file as .csv in body of the request.
    Example cURL:
        curl    --location 'http://127.0.0.1:5000/upload' \
                --form 'file=@"/stock_prices.csv"'
    :return: Response
    """
    if 'file' not in request.files:
        logger.error("No file part in request")
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.csv'):
        logger.error("Invalid file type")
        return jsonify({"error": "Invalid file type. Only CSV allowed"}), 400

    logger.info(f"File {file.filename} uploaded successfully")
    return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200


if __name__ == '__main__':
    pass
