import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# دقت کنید: در این کدهای جدید هیچ اثری از langchain.agents نیست!
from tools import ai_tutor_tools, generate_code, generate_quiz, generate_roadmap, review_github_repo

load_dotenv()

# ۱. ساخت مغز هوش مصنوعی
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    base_url="https://api.metisai.ir/openai/v1"
)

# ۲. اتصال مستقیم و مدرن ابزارها (بدون Agent قدیمی)
llm_with_tools = llm.bind_tools(ai_tutor_tools)

# ۳. کتابچه راهنمای ابزارها
tools_map = {
    "generate_code": generate_code,
    "generate_quiz": generate_quiz,
    "generate_roadmap": generate_roadmap,
    "review_github_repo": review_github_repo
}

# ۴. میدل‌ور خلاصه‌سازی
def summarize_chat_history(chat_history: list) -> str:
    if not chat_history or len(chat_history) < 4:
        return ""
    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
    summary_prompt = f"لطفاً مکالمه زیر را در دو جمله کوتاه به زبان فارسی خلاصه کن تا به عنوان حافظه استفاده شود:\n\n{history_text}"
    response = llm.invoke(summary_prompt)
    return response.content

# ۵. تابع اصلی ایجنت
def run_ai_tutor(
    user_question: str, 
    student_level: str = "Beginner", 
    user_context: dict = None,
    chat_history: list = None
) -> str:
    
    level_rules = {
        "Beginner": "توضیحات بسیار ساده، با مثال‌های ملموس، فاقد اصطلاحات پیچیده و به فارسی ارائه دهید.",
        "Intermediate": "توضیحات متعادل با جزئیات فنی متوسط ارائه دهید.",
        "Advanced": "توضیحات کاملاً فنی، عمیق و تخصصی بنویسید."
    }
    
    context_instruction = ""
    if user_context:
        context_instruction = (
            f"\n[اطلاعات بستر کاربر]:\n"
            f"- تکنولوژی‌های موردعلاقه کاربر: {user_context.get('fav_tech', 'مشخص نیست')}\n"
            f"- موضوعات مطالعه شده تا الان: {user_context.get('studied_topics', 'مشخص نیست')}\n"
            f"- مسیر یادگیری فعلی: {user_context.get('current_roadmap', 'مشخص نیست')}\n"
        )

    summary_instruction = ""
    if chat_history and len(chat_history) >= 4:
        chat_summary = summarize_chat_history(chat_history)
        summary_instruction = f"\n[خلاصه مکالمات قبلی شما با این کاربر]:\n{chat_summary}\n"

    system_message = (
        "شما یک دستیار هوشمند آموزش برنامه‌نویسی هستی. همیشه با لحن دوستانه و فارسی جواب بده. "
        f"قانون سطح کاربر: {level_rules.get(student_level, 'Beginner')}\n"
        f"{context_instruction}"
        f"{summary_instruction}"
    )
    
    full_prompt = f"{system_message}\n\nسوال کاربر: {user_question}"
    response = llm_with_tools.invoke(full_prompt)
    
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        if tool_name in tools_map:
            actual_tool_function = tools_map[tool_name]
            tool_result = actual_tool_function.invoke(tool_args)
            return tool_result
            
    return response.content