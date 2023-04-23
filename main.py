from enum import Enum
import pprint
from fastapi import FastAPI
import datetime as dt

from models.operations import TradeRead
from database import collection

class SortOrder(str, Enum):
    asc = 'asc'
    desc = 'desc'

class SortBy(str, Enum):
    trade_id = 'trade_id'
    asset_class = 'asset_class'
    counterparty = 'counterparty'
    instrument_name = 'instrument_name'
    trade_date_time = 'trade_date_time'
    trader = 'trader'

class TradeType(str, Enum):
    SELL = 'SELL'
    BUY = 'BUY'


app = FastAPI()

@app.get("/showall")
def show(asset_class:str | None = None, end: dt.datetime | None = None, max_price:float| None = None,min_price:float| None = None,start:dt.datetime | None = None, trade_type:TradeType | None = None, page_no: int = 0, per_page: int = 10, sort_by:SortBy = "trade_id", sort_order: SortOrder = "asc"):

    query = {}

    if asset_class:
        query['asset_class'] = asset_class
    
    if end:
        query["end"]["$lt"] = end
        
    if max_price: 
        query["trade_details.price"]["$lt"] =  max_price
            
    if min_price:
        query["trade_details.price"]["$gt"] = min_price

    if start:
        query["start"]["$gt"] = start

    if trade_type: 
        query["trade_details.buySellIndicator"] = trade_type
    
    sort_dir = 1
    if(sort_order == 'asc'):
        sort_dir = 1
    else:
        sort_dir = -1
    cursor = collection.find(query, {'_id': 0}).limit(per_page).skip(page_no * per_page).sort(
        key_or_list=sort_by, direction=sort_dir)
    
    return [TradeRead(**document) for document in cursor]

@app.get("/getbyid/{id}")
def get_by_id(id:int):
    trade = collection.find_one({"trade_id": id}, {'_id': 0})
    return trade

@app.post("/addtrade")
def add(instrument_id:int, instrument_name:str, trade_date_time:dt.date,buySellIndicator:str, price:float, quantity:int, trade_id:int , trader:str,asset_class:str | None = None,counterparty:str| None = None):

    query = {}
    
    if asset_class:
        query['asset_class'] = asset_class

    if counterparty:
        query['counterparty'] = counterparty

    if instrument_id:
        query['instrument_id'] = instrument_id

    if instrument_name:
        query['instrument_name'] = instrument_name

    if trade_date_time:
        query['trade_date_time'] = trade_date_time

    if buySellIndicator:
        query['trade_details.buySellIndicator'] = buySellIndicator

    if price:
        query['trade_details.price'] = price
        
    if quantity:
        query['trade_details.quantity'] = quantity

    if trade_id:
        query['trade_id'] = trade_id

    if trader:
        query['trader'] = trader
    return query

# @app.delete("/delete/{id}")
# def deleted_by_id(id:int):
#     collection.delete_one({"tradeId":id},{'_id':0})
#     return True

  



