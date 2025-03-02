# Stock Prediction - Flask Backend Documentation

## Overview
This project is a Flask-based backend that provides an API for uploading CSV files containing time series stock data. It also serves random data points and predicts future values.

## Requirements

### Set-up a Virtual Environment & Install Dependencies
Ensure you have Python installed, then install the required dependencies:

```sh
python -m venv venv
pip install -r requirements.txt
```

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
cd flask-backend
```

2. Install dependencies:
```sh
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

### Upload CSV
**Endpoint:** `POST /upload`
- Uploads a CSV file to the backend.
- Returns a success or error message.

### Get Random Time Series Data
**Endpoint:** `GET /get_timeseries`
- Retrieves 10 random points from the uploaded CSV.

## Adding Swagger API Documentation
To enable Swagger UI for API documentation:

1. Install `flask-swagger-ui`:
```sh
pip install flask-swagger-ui
```

2. Modify `main.py` to include Swagger UI:
```python
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"  # Path to your OpenAPI JSON file
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
```

3. Create a `static/swagger.json` file with API definitions.

4. Access Swagger UI at:
```
http://localhost:5000/api/docs
```

## Logging
- Logs are stored in `logs/app.log`.
- The `logging_handler.py` module ensures structured logging.

## Database
- SQLite is used for storing CSV metadata.
- Data is stored in `database/data.db`.

## Future Enhancements
- Improved prediction models for stock data.
- User authentication and multi-file support.

## License
This project is open-source. Modify and use it as needed.
