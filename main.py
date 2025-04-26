from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import date
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse , JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
import json
import os

app = FastAPI()
#静的fileとtemplate設定
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")

#入力データ
class DiaryInput(BaseModel):
    title: str
    content: str
#出力データ
class DiaryOutput(DiaryInput):
    posted_on: str
    commented: str

#コメント生成
def generate_comment(content: str) -> str:
    if "疲れた" in content:
        return "お疲れさまでした。しっかり休んでね。"
    elif "嬉しい" in content:
        return "それはよかったね！"
    elif "ねこ" in content:
        return "猫って癒されるよね〜"
    else:
        return "今日も一日よくがんばりました。"
    
#データ保存file
filename = "diary.json"

#ないときの初期file作成
if not os.path.exists(filename):
    with open(filename,"w",encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False)

#json読み込み
def load_data():
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
    
#json書き込み
def save_data(data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

#diaryをポストしてコメントと日付を追加して返す
@app.post("/items", response_model = DiaryOutput)
def create_item(item: DiaryInput):
    today =date.today().strftime("%Y/%m/%d/%a")
    comment = generate_comment(item.content)
    diary= DiaryOutput(title=item.title, 
        content=item.content, 
        posted_on=today,
        commented= comment
    )
    diary_data = load_data()
    diary_data.append(diary.model_dump())
    save_data(diary_data)
    return JSONResponse(content={"message": "投稿完了！"})

#入力フォームの表示
@app.get("/form", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("form.html", context)
#diary一覧の表示
@app.get("/list", response_class=HTMLResponse)
async def show_list(request: Request):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return templates.TemplateResponse("list.html", {"request": request, "diaries": data})

#表情管理
@app.get("/get_expression")
async def get_expression():
    # 今はランダムだけど、あとでGPT連携もOK！
    import random
    return {"expression": random.choice(["happy", "sad", "fight","serious"])}

#api説明ページ
@app.get("/")
def home():
    return {"message": "このサイトは日記投稿APIです。"}

#jsonをそのまま取得
@app.get("/diaries")
def get_diary():
    with open(filename,"r",encoding="utf-8") as f:
        data= json.load(f)
    return data
