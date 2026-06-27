import os
import sys
import importlib

print("🔍 [سیستم عیب‌یابی لانگ‌چین] در حال بررسی محیط پایتون شما...\n")

# ۱. بررسی نسخه پایتون ترمینال
print(f"🐍 نسخه پایتون فعال در ترمینال: {sys.version}")
print(f"📂 مسیر مفسر پایتون: {sys.executable}\n")

# ۲. لیست پکیج‌هایی که باید بررسی شوند
packages = [
    "pydantic",
    "pydantic_core",
    "langchain_core",
    "langchain_openai",
    "langchain",
    "langchain_community" # این پکیج بسیار مهم است و ابزارهای قدیمی مثل initialize_agent در آن است
]

print("--- وضعیت پکیج‌های نصب شده ---")
for pkg in packages:
    try:
        module = importlib.import_module(pkg)
        version = getattr(module, "__version__", "نامشخص")
        path = getattr(module, "__file__", "بدون فایل مستقیم")
        print(f"✅ پکیج {pkg} نصب است. نسخه: {version}")
        print(f"   مسیر نصب: {path}\n")
    except ImportError as e:
        print(f"❌ پکیج {pkg} نصب نیست یا خراب است! خطا: {e}\n")

print("--- تست وارد کردن (Import) مستقیم توابع ایجنت ---")
try:
    import langchain.agents
    print("✅ ماژول langchain.agents با موفقیت لود شد.")
    print(f"📂 مسیر فایل ماژول ایجنت: {langchain.agents.__file__}")
    
    # بررسی توابع موجود در این پوشه
    attributes = dir(langchain.agents)
    print("\n📦 لیست دستوراتی که در langchain.agents شما وجود دارند:")
    available_funcs = [attr for attr in attributes if not attr.startswith("_")]
    print(", ".join(available_funcs))
    
    # تست نهایی ایمپورت
    from langchain.agents import initialize_agent
    print("\n✅ تست نهایی موفقیت‌آمیز بود! initialize_agent بدون مشکل لود شد.")
    
except ImportError as e:
    print(f"\n❌ شکست در ایمپورت ایجنت! علت اصلی خطا:")
    print(f"   {type(e).__name__}: {e}")