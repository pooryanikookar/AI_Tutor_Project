import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    // ۱. دریافت اطلاعات ارسالی از سمت سایت (فایل page.tsx)
    const { messages, level } = await req.json();
    
    // ۲. استخراج آخرین سوال کاربر
    const latestMessage = messages[messages.length - 1].content;
    const selectedLevel = level || "Beginner";

    // ۳. ارسال درخواست مستقیم به سرور پایتون (FastAPI) روی پورت ۸۰۰۰
    const response = await fetch("http://127.0.0.1:8000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: latestMessage,
        level: selectedLevel,
        history: messages.slice(0, -1).map((m: any) => ({
          role: m.role,
          content: m.content,
        })),
        context: {},
      }),
    });

    // بررسی اینکه آیا پایتون اروری داده است یا خیر
    if (!response.ok) {
      const errorText = await response.text();
      console.error("خطا از سمت پایتون:", errorText);
      throw new Error("وب‌سرور پایتون پاسخ نداد یا خطایی داشت.");
    }

    // ۴. دریافت جواب پایتون
    const result = await response.json();

    // ۵. بازگرداندن جواب به سمت سایت (page.tsx)
    return NextResponse.json({
      content: result.response,
    });
    
  } catch (error: any) {
    console.error("خطا در فایل route.ts:", error.message);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}