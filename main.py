from enum import Enum
from fastapi import FastAPI
import datetime as dt
from datetime import timezone

from models.operations import TradeRead
from database import collection

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
    
    if max_price or min_price:
        query['tradeDetails.price'] = {}
        if max_price:
            query['tradeDetails.price']["$lte"] = max_price   
        if min_price:
            query['tradeDetails.price']["$gte"] = min_price

    if start or end:
        query["tradeDateTime"] = {}
        if start:
            start.replace(tzinfo=timezone.utc)
            query["tradeDateTime"]["$gt"] = start
        elif end:
            end.replace(tzinfo=timezone.utc)
            query["tradeDateTime"]["$lt"] = end

    if trade_type: 
        query["tradeDetails.buySellIndicator"] = trade_type
    
    sort_dir = 1
    if(sort_order == 'asc'):
        sort_dir = 1
    else:
        sort_dir = -1

    cursor = collection.find(query, {'_id': 0}).limit(per_page).skip(page_no * per_page).sort(
        key_or_list=sort_by, direction=sort_dir)
    
    return [TradeRead(**document) for document in cursor]

@app.get("/getbyid/{id}")
def get_by_id(id:str):
    trade = collection.find_one({"tradeId": id}, {'_id': 0})
    return TradeRead(**trade)