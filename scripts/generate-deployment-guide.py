#!/usr/bin/env python3
"""Generate PDF deployment guide for the ЖИРОЧИСТ Самара website."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, ListFlowable, ListItem, Image, Flowable,
)
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate
from reportlab.platypus.frames import Frame
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# Register Liberation Sans (has Cyrillic)
font_paths = {
    "LSans": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "LSans-Bold": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "LSans-Italic": "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
    "LSans-BoldItalic": "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
}
for name, path in font_paths.items():
    if os.path.exists(path):
        pdfmetrics.registerFont(TTFont(name, path))

registerFontFamily(
    "LSans", normal="LSans", bold="LSans-Bold",
    italic="LSans-Italic", boldItalic="LSans-BoldItalic",
)

# Eco-green palette (matches website)
PRIMARY = colors.HexColor("#0E5C3A")
ACCENT = colors.HexColor("#2D8659")
ACCENT_LIGHT = colors.HexColor("#C8E6C9")
BG = colors.HexColor("#FAF6EC")
SURFACE = colors.HexColor("#EDF5F2")
TEXT = colors.HexColor("#1A1F1C")
MUTED = colors.HexColor("#5C6A5F")
BORDER = colors.HexColor("#D8E0D3")
CODE_BG = colors.HexColor("#F1EDE1")

# Styles
ss = getSampleStyleSheet()

style_title = ParagraphStyle(
    "Title", parent=ss["Title"], fontName="LSans-Bold",
    fontSize=28, leading=34, textColor=PRIMARY, alignment=TA_LEFT,
    spaceBefore=0, spaceAfter=8,
)
style_subtitle = ParagraphStyle(
    "Subtitle", parent=ss["Normal"], fontName="LSans",
    fontSize=14, leading=18, textColor=MUTED, alignment=TA_LEFT,
    spaceBefore=0, spaceAfter=20,
)
style_h1 = ParagraphStyle(
    "H1", parent=ss["Heading1"], fontName="LSans-Bold",
    fontSize=18, leading=22, textColor=PRIMARY,
    spaceBefore=24, spaceAfter=10,
)
style_h2 = ParagraphStyle(
    "H2", parent=ss["Heading2"], fontName="LSans-Bold",
    fontSize=14, leading=18, textColor=ACCENT,
    spaceBefore=16, spaceAfter=6,
)
style_h3 = ParagraphStyle(
    "H3", parent=ss["Heading3"], fontName="LSans-Bold",
    fontSize=12, leading=15, textColor=PRIMARY,
    spaceBefore=10, spaceAfter=4,
)
style_body = ParagraphStyle(
    "Body", parent=ss["Normal"], fontName="LSans",
    fontSize=10.5, leading=15, textColor=TEXT, alignment=TA_JUSTIFY,
    spaceBefore=0, spaceAfter=6,
)
style_bullet = ParagraphStyle(
    "Bullet", parent=style_body, leftIndent=14, spaceAfter=3,
)
style_code = ParagraphStyle(
    "Code", parent=ss["Code"], fontName="Courier",
    fontSize=9, leading=12, textColor=TEXT,
    backColor=CODE_BG, borderColor=BORDER, borderWidth=0.5,
    borderPadding=6, leftIndent=0, rightIndent=0,
    spaceBefore=6, spaceAfter=6,
)
style_note = ParagraphStyle(
    "Note", parent=style_body, fontName="LSans-Italic",
    textColor=MUTED, fontSize=10, leading=14,
    leftIndent=10, rightIndent=10,
    backColor=SURFACE, borderColor=ACCENT, borderWidth=0,
    borderPadding=8, spaceBefore=8, spaceAfter=8,
)
style_step_num = ParagraphStyle(
    "StepNum", parent=ss["Normal"], fontName="LSans-Bold",
    fontSize=22, leading=24, textColor=ACCENT, alignment=TA_CENTER,
)
style_step_title = ParagraphStyle(
    "StepTitle", parent=ss["Normal"], fontName="LSans-Bold",
    fontSize=12, leading=15, textColor=PRIMARY,
)
style_step_body = ParagraphStyle(
    "StepBody", parent=style_body, fontSize=10.5, leading=14,
)
style_cover_label = ParagraphStyle(
    "CoverLabel", parent=ss["Normal"], fontName="LSans-Bold",
    fontSize=10, leading=12, textColor=ACCENT, alignment=TA_LEFT,
)
style_cover_title = ParagraphStyle(
    "CoverTitle", parent=ss["Title"], fontName="LSans-Bold",
    fontSize=34, leading=40, textColor=PRIMARY, alignment=TA_LEFT,
    spaceAfter=12,
)
style_cover_sub = ParagraphStyle(
    "CoverSub", parent=ss["Normal"], fontName="LSans",
    fontSize=14, leading=20, textColor=MUTED, alignment=TA_LEFT,
)
style_cover_meta = ParagraphStyle(
    "CoverMeta", parent=ss["Normal"], fontName="LSans",
    fontSize=11, leading=16, textColor=TEXT, alignment=TA_LEFT,
)


def P(text, style=style_body):
    return Paragraph(text, style)


def code_block(text):
    """Render a code block with line breaks preserved."""
    lines = text.strip().split("\n")
    # Escape HTML-special chars
    escaped = "<br/>".join(
        line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
        for line in lines
    )
    return Paragraph(escaped, style_code)


def step_box(num, title, body_paragraphs):
    """A step box with number on the left and content on the right."""
    content = [P(title, style_step_title), Spacer(1, 4)]
    for p in body_paragraphs:
        if isinstance(p, str):
            content.append(P(p, style_step_body))
        else:
            content.append(p)
    tbl = Table(
        [[P(str(num), style_step_num), content]],
        colWidths=[16 * mm, 150 * mm],
    )
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, 0), SURFACE),
        ("BACKGROUND", (1, 0), (1, 0), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (0, 0), 8),
        ("BOTTOMPADDING", (0, 0), (0, 0), 8),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("RIGHTPADDING", (1, 0), (1, 0), 10),
        ("TOPPADDING", (1, 0), (1, 0), 8),
        ("BOTTOMPADDING", (1, 0), (1, 0), 8),
    ]))
    return KeepTogether([tbl, Spacer(1, 8)])


def options_table():
    data = [
        [P("<b>Вариант</b>", style_step_body), P("<b>Цена/мес</b>", style_step_body),
         P("<b>Сложность</b>", style_step_body), P("<b>Для кого</b>", style_step_body)],
        ["Vercel + Neon", "0 ₽", "⭐ низкая", "Готовы потратить час на регистрацию"],
        ["Timeweb VPS", "250–400 ₽", "⭐⭐ средняя", "Самый надёжный для России"],
        ["Beget / Reg.ru", "200–500 ₽", "⭐⭐ средняя", "Простой российский вариант"],
    ]
    # Wrap text cells in Paragraph for proper wrapping
    for i in range(1, len(data)):
        for j in range(len(data[i])):
            if isinstance(data[i][j], str):
                data[i][j] = P(data[i][j], style_step_body)

    tbl = Table(data, colWidths=[40 * mm, 28 * mm, 35 * mm, 63 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "LSans-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SURFACE]),
        ("BOX", (0, 0), (-1, -1), 0.5, ACCENT),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
    ]))
    return tbl


def page_footer(canvas, doc):
    """Footer on body pages."""
    canvas.saveState()
    canvas.setFillColor(MUTED)
    canvas.setFont("LSans", 9)
    page_num = canvas.getPageNumber()
    if page_num > 1:  # skip cover
        canvas.drawCentredString(A4[0] / 2, 15 * mm, str(page_num - 1))
        canvas.setFont("LSans", 8)
        canvas.drawString(20 * mm, 15 * mm, "ЖИРОЧИСТ Самара · Инструкция по запуску сайта")
    canvas.restoreState()


def cover_canvas(canvas, doc):
    """Draw cover page background."""
    w, h = A4
    canvas.saveState()
    # Full-page dark green background
    canvas.setFillColor(colors.HexColor("#0C1F1A"))
    canvas.rect(0, 0, w, h, fill=1, stroke=0)

    pad_l = 40
    # Top accent line
    canvas.setStrokeColor(colors.HexColor("#2D8659"))
    canvas.setLineWidth(2)
    canvas.line(pad_l, h - 100, w - 40, h - 100)

    # Label
    canvas.setFillColor(colors.HexColor("#3DDBB5"))
    canvas.setFont("LSans-Bold", 10)
    canvas.drawString(pad_l, h - 90, "I N S T R U C T I O N   2 0 2 6")

    # Title
    canvas.setFillColor(colors.white)
    canvas.setFont("LSans-Bold", 36)
    canvas.drawString(pad_l, h - 200, "Инструкция")
    canvas.drawString(pad_l, h - 245, "по запуску сайта")

    # Subtitle
    canvas.setFillColor(colors.HexColor("#B0B8C0"))
    canvas.setFont("LSans", 16)
    canvas.drawString(pad_l, h - 285, "ЖИРОЧИСТ Самара — сайт-визитка")

    # Meta info with left accent border
    canvas.setStrokeColor(colors.HexColor("#3DDBB5"))
    canvas.setLineWidth(3)
    meta_y = h - 360
    meta_lines = [
        "Подробное руководство по развёртыванию",
        "на хостинге для самозанятого",
        "без опыта программирования",
    ]
    canvas.setFillColor(colors.HexColor("#B0B8C0"))
    canvas.setFont("LSans", 12)
    for i, line in enumerate(meta_lines):
        y = meta_y - i * 22
        canvas.line(pad_l, y - 4, pad_l, y + 12)
        canvas.drawString(pad_l + 14, y, line)

    # Footer
    canvas.setStrokeColor(colors.HexColor("#2D8659"))
    canvas.setLineWidth(1)
    canvas.line(pad_l, 70, w - 40, 70)
    canvas.setFillColor(colors.HexColor("#90989F"))
    canvas.setFont("LSans", 9)
    canvas.drawString(pad_l, 55, "ЖИРОЧИСТ Самара")
    canvas.drawRightString(w - 40, 55, "Самара · 2026")
    canvas.restoreState()


def build():
    out = "/home/z/my-project/download/Инструкция_по_запуску_сайта.pdf"

    doc = BaseDocTemplate(
        out, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=22 * mm,
        title="Инструкция по запуску сайта ЖИРОЧИСТ Самара",
        author="ЖИРОЧИСТ Самара",
        subject="Руководство по развёртыванию сайта-визитки",
    )

    # Cover page template (full bleed, no margins)
    cover_frame = Frame(0, 0, A4[0], A4[1], leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="cover")
    cover_template = PageTemplate(id="Cover", frames=[cover_frame], onPage=cover_canvas)

    # Body page template (with margins and footer)
    body_frame = Frame(
        20 * mm, 22 * mm,
        A4[0] - 40 * mm, A4[1] - 42 * mm,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        id="body",
    )
    body_template = PageTemplate(id="Body", frames=[body_frame], onPage=page_footer)

    doc.addPageTemplates([cover_template, body_template])

    story = []

    # === COVER === (empty flowable that triggers cover template)
    from reportlab.platypus.doctemplate import NextPageTemplate
    story.append(NextPageTemplate("Body"))
    story.append(PageBreak())

    # === INTRO ===
    story.append(P("Введение", style_h1))
    story.append(P(
        "Эта инструкция описывает, как выложить готовый сайт-визитку ЖИРОЧИСТ Самара в интернет. "
        "Сайт уже спроектирован и работает в песочнице — осталось выбрать хостинг, зарегистрировать домен "
        "и подключить несколько сервисов. Все шаги расписаны подробно, без предположений о технических знаниях."
    ))
    story.append(P(
        "Сайт сделан на современном стеке Next.js + Tailwind CSS + Prisma. Это значит, что для запуска нужен "
        "хостинг с поддержкой Node.js — обычный shared-хостинг за 100 ₽/мес не подойдёт. Ниже описаны три "
        "варианта, проверенных для российских пользователей."
    ))

    story.append(P("Три варианта запуска", style_h2))
    story.append(options_table())
    story.append(Spacer(1, 12))
    story.append(P(
        "Дальше в инструкции подробно разобран Вариант 2 (Timeweb VPS) — он оптимален по соотношению "
        "цены, надёжности и простоты для России. Варианты 1 и 3 описаны кратко в конце."
    ))

    # === WHAT YOU NEED ===
    story.append(P("Что понадобится заранее", style_h1))
    story.append(P("Перед началом работ подготовьте:", style_body))
    items = [
        "Паспортные данные — для регистрации домена .ru или .рф (требование Роскомнадзора).",
        "Действующий номер телефона — для подтверждения регистратора домена и хостинга.",
        "Электронная почта — лучше Яндекс или Mail.ru, не Google (могут быть проблемы с доступом).",
        "Telegram-аккаунт — для создания бота, который будет присылать уведомления о заявках.",
        "30–60 минут времени на каждый шаг (регистрация, настройки, проверка).",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    # === PART 1: GET THE CODE ===
    story.append(P("Часть 1. Получить исходный код сайта", style_h1))
    story.append(P(
        "Исходный код сайта находится в проекте. Его нужно скачать на компьютер в виде ZIP-архива, "
        "а затем загрузить на хостинг или в GitHub."
    ))

    story.append(step_box(1, "Скачайте ZIP-архив проекта",
        [
            "В интерфейсе песочницы нажмите кнопку «Скачать проект» или «Download» в правом верхнем углу. "
            "Получится файл размером около 5–10 МБ. Сохраните его в отдельную папку, например "
            "<font face='Courier'>C:\\Users\\Имя\\zhirochist-site</font>.",
            "Если кнопки скачивания нет — попросите администратора платформы выгрузить проект.",
        ]))

    story.append(step_box(2, "Зарегистрируйтесь на GitHub (опционально, но удобно)",
        [
            "GitHub — это бесплатный сервис для хранения кода. Аккаунт позволит в будущем обновлять сайт "
            "и автоматически выкатывать изменения.",
            "Откройте <font face='Courier'>github.com</font>, нажмите Sign up, придумайте логин и пароль. "
            "Подтвердите email.",
            "Создайте новый репозиторий: кнопка «New», имя <font face='Courier'>zhirochist-site</font>, "
            "Private (приватный). Нажмите «Create repository».",
        ]))

    story.append(step_box(3, "Установите Git и загрузите код в GitHub (опционально)",
        [
            "Скачайте Git с <font face='Courier'>git-scm.com</font>, установите с настройками по умолчанию.",
            "Распакуйте ZIP-архив проекта в папку. В этой папке нажмите правой кнопкой мыши → «Open Git Bash here» "
            "(или «Открыть терминал» в Windows 11).",
            "Выполните команды (замените YOUR-USERNAME на ваш логин GitHub):",
        ]))
    story.append(code_block(
        "git init\ngit add .\ngit commit -m \"first commit\"\ngit branch -M main\ngit remote add origin https://github.com/YOUR-USERNAME/zhirochist-site.git\ngit push -u origin main"
    ))
    story.append(P(
        "Если хотите пропустить GitHub — можно просто загрузить ZIP напрямую на сервер (см. ниже).",
        style_note
    ))

    # === PART 2: VPS TIMWEB ===
    story.append(PageBreak())
    story.append(P("Часть 2. Регистрация VPS на Timeweb Cloud", style_h1))
    story.append(P(
        "Timeweb Cloud — российский облачный провайдер с серверами в Москве и Санкт-Петербурге. "
        "Подходит для Next.js, поддерживает оплату с российской карты. Цена от 250 ₽/мес за сервер "
        "с подходящими характеристиками."
    ))

    story.append(step_box(1, "Зарегистрируйтесь на Timeweb Cloud",
        [
            "Откройте <font face='Courier'>timeweb.cloud</font>. Нажмите «Регистрация» в правом верхнем углу.",
            "Укажите email, придумайте пароль. Подтвердите по ссылке из письма.",
            "В личном кабинете выберите «Облачные серверы» → «Создать сервер».",
        ]))

    story.append(step_box(2, "Создайте сервер с параметрами",
        [
            "Выберите конфигурацию:",
            "• <b>Процессор:</b> 2 ядра (vCPU)",
            "• <b>Оперативная память:</b> 2 ГБ RAM",
            "• <b>Диск:</b> 20 ГБ SSD",
            "• <b>Операционная система:</b> Ubuntu 22.04 LTS",
            "• <b>Регион:</b> Москва (или Санкт-Петербург)",
            "Цена такого сервера — около 300 ₽/мес. Для одного сайта этого хватит с запасом.",
        ]))

    story.append(step_box(3, "Сохраните IP-адрес и пароль сервера",
        [
            "После создания сервера в личном кабинете появится его IP-адрес вида "
            "<font face='Courier'>45.142.122.18</font> и root-пароль. Запишите их в надёжное место.",
            "Пароль также придёт на email.",
        ]))

    # === PART 3: SETUP SERVER ===
    story.append(P("Часть 3. Настройка сервера", style_h1))
    story.append(P(
        "Далее идёт работа в терминале сервера. Это чёрное окно с командами. Не пугайтесь — "
        "команды можно копировать отсюда и вставлять."
    ))

    story.append(step_box(1, "Подключитесь к серверу по SSH",
        [
            "На Windows 10/11 откройте PowerShell или командную строку (Win+R → cmd). На Mac/Linux — Terminal.",
            "Подключитесь командой (замените IP на свой):",
        ]))
    story.append(code_block("ssh root@45.142.122.18"))
    story.append(P(
        "При первом подключении напишите <font face='Courier'>yes</font> и нажмите Enter. "
        "Затем введите пароль (при вводе символы не видны — это нормально)."
    ))

    story.append(step_box(2, "Установите Node.js 20 и Bun",
        [
            "Выполните по очереди команды (копируйте и вставляйте в терминал):",
        ]))
    story.append(code_block(
        "curl -fsSL https://deb.nodesource.com/setup_20.x | bash -\napt install -y nodejs git nginx\nnpm install -g bun pm2"
    ))
    story.append(P(
        "После установки проверьте, что всё работает: <font face='Courier'>node -v</font> должно показать "
        "v20.x.x, <font face='Courier'>bun -v</font> — версию 1.x.x."
    ))

    story.append(step_box(3, "Загрузите код сайта на сервер",
        [
            "Самый простой способ — клонировать с GitHub (если вы его создавали):",
        ]))
    story.append(code_block(
        "cd /var/www\ngit clone https://github.com/YOUR-USERNAME/zhirochist-site.git zhirochist\ncd zhirochist"
    ))
    story.append(P(
        "Если GitHub не использовали — загрузите ZIP-архив через SCP или файловый менеджер Timeweb "
        "(вкладка «Файлы» в личном кабинете)."
    ))

    story.append(step_box(4, "Установите зависимости и соберите сайт",
        [
            "В папке проекта выполните:",
        ]))
    story.append(code_block(
        "bun install\nbun run db:push\nbun run build"
    ))
    story.append(P(
        "Сборка займёт 2–5 минут. В конце должно появиться сообщение об успехе без красных ошибок."
    ))

    story.append(step_box(5, "Запустите сайт через PM2",
        [
            "PM2 — это менеджер процессов, который держит сайт работающим и автоматически перезапускает "
            "его при сбое или перезагрузке сервера.",
        ]))
    story.append(code_block(
        "cd /var/www/zhirochist\npm2 start \"bun run start\" --name zhirochist\npm2 save\npm2 startup"
    ))
    story.append(P(
        "Последняя команда выведет длинную команду вида "
        "<font face='Courier'>sudo env PATH=... pm2 startup ...</font>. Скопируйте и выполните её — "
        "это включит автозапуск сайта при перезагрузке сервера."
    ))
    story.append(P(
        "Проверьте, что сайт работает внутри сервера: "
        "<font face='Courier'>curl http://localhost:3000</font> — должно вернуть HTML-код страницы."
    ))

    # === PART 4: NGINX ===
    story.append(P("Часть 4. Настройка Nginx (обратный прокси)", style_h1))
    story.append(P(
        "Сейчас сайт доступен только на порту 3000 внутри сервера. Чтобы он был доступен по стандартным "
        "портам 80 (HTTP) и 443 (HTTPS) — нужен Nginx."
    ))

    story.append(step_box(1, "Создайте конфигурацию Nginx",
        [
            "Создайте файл конфигурации:",
        ]))
    story.append(code_block("nano /etc/nginx/sites-available/zhirochist"))
    story.append(P(
        "Вставьте туда (замените <font face='Courier'>your-domain.ru</font> на ваш домен):"
    ))
    story.append(code_block(
        "server {\n    listen 80;\n    server_name your-domain.ru www.your-domain.ru;\n\n"
        "    location / {\n        proxy_pass http://localhost:3000;\n"
        "        proxy_http_version 1.1;\n        proxy_set_header Upgrade $http_upgrade;\n"
        "        proxy_set_header Connection 'upgrade';\n        proxy_set_header Host $host;\n"
        "        proxy_set_header X-Real-IP $remote_addr;\n"
        "        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n"
        "        proxy_set_header X-Forwarded-Proto $scheme;\n        proxy_cache_bypass $http_upgrade;\n"
        "    }\n}"
    ))
    story.append(P(
        "Сохраните: Ctrl+O, Enter, Ctrl+X."
    ))

    story.append(step_box(2, "Включите конфигурацию и перезапустите Nginx",
        [
            "Выполните команды:",
        ]))
    story.append(code_block(
        "ln -s /etc/nginx/sites-available/zhirochist /etc/nginx/sites-enabled/\n"
        "nginx -t\nsystemctl restart nginx"
    ))
    story.append(P(
        "Команда <font face='Courier'>nginx -t</font> должна показать «test is successful». "
        "Если есть ошибки — проверьте синтаксис конфигурационного файла."
    ))

    # === PART 5: DOMAIN + SSL ===
    story.append(P("Часть 5. Регистрация домена и HTTPS", style_h1))

    story.append(step_box(1, "Зарегистрируйте домен на reg.ru",
        [
            "Откройте <font face='Courier'>reg.ru</font>. В поиске введите желаемое имя, например "
            "<font face='Courier'>zhirochist-samara.ru</font>.",
            "Если домен свободен — добавьте в корзину и оформите. Цена .ru — около 200–300 ₽/год.",
            "При оформлении укажите реальные паспортные данные — это требование Роскомнадзора для .ru.",
            "Оплатите домен российской картой.",
        ]))

    story.append(step_box(2, "Подключите домен к серверу (DNS)",
        [
            "В личном кабинете reg.ru откройте «Домены» → ваш домен → «DNS-серверы».",
            "Если используются DNS reg.ru — добавьте A-запись:",
            "• <b>Тип:</b> A",
            "• <b>Имя (хост):</b> @",
            "• <b>Значение:</b> IP вашего сервера (например, 45.142.122.18)",
            "• <b>TTL:</b> по умолчанию",
            "Добавьте вторую запись для www:",
            "• <b>Тип:</b> A",
            "• <b>Имя (хост):</b> www",
            "• <b>Значение:</b> тот же IP сервера",
            "Сохраните. DNS-записи обновляются до 24 часов (обычно 30–60 минут).",
        ]))

    story.append(step_box(3, "Проверьте, что домен смотрит на сервер",
        [
            "Через час-два проверьте — на компьютере откройте командную строку и введите:",
        ]))
    story.append(code_block("nslookup zhirochist-samara.ru"))
    story.append(P(
        "В ответе должен появиться ваш IP сервера. Если показывает другой IP или «не найден» — "
        "подождите ещё, DNS ещё не обновился."
    ))

    story.append(step_box(4, "Установите бесплатный SSL-сертификат (HTTPS)",
        [
            "Сертификат нужен, чтобы сайт открывался по <font face='Courier'>https://</font> (с замочком). "
            "Это важно для доверия посетителей и для работы форм в некоторых браузерах.",
            "На сервере выполните:",
        ]))
    story.append(code_block(
        "apt install -y certbot python3-certbot-nginx\ncertbot --nginx -d zhirochist-samara.ru -d www.zhirochist-samara.ru"
    ))
    story.append(P(
        "Certbot спросит ваш email (для уведомлений об истечении сертификата) — укажите реальный. "
        "Согласитесь с условиями. Сертификат установится автоматически и будет продлеваться каждые 60 дней."
    ))
    story.append(P(
        "Готово! Откройте <font face='Courier'>https://zhirochist-samara.ru</font> в браузере — сайт должен работать "
        "с зелёным замочком.",
        style_note
    ))

    # === PART 6: CONTACTS + TELEGRAM ===
    story.append(P("Часть 6. Настройка контактов и Telegram-бота", style_h1))

    story.append(step_box(1, "Замените контакты на реальные",
        [
            "В файле <font face='Courier'>src/app/page.tsx</font> в начале файла найдите блок:",
        ]))
    story.append(code_block(
        "const PHONE_DISPLAY = '+7 (996) 213-52-20'\n"
        "const PHONE_TEL = '+79962135220'\n"
        "const TELEGRAM_URL = 'https://t.me/+79962135220'\n"
        "const MAX_URL = 'https://max.ru/'\n"
        "const EMAIL = 'malofeev-koss@ya.ru'"
    ))
    story.append(P(
        "Замените значения на свои реальные телефон, Telegram-ссылку, ссылку на профиль MAX и email. "
        "После изменений пересоберите и перезапустите сайт:",
    ))
    story.append(code_block("cd /var/www/zhirochist\ngit pull  # если используете GitHub\nbun run build\npm2 restart zhirochist"))

    story.append(step_box(2, "Создайте Telegram-бота для уведомлений",
        [
            "Откройте Telegram, найдите <b>@BotFather</b>, отправьте /newbot.",
            "Придумайте имя (например, «Жиро Чист Заявки») и username (например, zhirochist_leads_bot).",
            "BotFather пришлёт токен вида <font face='Courier'>7890123456:AAHxxx...xxx</font>. "
            "Сохраните его — это «пароль» вашего бота.",
        ]))

    story.append(step_box(3, "Узнайте свой chat_id",
        [
            "Напишите своему новому боту любое сообщение (например, «Привет»).",
            "Откройте в браузере ссылку (замените TOKEN на ваш токен):",
        ]))
    story.append(code_block("https://api.telegram.org/bot<TOKEN>/getUpdates"))
    story.append(P(
        "В ответе найдите строку вида <font face='Courier'>\"chat\":{\"id\": 123456789}</font>. "
        "Число 123456789 — это ваш chat_id. Запишите его."
    ))

    story.append(step_box(4, "Запишите токен и chat_id в файл окружения",
        [
            "На сервере откройте файл <font face='Courier'>.env</font>:",
        ]))
    story.append(code_block("nano /var/www/zhirochist/.env"))
    story.append(P(
        "Заполните строки (вставьте ваши значения):"
    ))
    story.append(code_block(
        "TELEGRAM_BOT_TOKEN=7890123456:AAHxxx...xxx\n"
        "TELEGRAM_CHAT_ID=123456789"
    ))
    story.append(P("Сохраните и перезапустите:", ))
    story.append(code_block("pm2 restart zhirochist"))
    story.append(P(
        "Готово! Теперь при каждой новой заявке с сайта вам в Telegram придёт сообщение с именем, "
        "телефоном и комментарием клиента.",
        style_note
    ))

    # === PART 7: ALTERNATIVES ===
    story.append(PageBreak())
    story.append(P("Часть 7. Альтернативные варианты запуска", style_h1))

    story.append(P("Вариант 1. Vercel + Neon Postgres (бесплатно)", style_h2))
    story.append(P(
        "Если хотите полностью бесплатно и готовы потратить время на регистрацию в нескольких сервисах:"
    ))
    items = [
        "Зарегистрируйтесь на <font face='Courier'>vercel.com</font> через GitHub-аккаунт.",
        "Импортируйте репозиторий с кодом сайта. Vercel автоматически определит Next.js и соберёт его.",
        "На <font face='Courier'>neon.tech</font> создайте бесплатную Postgres-базу (хватит 0.5 ГБ).",
        "В Vercel добавьте переменную окружения <font face='Courier'>DATABASE_URL</font> с подключением из Neon.",
        "Измените в <font face='Courier'>prisma/schema.prisma</font> провайдер с sqlite на postgresql.",
        "Деплой автоматически запустится при пуше в GitHub.",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))
    story.append(P(
        "<b>Минусы для России:</b> Vercel и Neon могут блокировать российские IP. Если не открывается — "
        "используйте VPN при регистрации или переходите на VPS-вариант.",
        style_note
    ))

    story.append(P("Вариант 3. Beget / Reg.ru с VPS", style_h2))
    story.append(P(
        "Beget и Reg.ru предлагают российские VPS с предустановленным Node.js. Цена от 200 ₽/мес. "
        "Шаги такие же, как в основном варианте с Timeweb — отличаются только панели управления."
    ))
    story.append(P(
        "Beget также предлагает управляемый Node.js-хостинг (без необходимости настраивать Nginx вручную). "
        "Это проще, но дороже — от 500 ₽/мес."
    ))

    # === CHECKLIST ===
    story.append(P("Часть 8. Финальный чек-лист", style_h1))
    story.append(P("Проверьте, что всё готово к работе:", style_body))

    checklist = [
        ("Сайт открывается по основному домену", "https://your-domain.ru"),
        ("Сайт открывается по www-версии", "https://www.your-domain.ru"),
        ("HTTPS работает (зелёный замочек)", "Браузер показывает «Защищено»"),
        ("Форма заявки отправляется", "Заполните форму на сайте — должно прийти в Telegram"),
        ("Telegram-бот присылает уведомление", "Проверьте после тестовой заявки"),
        ("Все контакты заменены на реальные", "Телефон, WhatsApp, Telegram, email"),
        ("SSL-сертификат установлен", "Certbot завершился успешно"),
        ("Сайт работает после перезагрузки сервера", "pm2 startup настроен"),
        ("Метаданные SEO заполнены", "Title и description отображаются в выдаче"),
    ]
    data = [[P("<b>Что проверить</b>", style_step_body), P("<b>Как проверить</b>", style_step_body)]]
    for what, how in checklist:
        data.append([P("☐ " + what, style_step_body), P(how, style_step_body)])
    tbl = Table(data, colWidths=[90 * mm, 76 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "LSans-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SURFACE]),
        ("BOX", (0, 0), (-1, -1), 0.5, ACCENT),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 16))

    # === SUPPORT ===
    story.append(P("Если что-то не работает", style_h1))
    story.append(P(
        "90 % проблем решаются перезапуском или проверкой DNS. Если что-то не работает, проверьте в этом порядке:"
    ))
    items = [
        "Сайт не открывается по домену → DNS ещё не обновился (подождите до 24 часов), либо "
        "A-запись указывает на неправильный IP.",
        "Сайт открывается, но показывает ошибку 502 → Nginx не может достучаться до Next.js. "
        "Проверьте: <font face='Courier'>pm2 status</font> — должен быть онлайн. <font face='Courier'>pm2 logs zhirochist</font> — посмотрите ошибки.",
        "Форма отправляется, но в Telegram ничего не приходит → проверьте токен и chat_id в <font face='Courier'>.env</font>, "
        "перезапустите сайт <font face='Courier'>pm2 restart zhirochist</font>.",
        "HTTPS не работает (браузер пишет «Не защищено») → Certbot не отработал. Повторите команду certbot, "
        "убедитесь, что домен уже смотрит на сервер (п. 5, шаг 3).",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    story.append(Spacer(1, 18))
    story.append(P(
        "Если самостоятельно разобраться сложно — наймите фрилансера на бирже (Kwork, FL.ru) "
        "с задачей «Деплой Next.js на VPS». Стоимость работы: 1500–3000 ₽ за полное подключение под ключ.",
        style_note
    ))

    # Build with footer
    doc.build(story)
    print(f"✓ Saved: {out}")
    print(f"  Size: {os.path.getsize(out) / 1024:.1f} KB")


if __name__ == "__main__":
    build()
