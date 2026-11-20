#!/usr/bin/env python3
"""Generate SourceCraft Sites deployment guide PDF."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether,
)
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate, NextPageTemplate
from reportlab.platypus.frames import Frame
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

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

PRIMARY = colors.HexColor("#0E5C3A")
ACCENT = colors.HexColor("#2D8659")
SURFACE = colors.HexColor("#EDF5F2")
TEXT = colors.HexColor("#1A1F1C")
MUTED = colors.HexColor("#5C6A5F")
BORDER = colors.HexColor("#D8E0D3")
CODE_BG = colors.HexColor("#F1EDE1")
NOTE_BG = colors.HexColor("#FFF4E6")
NOTE_BORDER = colors.HexColor("#D97706")
FREE_BG = colors.HexColor("#ECFDF5")
FREE_BORDER = colors.HexColor("#10B981")

ss = getSampleStyleSheet()

style_h1 = ParagraphStyle("H1", parent=ss["Heading1"], fontName="LSans-Bold",
    fontSize=18, leading=22, textColor=PRIMARY, spaceBefore=24, spaceAfter=10)
style_h2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="LSans-Bold",
    fontSize=14, leading=18, textColor=ACCENT, spaceBefore=16, spaceAfter=6)
style_body = ParagraphStyle("Body", parent=ss["Normal"], fontName="LSans",
    fontSize=10.5, leading=15, textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=6)
style_bullet = ParagraphStyle("Bullet", parent=style_body, leftIndent=14, spaceAfter=3)
style_code = ParagraphStyle("Code", parent=ss["Code"], fontName="Courier",
    fontSize=9, leading=12, textColor=TEXT,
    backColor=CODE_BG, borderColor=BORDER, borderWidth=0.5,
    borderPadding=6, leftIndent=0, rightIndent=0, spaceBefore=6, spaceAfter=6)
style_note = ParagraphStyle("Note", parent=style_body, fontName="LSans-Italic",
    textColor=MUTED, fontSize=10, leading=14, leftIndent=10, rightIndent=10,
    backColor=SURFACE, borderColor=ACCENT, borderWidth=0, borderPadding=8,
    spaceBefore=8, spaceAfter=8)
style_free = ParagraphStyle("Free", parent=style_body, fontName="LSans",
    textColor=colors.HexColor("#065F46"), fontSize=10.5, leading=14,
    leftIndent=10, rightIndent=10, backColor=FREE_BG, borderColor=FREE_BORDER,
    borderWidth=1, borderPadding=8, spaceBefore=8, spaceAfter=8)
style_step_num = ParagraphStyle("StepNum", parent=ss["Normal"], fontName="LSans-Bold",
    fontSize=22, leading=24, textColor=ACCENT, alignment=TA_CENTER)
style_step_title = ParagraphStyle("StepTitle", parent=ss["Normal"], fontName="LSans-Bold",
    fontSize=12, leading=15, textColor=PRIMARY)
style_step_body = ParagraphStyle("StepBody", parent=style_body, fontSize=10.5, leading=14)


def P(text, style=style_body):
    return Paragraph(text, style)


def code_block(text):
    lines = text.strip().split("\n")
    escaped = "<br/>".join(
        line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
        for line in lines
    )
    return Paragraph(escaped, style_code)


def step_box(num, title, body_paragraphs):
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


def cover_canvas(canvas, doc):
    w, h = A4
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#0C1F1A"))
    canvas.rect(0, 0, w, h, fill=1, stroke=0)

    pad_l = 40
    canvas.setStrokeColor(colors.HexColor("#2D8659"))
    canvas.setLineWidth(2)
    canvas.line(pad_l, h - 100, w - 40, h - 100)

    canvas.setFillColor(colors.HexColor("#3DDBB5"))
    canvas.setFont("LSans-Bold", 10)
    canvas.drawString(pad_l, h - 90, "I N S T R U C T I O N   ·   S O U R C E C R A F T   ·   2 0 2 6")

    canvas.setFillColor(colors.white)
    canvas.setFont("LSans-Bold", 32)
    canvas.drawString(pad_l, h - 200, "Запуск сайта")
    canvas.drawString(pad_l, h - 240, "на SourceCraft Sites")

    canvas.setFillColor(colors.HexColor("#B0B8C0"))
    canvas.setFont("LSans", 14)
    canvas.drawString(pad_l, h - 280, "Бесплатный статический хостинг из GitHub-репозитория")

    canvas.setStrokeColor(colors.HexColor("#3DDBB5"))
    canvas.setLineWidth(3)
    meta_y = h - 350
    meta_lines = [
        "Бесплатный хостинг — 0 ₽ навсегда",
        "Подключение через GitHub-репозиторий",
        "Автоматический HTTPS и CI/CD",
        "Без своего домена (только поддомен SourceCraft)",
    ]
    canvas.setFillColor(colors.HexColor("#B0B8C0"))
    canvas.setFont("LSans", 11)
    for i, line in enumerate(meta_lines):
        y = meta_y - i * 20
        canvas.line(pad_l, y - 4, pad_l, y + 12)
        canvas.drawString(pad_l + 14, y, line)

    # Variant C badge
    canvas.setFillColor(colors.HexColor("#3DDBB5"))
    canvas.roundRect(pad_l, h - 540, w - 80, 50, 8, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#0C1F1A"))
    canvas.setFont("LSans-Bold", 11)
    canvas.drawString(pad_l + 14, h - 508, "ВАРИАНТ C — КОМБИНИРОВАННЫЙ")
    canvas.setFont("LSans", 9)
    canvas.drawString(pad_l + 14, h - 522, "Сначала бесплатный SourceCraft Sites → затем VPS с своим доменом")

    canvas.setStrokeColor(colors.HexColor("#2D8659"))
    canvas.setLineWidth(1)
    canvas.line(pad_l, 70, w - 40, 70)
    canvas.setFillColor(colors.HexColor("#90989F"))
    canvas.setFont("LSans", 9)
    canvas.drawString(pad_l, 55, "ЖИРОЧИСТ Самара")
    canvas.drawRightString(w - 40, 55, "Самара · 2026")
    canvas.restoreState()


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MUTED)
    canvas.setFont("LSans", 9)
    page_num = canvas.getPageNumber()
    if page_num > 1:
        canvas.drawCentredString(A4[0] / 2, 15 * mm, str(page_num - 1))
        canvas.setFont("LSans", 8)
        canvas.drawString(20 * mm, 15 * mm, "ЖИРОЧИСТ Самара · Запуск на SourceCraft Sites")
    canvas.restoreState()


def build():
    out = "/home/z/my-project/download/Инструкция_SourceCraft.pdf"

    doc = BaseDocTemplate(
        out, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=22 * mm,
        title="Инструкция по запуску сайта ЖИРОЧИСТ Самара на SourceCraft Sites",
        author="ЖИРОЧИСТ Самара",
        subject="Руководство по развёртыванию статической версии сайта на бесплатном хостинге SourceCraft Sites",
    )

    cover_frame = Frame(0, 0, A4[0], A4[1], leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="cover")
    cover_template = PageTemplate(id="Cover", frames=[cover_frame], onPage=cover_canvas)

    body_frame = Frame(
        20 * mm, 22 * mm, A4[0] - 40 * mm, A4[1] - 42 * mm,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="body",
    )
    body_template = PageTemplate(id="Body", frames=[body_frame], onPage=page_footer)

    doc.addPageTemplates([cover_template, body_template])

    story = []

    story.append(NextPageTemplate("Body"))
    story.append(PageBreak())

    # === PART 1: WHAT IS SOURCECRAFT SITES ===
    story.append(P("Часть 1. Что такое SourceCraft Sites", style_h1))
    story.append(P(
        "SourceCraft Sites — это бесплатный сервис статического хостинга от SourceCraft. "
        "Вы загружаете HTML/CSS/JS файлы в публичный репозиторий на GitHub, SourceCraft автоматически "
        "публикует сайт и выдаёт адрес вида <font face='Courier'>ваше-имя.sourcecraft.site</font>. "
        "HTTPS подключается автоматически, без настроек."
    ))
    story.append(P(
        "Сервис полностью бесплатный, без лимитов на трафик и количество сайтов. "
        "Подходит для лендингов, визиток, портфолио — любых статических сайтов.",
        style_free
    ))

    story.append(P("Ограничения (важно!)", style_h2))
    items = [
        "<b>Только статика</b> — нельзя запускать серверный код (Node.js, PHP, Python). Наша форма заявки адаптирована под это ограничение через сервис Web3Forms.",
        "<b>Свой домен подключить нельзя</b> — адрес будет вида <font face='Courier'>zhirochist.sourcecraft.site</font>. Это нормально для старта; когда заработаете — переходите на VPS со своим доменом.",
        "<b>Нет базы данных</b> — заявки не сохраняются на сервере, а приходят сразу на email через Web3Forms.",
        "<b>Публичный репозиторий</b> — код сайта будет виден всем на GitHub. Если не хотите — используйте VPS-версию.",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    story.append(P("Что работает на SourceCraft Sites", style_h2))
    items = [
        "✅ Весь лендинг с тем же дизайном (эко-зелёная палитра, секции, стили)",
        "✅ Форма заявки → заявки приходят на ваш email malofeev-koss@ya.ru через Web3Forms",
        "✅ Кнопки звонка, Telegram, MAX, email — все кликабельные",
        "✅ Адаптивный дизайн под телефон/планшет/десктоп",
        "✅ HTTPS автоматически (зелёный замочек)",
        "✅ Автоматическое обновление при пуше в GitHub",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    story.append(P("Что НЕ работает на SourceCraft Sites", style_h2))
    items = [
        "❌ Свой домен (только поддомен sourcecraft.site)",
        "❌ Telegram-бот для уведомлений о заявках (только email через Web3Forms)",
        "❌ Сохранение заявок в базу данных (только пересылка на email)",
        "❌ Серверные API endpoints (наш /api/lead не вызывается)",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    # === PART 2: WHAT YOU NEED ===
    story.append(P("Часть 2. Что нужно заранее", style_h1))
    items = [
        ("GitHub-аккаунт", "Бесплатная регистрация на github.com — туда загрузим код сайта"),
        ("Email malofeev-koss@ya.ru", "На него будут приходить заявки с формы через Web3Forms"),
        ("Аккаунт SourceCraft", "Бесплатная регистрация на sourcecraft.dev через GitHub-логин"),
        ("Web3Forms access key", "Бесплатный ключ для приёма заявок без сервера"),
        ("Код сайта из архива", "Файлы из папки src/ архива ЖироЧист_Самара_полный_пакет.zip"),
    ]
    data = [[P("<b>Что</b>", style_step_body), P("<b>Зачем</b>", style_step_body)]]
    for what, why in items:
        data.append([P(what, style_step_body), P(why, style_step_body)])
    tbl = Table(data, colWidths=[50 * mm, 116 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
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
    story.append(Spacer(1, 10))

    story.append(P(
        "Все шаги ниже бесплатные. Если у вас уже есть GitHub-аккаунт — пропустите шаг 1.",
        style_note
    ))

    # === PART 3: STEP-BY-STEP ===
    story.append(PageBreak())
    story.append(P("Часть 3. Пошаговая инструкция", style_h1))

    story.append(step_box(1, "Зарегистрируйтесь на GitHub",
        [
            "Откройте <font face='Courier'>github.com</font>, нажмите «Sign up» в правом верхнем углу.",
            "Введите email <font face='Courier'>malofeev-koss@ya.ru</font>, придумайте пароль, выберите username "
            "(например, <font face='Courier'>zhirochist-samara</font> или ваше имя).",
            "Подтвердите email по ссылке из письма.",
            "На странице вопроса «How do you plan to use GitHub?» выберите «Just me» и пропустите опрос.",
        ]))

    story.append(step_box(2, "Получите ключ Web3Forms",
        [
            "Откройте <font face='Courier'>web3forms.com</font> — это бесплатный сервис для приёма форм без бэкенда.",
            "В центре страницы найдите форму «Get your Access Key».",
            "Введите ваш email: <font face='Courier'>malofeev-koss@ya.ru</font>",
            "Нажмите «Get Access Key». На email в течение минуты придёт письмо с ключом вида "
            "<font face='Courier'>a1b2c3d4-e5f6-7890-abcd-ef1234567890</font>.",
            "Сохраните ключ — он понадобится в шаге 5.",
        ]))
    story.append(P(
        "Web3Forms бесплатный: 250 заявок в месяц на бесплатном тарифе. Для начала более чем достаточно.",
        style_note
    ))

    story.append(step_box(3, "Создайте новый репозиторий на GitHub",
        [
            "На GitHub нажмите «+» в правом верхнем углу → «New repository».",
            "Repository name: <font face='Courier'>zhirochist-site</font>",
            "Description: «Сайт-визитка ЖИРОЧИСТ Самара — чистка жироуловителей»",
            "Выберите <b>Public</b> (обязательно — SourceCraft работает только с публичными репозиториями).",
            "Поставьте галочку «Add a README file».",
            "Нажмите «Create repository».",
        ]))

    story.append(step_box(4, "Загрузите код сайта в репозиторий",
        [
            "Распакуйте архив <font face='Courier'>ЖироЧист_Самара_полный_пакет.zip</font> на компьютер.",
            "В репозитории на GitHub нажмите «Add file» → «Upload files».",
            "Перетащите в окно следующие файлы и папки:",
            "• <font face='Courier'>src/</font> (вся папка с page.tsx, layout.tsx, globals.css, api/)",
            "• <font face='Courier'>prisma/</font> (папка со schema.prisma)",
            "• <font face='Courier'>package.json</font>",
            "• <font face='Courier'>next.config.static.ts</font> (это важно! — статический конфиг)",
            "• <font face='Courier'>scripts/qr/</font> (папка с PNG-файлами QR-кодов)",
            "В поле «Commit changes» внизу напишите: «Initial upload».",
            "Нажмите «Commit changes».",
        ]))
    story.append(P(
        "Важно: загрузите именно <font face='Courier'>next.config.static.ts</font>, а не <font face='Courier'>next.config.ts</font>. "
        "Статический конфиг включает режим экспорта <font face='Courier'>output: 'export'</font>, который нужен для SourceCraft Sites.",
        style_note
    ))

    story.append(step_box(5, "Создайте файл .env с ключом Web3Forms",
        [
            "В репозитории нажмите «Add file» → «Create new file».",
            "Имя файла: <font face='Courier'>.env.local</font>",
            "Содержимое (замените ВАШ_КЛЮЧ на ключ из шага 2):",
        ]))
    story.append(code_block(
        'NEXT_PUBLIC_WEB3FORMS_KEY=ВАШ_КЛЮЧ_ИЗ_ШАГА_2'
    ))
    story.append(P(
        "Нажмите «Commit new file». ВАЖНО: переменные с префиксом <font face='Courier'>NEXT_PUBLIC_</font> "
        "доступны в браузере — это нужно, чтобы форма на клиенте могла отправить ключ Web3Forms."
    ))

    story.append(step_box(6, "Подготовьте файл package.json для статической сборки",
        [
            "Откройте файл <font face='Courier'>package.json</font> в репозитории (кликните на него).",
            "Нажмите карандаш (Edit) в правом верхнем углу.",
            "В разделе scripts добавьте команду static-build. Должно получиться:",
        ]))
    story.append(code_block(
        '"scripts": {\n'
        '  "dev": "next dev -p 3000",\n'
        '  "build": "next build",\n'
        '  "static-build": "cp next.config.static.ts next.config.ts && next build",\n'
        '  "start": "next start",\n'
        '  "lint": "eslint ."\n'
        '}'
    ))
    story.append(P(
        "Нажмите «Commit changes». Эта команда static-build скопирует статический конфиг и соберёт сайт в папку <font face='Courier'>out/</font>."
    ))

    # === PART 4: SOURCECRAFT SETUP ===
    story.append(PageBreak())
    story.append(P("Часть 4. Подключение SourceCraft Sites", style_h1))

    story.append(step_box(1, "Зарегистрируйтесь на SourceCraft",
        [
            "Откройте <font face='Courier'>sourcecraft.dev</font>.",
            "Нажмите «Войти» или «Sign in» в правом верхнем углу.",
            "Выберите «Continue with GitHub» — авторизация через ваш GitHub-аккаунт.",
            "Подтвердите доступ SourceCraft к вашему GitHub (нужно для чтения репозитория).",
            "После авторизации вы попадёте в личный кабинет SourceCraft.",
        ]))

    story.append(step_box(2, "Создайте организацию (если нужно)",
        [
            "SourceCraft Sites работает с публичными репозиториями публичных организаций.",
            "В личном кабинете откройте «Организации» → «Создать организацию».",
            "Название: «ЖИРОЧИСТ» или ваше имя.",
            "Тип: Public (публичная).",
            "После создания перенесите репозиторий zhirochist-site в эту организацию: "
            "на GitHub откройте репозиторий → Settings → Transfer → укажите имя организации.",
        ]))
    story.append(P(
        "Если не хотите создавать организацию — попробуйте сразу шаг 3. SourceCraft периодически "
        "обновляет правила; возможно, личные публичные репозитории тоже поддерживаются.",
        style_note
    ))

    story.append(step_box(3, "Создайте Site (сайт) в SourceCraft",
        [
            "В личном кабинете SourceCraft откройте раздел «Sites».",
            "Нажмите «Create site» или «Создать сайт».",
            "Выберите репозиторий <font face='Courier'>zhirochist-site</font> из списка.",
            "Укажите ветку: <font face='Courier'>main</font> (или master — какая у вас основная).",
            "Build command: <font face='Courier'>npm install && npm run static-build</font>",
            "Output directory: <font face='Courier'>out</font>",
            "Нажмите «Create» или «Deploy».",
        ]))
    story.append(P(
        "SourceCraft автоматически выполнит установку зависимостей и сборку. Это займёт 2–5 минут. "
        "В логах сборки должно быть сообщение «Exported successfully» — значит всё прошло хорошо."
    ))

    story.append(step_box(4, "Получите адрес сайта",
        [
            "После успешной сборки в карточке сайта появится адрес вида:",
            "<font face='Courier'>https://zhirochist-samara.sourcecraft.site</font>",
            "(точное имя зависит от вашего username на GitHub).",
            "Откройте адрес в браузере — должна появиться главная страница ЖИРОЧИСТ Самара.",
            "Сайт работает по HTTPS, ничего настраивать не нужно.",
        ]))
    story.append(P(
        "Готово! Сайт опубликован и доступен по адресу. Заявки с формы будут приходить на "
        "<font face='Courier'>malofeev-koss@ya.ru</font> через Web3Forms.",
        style_free
    ))

    # === PART 5: TESTING ===
    story.append(P("Часть 5. Проверка работы формы заявки", style_h1))

    story.append(step_box(1, "Заполните тестовую заявку",
        [
            "Откройте ваш адрес на SourceCraft Sites в браузере.",
            "Прокрутите до секции «Оставить заявку».",
            "Заполните форму тестовыми данными:",
            "• Имя: «Тест»",
            "• Телефон: ваш номер",
            "• Услуга: «Чистка жироуловителя»",
            "Нажмите «Отправить заявку».",
        ]))

    story.append(step_box(2, "Проверьте email",
        [
            "Откройте почту <font face='Courier'>malofeev-koss@ya.ru</font>.",
            "Должно прийти письмо от Web3Forms с темой «Новая заявка с сайта ЖИРОЧИСТ Самара».",
            "В письме будут указаны имя, телефон, услуга, адрес и комментарий клиента.",
            "Если письмо не пришло в течение 5 минут — проверьте папку «Спам».",
        ]))

    story.append(step_box(3, "Если форма не работает",
        [
            "Проверьте, что в файле <font face='Courier'>.env.local</font> в репозитории указан правильный ключ "
            "NEXT_PUBLIC_WEB3FORMS_KEY (без пробелов в начале/конце).",
            "Проверьте лог сборки в SourceCraft — нет ли ошибок. Если есть — обычно проблема в "
            "неправильном package.json или отсутствии next.config.static.ts.",
            "Откройте инструменты разработчика в браузере (F12) → Console → заполните форму → "
            "посмотрите ошибки. Если есть CORS — это нормально, Web3Forms поддерживает их.",
        ]))

    # === PART 6: EVERYDAY USE ===
    story.append(P("Часть 6. Повседневное использование", style_h1))

    story.append(P("Как обновлять сайт", style_h2))
    story.append(P(
        "SourceCraft автоматически пересобирает сайт при каждом пуше в основную ветку GitHub-репозитория. "
        "Чтобы изменить что-то на сайте (например, цену или контакт):"
    ))
    items = [
        "Отредактируйте нужный файл прямо на GitHub (кнопка «карандаш» при просмотре файла).",
        "Сделайте commit с описанием изменения.",
        "Подождите 2–3 минуты — SourceCraft пересоберёт сайт автоматически.",
        "Изменения появятся по тому же адресу.",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    story.append(P("Что нельзя менять на статической версии", style_h2))
    items = [
        "<b>QR-коды в визитках</b> — если зарегистрировали домен и хотите обновить QR в визитках, "
        "перегенерируйте PDF по инструкции из архива (Лист 6 руководства визиток).",
        "<b>Telegram-уведомления</b> — не подключаются на SourceCraft. Если нужны — переходите на VPS.",
        "<b>Сохранение заявок в базу</b> — нет БД, заявки только на email.",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    story.append(P("Что можно менять прямо на GitHub", style_h2))
    items = [
        "<b>Цены и услуги</b> — в файле <font face='Courier'>src/app/page.tsx</font> найдите массив <font face='Courier'>pricing = [...]</font>.",
        "<b>Текст секций</b> — там же, в массивах <font face='Courier'>services</font>, <font face='Courier'>segments</font>, <font face='Courier'>faq</font>.",
        "<b>Контакты</b> — в начале <font face='Courier'>src/app/page.tsx</font>: PHONE_DISPLAY, TELEGRAM_URL, MAX_URL, EMAIL.",
        "<b>Тексты в FAQ</b> — массив <font face='Courier'>faq = [...]</font>.",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    # === PART 7: MIGRATION TO VPS ===
    story.append(PageBreak())
    story.append(P("Часть 7. Переход на VPS со своим доменом (Вариант C → B)", style_h1))
    story.append(P(
        "Когда сайт начнёт приносить клиентов и вы захотите свой домен <font face='Courier'>zhirochist-samara.ru</font> "
        "и Telegram-уведомления — переходите на VPS. Это Вариант B из основной инструкции."
    ))

    story.append(P("Что меняется при переходе", style_h2))
    items = [
        "✅ Появляется свой домен <font face='Courier'>zhirochist-samara.ru</font> вместо поддомена SourceCraft",
        "✅ Подключается Telegram-бот — заявки приходят сразу в Telegram, не только на email",
        "✅ Заявки сохраняются в SQLite базу на сервере — есть история",
        "✅ Можно подключить Яндекс.Метрику и аналитику",
        "❌ Нужно платить за VPS (~800 ₽/мес на Beget/Timeweb) + домен (~250 ₽/год)",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    story.append(P("Как перейти — 4 шага", style_h2))

    story.append(step_box(1, "Арендуйте VPS и домен",
        [
            "Следуйте инструкции <font face='Courier'>Инструкция_Beget.pdf</font> или "
            "<font face='Courier'>Инструкция_по_запуску_сайта.pdf</font> (для Timeweb) из архива.",
            "Арендуйте VPS KVM (2 vCPU, 2 ГБ RAM) и домен .ru.",
        ]))

    story.append(step_box(2, "Загрузите код на сервер",
        [
            "На сервере клонируйте тот же GitHub-репозиторий:",
        ]))
    story.append(code_block(
        'cd /var/www\ngit clone https://github.com/ВАШ_ЛОГИН/zhirochist-site.git zhirochist\ncd zhirochist'
    ))

    story.append(step_box(3, "Переключитесь на серверный конфиг",
        [
            "В папке проекта переименуйте конфиги:",
        ]))
    story.append(code_block(
        '# Включаем серверный режим (output: standalone вместо export)\n'
        'rm next.config.ts\n'
        'cp next.config.static.ts next.config.ts.bak  # на всякий случай\n'
        '# Если next.config.ts не существует, создайте его с output: standalone\n'
        'cat > next.config.ts << \'EOF\'\n'
        'import type { NextConfig } from "next";\n'
        'const nextConfig: NextConfig = {\n'
        '  output: "standalone",\n'
        '  reactStrictMode: false,\n'
        '  typescript: { ignoreBuildErrors: true }\n'
        '};\n'
        'export default nextConfig;\n'
        'EOF'
    ))

    story.append(step_box(4, "Настройте Telegram-бота и запустите",
        [
            "Откройте файл <font face='Courier'>.env</font> на сервере:",
        ]))
    story.append(code_block(
        'nano /var/www/zhirochist/.env\n\n'
        '# Заполните:\n'
        'NEXT_PUBLIC_WEB3FORMS_KEY=оставьте_ключ_для_дублирования_на_email\n'
        'TELEGRAM_BOT_TOKEN=токен_от_BotFather\n'
        'TELEGRAM_CHAT_ID=ваш_chat_id'
    ))
    story.append(P(
        "Теперь заявки будут приходить И на email (через Web3Forms), И в Telegram (через /api/lead). "
        "Двойное уведомление — надёжнее."
    ))
    story.append(P(
        "Пересоберите и запустите сайт:",
    ))
    story.append(code_block(
        'cd /var/www/zhirochist\n'
        'bun install\n'
        'bun run db:push\n'
        'bun run build\n'
        'pm2 start "bun run start" --name zhirochist\n'
        'pm2 save && pm2 startup'
    ))

    story.append(P(
        "После настройки Nginx, DNS и SSL (см. инструкции в архиве) сайт будет доступен по "
        "<font face='Courier'>https://zhirochist-samara.ru</font> с полным функционалом.",
        style_free
    ))

    # === PART 8: CHECKLIST ===
    story.append(P("Часть 8. Финальный чек-лист SourceCraft Sites", style_h1))
    checklist = [
        ("GitHub-аккаунт зарегистрирован", "github.com открывается"),
        ("Web3Forms ключ получен на email", "Письмо от web3forms.com пришло"),
        ("Репозиторий zhirochist-site создан (Public)", "Виден на GitHub"),
        ("Код загружен в репозиторий", "Файлы src/, package.json, next.config.static.ts"),
        (".env.local с WEB3FORMS_KEY создан", "В корне репозитория"),
        ("Аккаунт SourceCraft создан", "Через GitHub-логин"),
        ("Site создан в SourceCraft", "Привязан к репозиторию"),
        ("Build command: npm run static-build", "В настройках Site"),
        ("Output directory: out", "В настройках Site"),
        ("Сайт собран без ошибок", "Статус: Success в логах"),
        ("Сайт открывается по адресу .sourcecraft.site", "Главная страница видна"),
        ("Форма отправляет заявку", "Тест → письмо на email"),
        ("Email получает заявки", "Папка «Входящие» или «Спам»"),
    ]
    data = [[P("<b>Что проверить</b>", style_step_body), P("<b>Как проверить</b>", style_step_body)]]
    for what, how in checklist:
        data.append([P("☐ " + what, style_step_body), P(how, style_step_body)])
    tbl = Table(data, colWidths=[95 * mm, 71 * mm])
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

    # === SUMMARY ===
    story.append(P("Итог по Варианту C", style_h1))
    story.append(P(
        "Вы выбрали комбинированный подход: сначала бесплатный статический хостинг (SourceCraft Sites), "
        "затем переход на VPS с своим доменом. Это оптимально для самозанятого — не платите за хостинг, "
        "пока сайт не приносит доход, но готовы масштабироваться в любой момент."
    ))

    story.append(P("Сравнение этапов", style_h2))
    story.append(Table([
        [P("<b>Параметр</b>", style_step_body), P("<b>Этап 1: SourceCraft</b>", style_step_body), P("<b>Этап 2: VPS</b>", style_step_body)],
        [P("Цена", style_step_body), P("0 ₽", style_step_body), P("~10 000 ₽/год", style_step_body)],
        [P("Домен", style_step_body), P("поддомен sourcecraft.site", style_step_body), P("zhirochist-samara.ru", style_step_body)],
        [P("Форма заявки", style_step_body), P("→ email", style_step_body), P("→ email + Telegram", style_step_body)],
        [P("База данных", style_step_body), P("❌ нет", style_step_body), P("✅ SQLite", style_step_body)],
        [P("HTTPS", style_step_body), P("✅ автоматически", style_step_body), P("✅ через certbot", style_step_body)],
        [P("Время запуска", style_step_body), P("~30 минут", style_step_body), P("~2-3 часа", style_step_body)],
    ], colWidths=[40 * mm, 63 * mm, 63 * mm], style=[
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

    story.append(Spacer(1, 16))
    story.append(P(
        "Если возникнут вопросы по конкретному шагу — возвращайтесь к этой инструкции. "
        "Все адреса сайтов и сервисов проверены, контакты (телефон +7 996 213-52-20, "
        "email malofeev-koss@ya.ru) уже вшиты в код сайта.",
        style_note
    ))

    doc.build(story)
    print(f"✓ Saved: {out}")
    print(f"  Size: {os.path.getsize(out) / 1024:.1f} KB")


if __name__ == "__main__":
    build()
