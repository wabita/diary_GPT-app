from fastapi import FastAPI
from pydantic import BaseModel,Field
from datetime import date
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class DiaryInput(BaseModel):
    title: str
    content: str

class DiaryOutput(DiaryInput):
    posted_on: str
    commented: str

def generate_comment(content: str) -> str:
    if "疲れた" in content:
        return "お疲れさまでした。しっかり休んでね。"
    elif "嬉しい" in content:
        return "それはよかったね！"
    elif "ねこ" in content:
        return "猫って癒されるよね〜"
    else:
        return "今日も一日よくがんばりました。"

@app.get("/")
def home():
    return {"message": "このサイトは日記投稿APIです。"}
    
filename = "diary.json"
diary_data=[]

if not os.path.exists(filename):
    with open(filename,"w",encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False)

with open(filename,"r",encoding="utf-8") as f:
        diary_data =json.load(f)


@app.post("/items", response_model = DiaryOutput)
def create_item(item: DiaryInput):
    today =date.today().strftime("%Y/%m/%d/%a")
    comment = generate_comment(item.content)
    diary= DiaryOutput(title=item.title, 
        content=item.content, 
        posted_on=today,
        commented= comment
    )
    diary_data.append(diary.model_dump())
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(diary_data, f, ensure_ascii=False)
    return diary

@app.get("/diaries")
def get_diary():
    with open(filename,"r",encoding="utf-8") as f:
        data= json.load(f)
    return data

@app.get("/form", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("form.html", context)

@app.get("/list", response_class=HTMLResponse)
async def show_list(request: Request):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return templates.TemplateResponse("list.html", {"request": request, "diaries": data})
