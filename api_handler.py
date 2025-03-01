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
    API endpoint: /upload
    Expect file as .csv in body of the request. Check if file is .csv format
    Example cURL:
        curl    --location 'http://127.0.0.1:5000/upload' \
                --form 'file=@"/stock_prices.csv"'
    :return: Response
    """
    if 'file' not in request.files:
        logger.error("No file part in request")
        return jsonify({"error": "No file part in request body."}), 400

    file = request.files['file']

    if file.filename == '':
        logger.error("No selected file")
        return jsonify({"error": "No selected file."}), 400

    if not file.filename.endswith('.csv'):
        logger.error("Invalid file type")
        return jsonify({"error": "Invalid file type. Only CSV allowed."}), 400

    """
    TO ADD
    Preliminary check of the csv file. Make sure there are no nulls. 
    If nulls are found solve them depending on type of data in the column.
    Ex. If null in datetime column drop row or calculate timedelta between points and use it to determine missing point.
    If null in value column, make it 0.
    If null in object (str) type column fill in from previous row.
    If multiple values in str type column notify the user about it and keep only rows with most appearances. 
    """

    # Save file in UPLOADS folder.
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Save metadata in DB.
    save_csv_metadata(file.filename, file_path)

    logger.info(f"File {file.filename} uploaded successfully")
    return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200


if __name__ == '__main__':
    pass
