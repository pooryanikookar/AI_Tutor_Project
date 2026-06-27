from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from agent import run_ai_tutor # فراخوانی مغز هوش مصنوعی

app = FastAPI(title="AI Tutor Backend API")

# باز کردن دسترسی CORS برای اتصال فرانت‌اند
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ۱. ساخت ساختار داده کاربر با استفاده از Pydantic (میدل‌ور و گاردلاین ورودی)
# این مدل مشخص می‌کند که ورودی‌های ما دقیقاً باید چه فرمتی داشته باشند
class ChatRequest(BaseModel):
    question: str
    level: str = "Beginner"
    history: List[Dict] = []
    context: Dict = {}

# ۲. آدرس ارتباطی برای چت
@app.post("/api/chat")
# به جای دریافت خام اطلاعات، مستقیماً کلاس ChatRequest را تحویل می‌گیریم
async def chat_endpoint(request_data: ChatRequest):
    
    # فراخوانی تابع اصلی اِیجنت با داده‌های معتبر شده توسط Pydantic
    ai_response = run_ai_tutor(
        user_question=request_data.question,
        student_level=request_data.level,
        user_context=request_data.context,
        chat_history=request_data.history
    )
    
    return {"response": ai_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)