import pandas as pd
from flask import Blueprint, request, jsonify
from os import path
from io import BytesIO
from random import randint
from db_handler import save_csv_metadata
from logging_handler import logger
from config import UPLOAD_FOLDER
from util import linear_trend_forecast


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

    try:
        df = pd.read_csv(BytesIO(file.stream.read()), header=None, names=['Name', 'Date', 'Price'])

        # Check if DF is empty.
        if df.empty:
            logger.error("CSV file is empty")
            return jsonify({"error": "CSV file is empty."}), 400

        # Check if DF has 3 columns.
        if len(df.columns) != 3:
            logger.error(f"CSV file has {len(df.columns)} columns.")
            return jsonify({"error": "CSV file must have three columns."}), 400

        # Check Date column.
        try:
            df["Date"] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        except ValueError:
            logger.error(f"Error validating CSV - DATE column. {ValueError}")
            return jsonify({"error": "Invalid CSV - DATE column - Check logs for more info."}), 400

    except Exception as e:
        logger.error(f"Error validating CSV: {str(e)}")
        return jsonify({"error": "Error validating CSV."}), 400

    # Save file in UPLOADS folder.
    file_path = path.join(UPLOAD_FOLDER, file.filename)
    df.index.name = 'idx'
    df.to_csv(file_path, index=True)

    # Save metadata in DB.
    save_csv_metadata(file.filename, file_path)

    logger.info(f"File {file.filename} uploaded successfully")
    return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200


@api_blueprint.route('/get_timeseries', methods=['GET'])
def get_timeseries():
    """
    API endpoint: /get_timeseries
    Expect filename as param.
    Example cURL:
        curl --location 'http://127.0.0.1:5000/get_timeseries?filename=stock_prices.csv'
    :return: Data as list of dicts with the following keys: timestamp / stock_price / stock_name or Error.
    """
    filename = request.args.get('filename')
    if not filename:
        logger.error("Filename not provided")
        return jsonify({"error": "Filename is required"}), 400

    file_path = path.join(UPLOAD_FOLDER, filename)
    if not path.exists(file_path):
        logger.error("File not found")
        return jsonify({"error": "File not found"}), 404

    try:
        df = pd.read_csv(file_path)
        if len(df) < 10:
            return jsonify({"error": "Not enough data points"}), 400

        start_idx = randint(0, len(df) - 10)
        selected_points = df.iloc[start_idx:start_idx + 10].to_dict(orient='records')

        logger.info(f"Returning 10 points from index {start_idx}")
        return jsonify({"data": selected_points}), 200
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({"error": "Failed to process file"}), 500


@api_blueprint.route('/get_forecast', methods=['GET'])
def get_forecast():
    filename = request.args.get('filename')
    if not filename:
        logger.error("Filename not provided")
        return jsonify({"error": "Filename is required"}), 400

    file_path = path.join(UPLOAD_FOLDER, filename)
    if not path.exists(file_path):
        logger.error("File not found")
        return jsonify({"error": "File not found"}), 404

    start_idx = request.args.get('start_idx')
    if not start_idx:
        logger.error("No starting index provided.")
        return jsonify({"error": "Starting index is required"}), 400

    try:
        df = pd.read_csv(file_path)
        forecast = linear_trend_forecast(df.loc[int(start_idx) - 10:int(start_idx)])

        # Forecast future values
        forecast.to_dict(orient='records')

        return jsonify({"data": forecast.to_dict(orient='records')}), 200

    except Exception as e:
        logger.error(f"Error creating forecast: {str(e)}")
        return jsonify({"error": "Failed to create forecast."}), 500


if __name__ == '__main__':
    pass
