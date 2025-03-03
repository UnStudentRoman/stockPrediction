# Stock Prediction - Flask Backend Documentation

## Overview
This project is a Flask-based backend that provides an API for uploading CSV files containing time series stock data. It also serves random data points and predicts future values.

## Requirements

### Set-up a Virtual Environment & Install Dependencies
Ensure you have Python installed, then install the required dependencies:

## Project Structure
```
flask-backend/
│── main.py              # Starts the Flask API
│── api_handler.py       # Handles API routes and logic
│── db_handler.py        # Handles database interactions
│── logging_handler.py   # Configures logging
│── util.py              # Helper functions
│── requirements.txt     # Dependencies
│── uploads/             # Directory for storing uploaded CSVs
│── database/            # Directory for database storage
│── logs/                # Directory for log files
└── config.py            # Centralized configuration settings
```

## Setup and Running the API

1. Clone the repository:
```sh
git clone <repository_url>
cd sockPrediction
```

2. Install dependencies:
```sh
python -m venv venv
pip install -r requirements.txt
```

3. Start the Flask application:
```sh
python main.py
```

4. The API will be available at:
```
http://localhost:5000
```

## API Endpoints

### Swagger
**Endpoint:** `GET /swagger`
- API documentation.

### Upload CSV
**Endpoint:** `POST /upload`
- Uploads a CSV file to the backend.
- Returns a success or error message.

### Get Random Time Series Data
**Endpoint:** `GET /get_timeseries`
- Retrieves 10 random points from the uploaded CSV.

### Get Time Series Forecast
**Endpoint:** `GET /get_forecast`
- Create 3 points from the uploaded CSV and the endpoint of the "/get_timeseries" data.

### Get All Uploads
**Endpoint:** `GET /all_uploads`
- Queries the database for all uploaded CSV files.

## Logging
- Logs are stored in `logs/app.log`.
- The `logging_handler.py` module ensures structured logging.

## Database
- SQLite is used for storing CSV metadata.
- Data is stored in `database/data.db`.

## How to Use

- Start Flask server by running main.py
- Query `GET /all_uploads` endpoint to see what files are in the database.
- Upload a file via `POST /upload`. 
- Check `GET /all_uploads` to make sure the file is in the database.
- Use `GET /get_timeseries` to generate 10 random points.
- Use `GET /get_forecast` to generate 3 prediction points.
