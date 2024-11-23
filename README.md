# Vancouver Crime Data Visualization - Backend
The backend service for the Vancouver crime data visualization.

Data from [GeoDASH VPD Open Data](https://geodash.vpd.ca/opendata/#).

## Dependencies
Python 3.13+

PostgreSQL 17

FastAPI

    pip install "fastapi[standard]"

SQLAlchemy

    pip install SQLAlchemy
  
psycopg2

    pip install psycopg2

## How to Run
    DB_USERNAME=<YOUR_USERNAME> DB_PASSWORD=<YOUR_PASSWORD> fastapi dev main.py
