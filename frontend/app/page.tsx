"use client";

import { useState } from "react";
import { Send, Bot, User, Award, GraduationCap } from "lucide-react";

// تعریف ساختار پیام‌ها
type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

export default function ChatPage() {
  const [level, setLevel] = useState<"Beginner" | "Advanced">("Beginner");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // تابع اصیل، دستی و قدرتمند ما برای ارسال پیام
  const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // ۱. اضافه کردن پیام کاربر به صفحه
    const userMsg: Message = { id: Date.now().toString(), role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      // ۲. تماس مستقیم و بدون واسطه با بک‌اند خودمان
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [...messages, userMsg],
          level: level,
        }),
      });

      const data = await response.json();

      // ۳. اضافه کردن پیام هوش مصنوعی به صفحه
      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.content || data.response || "پاسخی دریافت نشد.",
      };
      setMessages((prev) => [...prev, assistantMsg]);
      
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { id: Date.now().toString(), role: "assistant", content: "⚠️ خطایی در ارتباط با سرور رخ داد." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-100 font-sans">
      {/* هدر */}
      <header className="flex items-center justify-between px-6 py-4 bg-slate-900 border-b border-slate-800 shrink-0">
        <div className="flex items-center gap-3">
          <Bot className="w-8 h-8 text-blue-500" />
          <div>
            <h1 className="text-lg font-bold">دستیار آموزشی هوشمند برنامه‌نویسی</h1>
            <p className="text-xs text-slate-400">طراحی شده با Next.js و پایتون</p>
          </div>
        </div>

        <div className="flex items-center gap-2 bg-slate-800 p-1 rounded-lg border border-slate-700">
          <button
            onClick={() => setLevel("Beginner")}
            className={`flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
              level === "Beginner" ? "bg-blue-600 text-white shadow-md" : "text-slate-400 hover:text-white"
            }`}
          >
            <GraduationCap className="w-4 h-4" />
            مبتدی
          </button>
          <button
            onClick={() => setLevel("Advanced")}
            className={`flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
              level === "Advanced" ? "bg-indigo-600 text-white shadow-md" : "text-slate-400 hover:text-white"
            }`}
          >
            <Award className="w-4 h-4" />
            پیشرفته
          </button>
        </div>
      </header>

      {/* بخش چت‌ها */}
      <main className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-slate-500 gap-2">
            <Bot className="w-12 h-12 text-slate-700 animate-pulse" />
            <p>سوالی درباره کوییز، نقشه راه، کدنویسی یا بررسی پروژه گیت‌هاب بپرسید...</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 max-w-3xl ${
                message.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                  message.role === "user" ? "bg-blue-600" : "bg-slate-800 border border-slate-700"
                }`}
              >
                {message.role === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4 text-blue-400" />}
              </div>
              <div
                className={`p-4 rounded-2xl leading-relaxed text-sm ${
                  message.role === "user"
                    ? "bg-blue-600/90 text-white rounded-tr-none"
                    : "bg-slate-900 border border-slate-800 rounded-tl-none whitespace-pre-wrap"
                }`}
              >
                {message.content}
              </div>
            </div>
          ))
        )}

        {/* انیمیشن لودینگ */}
        {isLoading && (
          <div className="flex gap-3 max-w-3xl mr-auto">
             <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 text-slate-400 animate-pulse" />
             </div>
             <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 rounded-tl-none text-slate-400 text-sm animate-pulse">
                در حال تفکر و پردازش...
             </div>
          </div>
        )}
      </main>

      {/* فرم ارسال */}
      <footer className="p-4 bg-slate-900 border-t border-slate-800 shrink-0">
        <form onSubmit={handleFormSubmit} className="flex gap-2 max-w-4xl mx-auto">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="سوال خود را بپرسید..."
            disabled={isLoading}
            className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500 text-slate-100 placeholder:text-slate-600 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-500 text-white p-3 rounded-xl transition-all flex items-center justify-center shrink-0 shadow-md disabled:bg-slate-800 disabled:text-slate-600"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </footer>
    </div>
  );
}