from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os
import requests # کتابخانه پایتون برای ارسال درخواست به اینترنت

# ساخت مدل جی‌پی‌تی برای داخل ابزارها
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    base_url="https://api.metisai.ir/openai/v1"
)

# ---------------------------------------------------------
# ۱. ابزار تولید کد (Code Generator Tool) - ۱۰ نمره
# ---------------------------------------------------------
@tool
def generate_code(topic: str) -> str:
    """
    Use this tool when the user asks to generate code, write a script, or wants a programming example.
    Input should be the topic or description of the code needed.
    """
    prompt = f"یک کد تمیز و خوانای پایتون به همراه توضیحات فارسی ساده برای این موضوع بنویس: {topic}"
    response = llm.invoke(prompt)
    return response.content

# ---------------------------------------------------------
# ۲. ابزار ساخت کوییز (Quiz Generator Tool) - ۱۰ نمره
# ---------------------------------------------------------
@tool
def generate_quiz(topic: str) -> str:
    """
    Use this tool when the user asks for a quiz, test, or questions about a specific topic.
    Input should be the subject of the quiz.
    """
    prompt = f"یک کوییز ۳ سوالی تستی (چند گزینه‌ای) به زبان فارسی به همراه پاسخ صحیح درباره این موضوع بساز: {topic}"
    response = llm.invoke(prompt)
    return response.content

# ---------------------------------------------------------
# ۳. ابزار طراح مسیر یادگیری (Learning Roadmap Tool) - ۱۰ نمره
# ---------------------------------------------------------
@tool
def generate_roadmap(role: str) -> str:
    """
    Use this tool when the user asks for a learning roadmap, career path, or how to become a specific role.
    Input should be the target role (e.g., Backend Developer).
    """
    prompt = f"یک مسیر یادگیری قدم به قدم و فازبندی شده به زبان فارسی برای تبدیل شدن به {role} طراحی کن."
    response = llm.invoke(prompt)
    return response.content

# ---------------------------------------------------------
# ۴. ابزار بررسی گیت‌هاب (GitHub Review Tool) - ۱۵ نمره
# ---------------------------------------------------------
@tool
def review_github_repo(repo_url: str) -> str:
    """
    Use this tool when the user wants to review a GitHub repository or project and get feedback.
    Input should be the full GitHub repository URL (e.g., https://github.com/owner/repo).
    """
    try:
        # ۱. تجزیه آدرس گیت‌هاب برای به دست آوردن نام مالک و نام پروژه
        parts = repo_url.strip("/").split("/")
        if len(parts) < 5:
            return "❌ خطا: آدرس گیت‌هاب معتبر نیست. لطفا آدرس کامل مخزن را وارد کنید."
        
        owner = parts[3]
        repo = parts[4]

        # ۲. تنظیم توکن گیت‌هاب برای دور زدن محدودیت دانلود
        token = os.getenv("GITHUB_TOKEN")
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"

        # ۳. تماس با API گیت‌هاب برای گرفتن لیست فایل‌ها
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        api_response = requests.get(api_url, headers=headers)
        
        if api_response.status_code != 200:
            return f"❌ خطا در اتصال به گیت‌هاب: {api_response.json().get('message', 'کد وضعیت ' + str(api_response.status_code))}"

        files_data = api_response.json()
        file_names = [f["name"] for f in files_data] # لیست نام فایل‌ها

        # ۴. تلاش برای خواندن فایل اصلی پروژه (مثل README یا فایل‌های پایتونی)
        main_file_content = "محتوایی یافت نشد."
        for file_info in files_data:
            if file_info["name"].lower() in ["readme.md", "main.py", "app.py"]:
                file_response = requests.get(file_info["download_url"], headers=headers)
                if file_response.status_code == 200:
                    main_file_content = file_response.text[:1500] # محدود کردن حجم متن برای صرفه‌جویی در هزینه
                    break

        # ۵. فرستادن اطلاعات به هوش مصنوعی برای نقد و بررسی
        prompt = f"""
        شما یک مهندس نرم‌افزار ارشد هستید. لطفا پروژه گیت‌هاب زیر را بررسی کنید و بازخورد ساختاریافته، دقیق و به زبان فارسی ارائه دهید.
        
        نام پروژه: {repo}
        لیست فایل‌های موجود: {', '.join(file_names)}
        محتوای فایل اصلی پروژه:
        {main_file_content}
        
        لطفا در پاسخ خود موارد زیر را پوشش دهید:
        1. تحلیل ساختار فایل‌ها (آیا مرتب است؟)
        2. نقاط قوت پروژه
        3. نقاط ضعف و پیشنهاداتی برای بهبود کدها و ساختار
        """
        review_response = llm.invoke(prompt)
        return review_response.content

    except Exception as e:
        return f"❌ خطا در اجرای ابزار بررسی گیت‌هاب: {str(e)}"


# لیست تمام ابزارهای ما (حالا شد ۴ ابزار)
ai_tutor_tools = [generate_code, generate_quiz, generate_roadmap, review_github_repo]