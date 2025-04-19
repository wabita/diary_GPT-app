from fastapi import FastAPI
from pydantic import BaseModel,Field
from datetime import date
import json
import os

app = FastAPI()

class DiaryInput(BaseModel):
    title: str
    content: str

class DiaryOutput(DiaryInput):
    posted_on: date

@app.get("/")
def home():
    return {"message": "このサイトは日記投稿APIです。"}
    
filename = "diary.json"
diary_data=[]

if os.path.exists(filename):
    with open(filename,"r",encoding="utf-8") as f:
        diary_data =json.load(f)


@app.post("/items/", response_model = DiaryOutput)
def create_item(item: DiaryInput):
    today =date.today()
    diary= DiaryOutput(title=item.title, content=item.content, posted_on=today)
    diary_data.append(diary.model_dump())
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(diary_data, f, ensure_ascii=False)
    return diary

@app.get("/diaries/")
def get_diary():
    with open(filename,"r",encoding="utf-8") as f:
        data= json.load(f)
    return data
