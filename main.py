from enum import Enum
from fastapi import FastAPI
import datetime as dt
from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")  
client = MongoClient(config["MONGO_URI"])

db = client['steeleye']

collection = db['trades']

class SortOrder(str, Enum):
    asc = 'asc'
    desc = 'desc'

class SortBy(str, Enum):
    tradeId = 'tradeId'
    assetClass = 'assetClass'
    counterparty = 'counterparty'
    instrumentName = 'instrumentName'
    tradeDateTime = 'tradeDateTime'
    trader = 'trader'

class TradeType(str, Enum):
    SELL = 'SELL'
    BUY = 'BUY'


app = FastAPI()

@app.get("/showall")
def show(asset_class:str | None = None, end: dt.datetime | None = None, max_price:float| None = None,min_price:float| None = None,start:dt.datetime | None = None, trade_type:TradeType | None = None, page_no: int = 0, per_page: int = 10, sort_by:SortBy = "tradeId", sort_order: SortOrder = "asc"):

    query = {}

    if asset_class:
        query['assetClass'] = asset_class
    
    if end:
        query["end"]["$lt"] = end
        
    if max_price: 
        query["tradeDetails.price"]["$lt"] =  max_price
            
    if min_price:
        query["tradeDetails.price"]["$gt"] = min_price

    if start:
        query["start"]["$gt"] = start

    if trade_type: 
        query["tradeDetails.buySellIndicator"] = trade_type
    
    result = []
    sort_dir = 1
    if(sort_order == 'asc'):
        sort_dir = 1
    else:
        sort_dir = -1
    for trades in collection.find(query, {'_id': 0}).limit(per_page).skip(page_no * per_page).sort(
        key_or_list=sort_by, direction=sort_dir):
       result.append(trades)

    return result

@app.get("/getbyid/{id}")
def get_by_id(id:int):
    trade = collection.find_one({"tradeId": id}, {'_id': 0})
    return trade

@app.post("/addtrade")
def add(instrument_id:int, instrument_name:str, trade_date_time:dt.date,buySellIndicator:str, price:float, quantity:int, trade_id:int , trader:str,asset_class:str | None = None,counterparty:str| None = None):

    query = {}
    
    if asset_class:
        query['assetClass'] = asset_class

    if counterparty:
        query['counterparty'] = counterparty

    if instrument_id:
        query['instrumentId'] = instrument_id

    if instrument_name:
        query['instrumentName'] = instrument_name

    if trade_date_time:
        query['tradeDateTime'] = trade_date_time

    if buySellIndicator:
        query['tradeDetails.buySellIndicator'] = buySellIndicator

    if price:
        query['tradeDetails.price'] = price
        
    if quantity:
        query['tradeDetails.quantity'] = quantity

    if trade_id:
        query['tradeId'] = trade_id

    if trader:
        query['trader'] = trader
    return query

# @app.delete("/delete/{id}")
# def deleted_by_id(id:int):
#     collection.delete_one({"tradeId":id},{'_id':0})
#     return True

  



