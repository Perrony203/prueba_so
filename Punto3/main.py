from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from pymongo import MongoClient 
from dotenv import load_dotenv
from bson.binary import UuidRepresentation
import os
import boto3
from boto3.s3.transfer import S3Transfer
import json
import io

s3 = boto3.client('s3')
transfer = S3Transfer(s3)

load_dotenv()

app = FastAPI()

client = MongoClient(os.getenv("MONGO_URI"), uuidRepresentation="standard")
db = client[os.getenv("MONGO_DB")]
collection = db[os.getenv("MONGO_COLLECTION")] 

class Item(BaseModel):     
    name: str 
    price: float

class ItemResponse(BaseModel):
    id: UUID
    name: str
    price: float
    createdAt: datetime

@app.get("/items/", response_model=list[ItemResponse])
def read_items():
    items = []
    for doc in collection.find():          
        items.append(ItemResponse(**doc))
    return items

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: str):
    item = collection.find_one({"id": UUID(item_id)})
    if item:
        return ItemResponse(**item)
    else:
        raise HTTPException(status_code=404, detail="Item no encontrado") 

@app.post("/items/")
def create_item(item: Item):
    new_item = {
        "id": uuid4(),
        "name": item.name,
        "price": item.price,
        "createdAt": datetime.now()
    }
    
    collection.insert_one(new_item)
    new_item.pop("_id", None)
    
    # new_item["id"] = str(new_item["id"])
    # new_item["createdAt"] = str(new_item["createdAt"])
    
    nombre = str("doc-" + new_item['name'] + ".json")
    
    jsonBytes = json.dumps(new_item, default = str).encode('utf-8')
    fileObj = io.BytesIO(jsonBytes)
    
    s3.upload_fileobj(Fileobj = fileObj, Bucket = 'user-spcjaga-smm-ueia-so', Key = nombre)
    
    return {"mensaje": "Item creado con éxito", "data": new_item}