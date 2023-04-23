## API Project Readme

This is a Python API project for managing trades using FastAPI framework and MongoDB database. This project is created for the backend developer position.
Requirements

- Python 3.6 or above
- MongoDB
- fastapi
- pymongo
- python-dotenv

### Installation

1. Clone the repository:

```
git clone https://github.com/mishrarohit10/Rohit-Mishra_Back_End.git
cd Rohit-Mishra_Back_End
```

2. Create a virtual environment and activate it:

```
python3 -m venv env
source env/bin/activate
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Create a .env file and set the MONGO_URI variable to your MongoDB URI:

```
MONGO_URI=<your-mongodb-uri>
```

### Usage

- Start the API server:

```
uvicorn main:app --reload
```

- Open your web browser and go to http://localhost:8000/docs to view the Swagger UI for the API.

- Use the Swagger UI to test the API endpoints.

### API Endpoints
1. GET /showall

> This endpoint returns a list of trades based on the query parameters. The query parameters are optional and can be used to filter, sort and paginate the results.

- Query Parameters

```
asset_class: Filter by asset class.
end: Filter by end date time.
max_price: Filter by maximum trade price.
min_price: Filter by minimum trade price.
start: Filter by start date time.
trade_type: Filter by trade type (BUY/SELL).
page_no: Page number (default is 0).
per_page: Number of trades per page (default is 10).
sort_by: Sort by field (tradeId, assetClass, counterparty, instrumentName, tradeDateTime, trader).
sort_order: Sort order (asc or desc).
```

- Example

> To get all trades of type SELL with asset class Equity sorted by tradeDateTime in descending order, use the following URL:

```
http://localhost:8000/showall?trade_type=SELL&asset_class=Equity&sort_by=tradeDateTime&sort_order=desc
```

2. GET /getbyid/{id}

> This endpoint returns a trade by its tradeId.

- Path Parameters
```
id: The trade ID.
```
- Example

> To get the trade with ID 123, use the following URL:

```
http://localhost:8000/getbyid/123
```