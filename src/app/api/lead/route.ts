import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

// Telegram-уведомления о новых заявках.
// Настройте через @BotFather: создайте бота, получите токен и chat_id.
// Запишите в переменные окружения TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID.
async function notifyTelegram(lead: {
  name: string;
  phone: string;
  service: string;
  address: string | null;
  comment: string | null;
}) {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) return; // тихо пропускаем, если не настроено

  const text =
    `🟢 Новая заявка с сайта\n\n` +
    `👤 Имя: ${lead.name}\n` +
    `📞 Телефон: ${lead.phone}\n` +
    `🛠 Услуга: ${lead.service}\n` +
    (lead.address ? `📍 Адрес: ${lead.address}\n` : "") +
    (lead.comment ? `💬 Комментарий: ${lead.comment}\n` : "") +
    `\n⏰ ${new Date().toLocaleString("ru-RU", { timeZone: "Europe/Samara" })}`;

  try {
    await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chatId, text, parse_mode: "HTML" }),
    });
  } catch {
    // не критично — заявка уже сохранена в БД
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const name = String(body.name || "").trim();
    const phone = String(body.phone || "").trim();
    const service = String(body.service || "Чистка жироуловителя").trim();
    const address = body.address ? String(body.address).trim() : null;
    const comment = body.comment ? String(body.comment).trim() : null;

    if (!name || name.length < 2) {
      return NextResponse.json({ ok: false, error: "Укажите имя" }, { status: 400 });
    }
    if (!phone || phone.replace(/\D/g, "").length < 10) {
      return NextResponse.json({ ok: false, error: "Укажите корректный телефон" }, { status: 400 });
    }

    const lead = await db.lead.create({
      data: { name, phone, service, address, comment },
    });

    // Отправляем уведомление в Telegram (не блокируем ответ клиенту)
    notifyTelegram({ name, phone, service, address, comment }).catch(() => {});

    return NextResponse.json({ ok: true, id: lead.id });
  } catch (err) {
    console.error("lead error", err);
    return NextResponse.json({ ok: false, error: "Не удалось сохранить заявку" }, { status: 500 });
  }
}

export async function GET() {
  try {
    const leads = await db.lead.findMany({ orderBy: { createdAt: "desc" }, take: 50 });
    return NextResponse.json({ ok: true, leads });
  } catch {
    return NextResponse.json({ ok: true, leads: [] });
  }
}
