from fastapi import FastAPI
from pydantic import BaseModel,Field
from datetime import date

app = FastAPI()

class DiaryInput(BaseModel):
    title: str
    content: str

class DiaryOutput(DiaryInput):
    posted_on: date

@app.get("/")
def home():
    return {"message": "このサイトは日記投稿APIです。"}
    
diary_list =[]

@app.post("/items/", response_model = DiaryOutput)
def create_item(item: DiaryInput):
    today =date.today()
    diary= DiaryOutput(title=item.title, content=item.content, posted_on=today)
    diary_list.append(diary)
    return diary

@app.get("/diary_page")
def get_diary():
    return diary_list