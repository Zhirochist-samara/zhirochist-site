#!/usr/bin/env python3
"""Generate Beget-specific deployment guide PDF for ЖИРОЧИСТ Самара site."""

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

# Register Liberation Sans (Cyrillic support)
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
SURFACE = colors.HexColor("#EDF5F2")
TEXT = colors.HexColor("#1A1F1C")
MUTED = colors.HexColor("#5C6A5F")
BORDER = colors.HexColor("#D8E0D3")
CODE_BG = colors.HexColor("#F1EDE1")
WARN_BG = colors.HexColor("#FFF4E6")
WARN_BORDER = colors.HexColor("#D97706")

ss = getSampleStyleSheet()

style_title = ParagraphStyle("Title", parent=ss["Title"], fontName="LSans-Bold",
    fontSize=28, leading=34, textColor=PRIMARY, alignment=TA_LEFT, spaceAfter=8)
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
style_warn = ParagraphStyle("Warn", parent=style_body, fontName="LSans",
    textColor=colors.HexColor("#7C2D12"), fontSize=10.5, leading=14,
    leftIndent=10, rightIndent=10, backColor=WARN_BG, borderColor=WARN_BORDER,
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


def make_table(data_rows, col_widths, header=True):
    data = []
    for i, row in enumerate(data_rows):
        if i == 0 and header:
            data.append([P(f"<b>{c}</b>", style_step_body) for c in row])
        else:
            data.append([P(c if isinstance(c, str) else str(c), style_step_body) for c in row])
    tbl = Table(data, colWidths=col_widths)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [colors.white, SURFACE]),
        ("BOX", (0, 0), (-1, -1), 0.5, ACCENT),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
    ]
    if header:
        style.insert(0, ("BACKGROUND", (0, 0), (-1, 0), PRIMARY))
        style.insert(1, ("TEXTCOLOR", (0, 0), (-1, 0), colors.white))
    tbl.setStyle(TableStyle(style))
    return tbl


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
    canvas.drawString(pad_l, h - 90, "I N S T R U C T I O N   ·   B E G E T   ·   2 0 2 6")

    canvas.setFillColor(colors.white)
    canvas.setFont("LSans-Bold", 34)
    canvas.drawString(pad_l, h - 200, "Запуск сайта")
    canvas.drawString(pad_l, h - 245, "на хостинге Beget")

    canvas.setFillColor(colors.HexColor("#B0B8C0"))
    canvas.setFont("LSans", 16)
    canvas.drawString(pad_l, h - 285, "ЖИРОЧИСТ Самара — пошаговое руководство")

    canvas.setStrokeColor(colors.HexColor("#3DDBB5"))
    canvas.setLineWidth(3)
    meta_y = h - 360
    meta_lines = [
        "Регистрация домена и VPS на Beget",
        "Установка Node.js и запуск Next.js",
        "Бесплатный SSL и Telegram-уведомления",
    ]
    canvas.setFillColor(colors.HexColor("#B0B8C0"))
    canvas.setFont("LSans", 12)
    for i, line in enumerate(meta_lines):
        y = meta_y - i * 22
        canvas.line(pad_l, y - 4, pad_l, y + 12)
        canvas.drawString(pad_l + 14, y, line)

    # Warning badge
    canvas.setFillColor(colors.HexColor("#FEF3C7"))
    canvas.roundRect(pad_l, h - 510, w - 80, 60, 8, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#92400E"))
    canvas.setFont("LSans-Bold", 10)
    canvas.drawString(pad_l + 14, h - 462, "ВНИМАНИЕ")
    canvas.setFont("LSans", 9)
    canvas.drawString(pad_l + 14, h - 478, "Beget восстанавливается после кибератаки 1–2 ноября 2026 г.")
    canvas.drawString(pad_l + 14, h - 491, "VPS может быть временно недоступен — см. часть 1 данной инструкции")

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
        canvas.drawString(20 * mm, 15 * mm, "ЖИРОЧИСТ Самара · Запуск на Beget")
    canvas.restoreState()


def build():
    out = "/home/z/my-project/download/Инструкция_Beget.pdf"

    doc = BaseDocTemplate(
        out, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=22 * mm,
        title="Инструкция по запуску сайта ЖИРОЧИСТ Самара на Beget",
        author="ЖИРОЧИСТ Самара",
        subject="Руководство по развёртыванию сайта-визитки на хостинге Beget",
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

    # === COVER ===
    story.append(NextPageTemplate("Body"))
    story.append(PageBreak())

    # === PART 1: IMPORTANT WARNING ===
    story.append(P("Часть 1. Важное предупреждение о состоянии Beget", style_h1))
    story.append(P(
        "В ночь с 1 на 2 ноября 2026 года хостинг-провайдер Beget подвергся серьёзной кибератаке. "
        "Была уничтожена часть облачной инфраструктуры: VPS, S3-хранилище, Kubernetes, облачные базы данных. "
        "На 16 ноября 2026 года восстановлено 95% виртуального хостинга и 94% выделенных серверов, "
        "но новые VPS для заказчиков могут быть временно недоступны."
    ))
    story.append(P(
        "Если раздел «VPS» на сайте beget.com помечен как «Временно недоступно» — это нормально. "
        "Beget активно восстанавливает инфраструктуру. Проверяйте статус регулярно (раз в 3–5 дней) "
        "или подпишитесь на их Telegram-канал @beget, чтобы узнать о возобновлении приёма заказов.",
        style_warn
    ))
    story.append(P("Что делать, пока VPS Beget недоступен:", style_h2))
    story.append(P("• Зарегистрировать домен на Beget или reg.ru прямо сейчас (домены работают).", style_bullet))
    story.append(P("• Прочитать стратегию и стикеры из архива, подготовить Telegram-бота.", style_bullet))
    story.append(P("• Подождать 2–4 недели до полного восстановления VPS Beget.", style_bullet))
    story.append(P("• Если сайт нужно запустить срочно — используйте Timeweb Cloud (см. инструкцию «Инструкция_по_запуску_сайта.pdf»).", style_bullet))
    story.append(P(
        "Дальше в этой инструкции предполагается, что VPS Beget уже доступен для заказа. "
        "Если это не так — вернитесь к этому разделу и выберите альтернативу."
    ))

    # === PART 2: WHAT TO RENT ===
    story.append(P("Часть 2. Что арендовать на Beget", style_h1))
    story.append(P(
        "Для работы сайта на Next.js нужен именно VPS KVM (виртуальный сервер с root-доступом), "
        "а не обычный shared-хостинг. Shared-хостинг Beget поддерживает только PHP/MySQL и не подходит."
    ))

    story.append(P("Список необходимых услуг:", style_h2))
    story.append(make_table(
        [
            ["Услуга", "Зачем нужна", "Цена", "Срок"],
            ["Домен .ru", "Адрес сайта (например, zhirochist-samara.ru)", "~250 ₽", "за год"],
            ["VPS KVM «Стратегия»", "Хостинг для Next.js (2 vCPU, 2 ГБ RAM, 30 ГБ SSD)", "~810 ₽/мес", "помесячно"],
            ["SSL Let's Encrypt", "HTTPS (зелёный замочек)", "бесплатно", "автопродление"],
            ["Бэкапы", "Резервные копии сервера", "включено", "ежедневно"],
        ],
        col_widths=[35 * mm, 65 * mm, 30 * mm, 36 * mm],
    ))
    story.append(Spacer(1, 10))
    story.append(P(
        "<b>Итого на старте:</b> ~1 060 ₽ (домен + первый месяц VPS)<br/>"
        "<b>Итого на год:</b> ~9 970 ₽ (домен + 12 месяцев VPS)",
        style_note
    ))

    story.append(P("Какой тариф VPS выбрать", style_h2))
    story.append(P(
        "Beget предлагает линейку VPS-тарифов на KVM-виртуализации. Для сайта на Next.js "
        "минимально достаточно конфигурации 2 vCPU / 2 ГБ RAM / 30 ГБ SSD. Это тариф уровня "
        "«Стратегия» или аналог — точное название смотрите в актуальной линейке на beget.com/vps."
    ))
    story.append(make_table(
        [
            ["Тариф (примерно)", "CPU", "RAM", "Диск", "Цена/мес", "Подходит?"],
            ["Минимальный", "1 ядро", "1 ГБ", "20 ГБ", "~210 ₽", "Слабо — Next.js может тормозить"],
            ["Стратегия", "2 ядра", "2 ГБ", "30 ГБ", "~810 ₽", "✅ Оптимально для нашего сайта"],
            ["Продвинутый", "4 ядра", "4 ГБ", "50 ГБ", "~1 500 ₽", "С запасом, если будет много заявок"],
        ],
        col_widths=[28 * mm, 18 * mm, 18 * mm, 18 * mm, 24 * mm, 60 * mm],
    ))

    story.append(P("Почему не подойдёт shared-хостинг Beget", style_h2))
    story.append(P(
        "Shared-хостинг Beget (тарифы «Blog», «Start», «Vip») — это классический PHP/MySQL хостинг "
        "для сайтов на WordPress, Joomla, Битрикс. Там нельзя запустить Node.js-приложение как "
        "постоянный процесс, а Next.js именно так и работает. Поэтому для нашего сайта "
        "shared-хостинг не подходит — только VPS KVM."
    ))

    # === PART 3: REGISTRATION ===
    story.append(PageBreak())
    story.append(P("Часть 3. Регистрация аккаунта и домена на Beget", style_h1))

    story.append(step_box(1, "Зарегистрируйтесь на Beget",
        [
            "Откройте <font face='Courier'>beget.com</font> (или <font face='Courier'>beget.ru</font>).",
            "В правом верхнем углу нажмите «Регистрация».",
            "Укажите email, придумайте пароль, подтвердите по ссылке из письма.",
            "Заполните профиль: ФИО, телефон. Для регистрации домена .ru позже понадобятся "
            "паспортные данные — заполните их в личном кабинете заранее.",
        ]))

    story.append(step_box(2, "Пополните баланс",
        [
            "В личном кабинете <font face='Courier'>cp.beget.com</font> откройте раздел «Баланс» → «Пополнить».",
            "Минимальная сумма пополнения обычно 100 ₽. Рекомендую сразу положить 1 100 ₽ — "
            "хватит на домен и первый месяц VPS.",
            "Способы оплаты: банковская карта (Россия), СБП, ЮMoney, Qiwi, безналичный расчёт.",
        ]))

    story.append(step_box(3, "Зарегистрируйте домен .ru",
        [
            "В панели управления откройте раздел «Домены» → «Зарегистрировать домен».",
            "Введите желаемое имя, например <font face='Courier'>zhirochist-samara.ru</font>.",
            "Проверьте, что домен свободен. Если занят — попробуйте варианты: "
            "<font face='Courier'>zhirochist63.ru</font>, <font face='Courier'>zhirochist-samara.ru</font>, "
            "<font face='Courier'>жироуловитель-самара.рф</font> (кириллица).",
            "Добавьте в корзину, оплатите (~250 ₽ за год).",
            "При регистрации укажите реальные паспортные данные — требование Роскомнадзора.",
            "После регистрации домен автоматически будет использовать NS-серверы Beget: "
            "<font face='Courier'>ns1.beget.com</font>, <font face='Courier'>ns2.beget.com</font> и т.д.",
        ]))

    story.append(step_box(4, "Заполните данные регистратора",
        [
            "В разделе «Домены» → ваш домен → «Данные регистратора» заполните: ФИО, "
            "паспортные данные (серия, номер, кем и когда выдан), адрес, телефон, email.",
            "Без этих данных домен .ru не будет делегирован (не начнёт работать).",
            "Проверка данных занимает от нескольких минут до суток.",
        ]))

    # === PART 4: VPS ORDER ===
    story.append(P("Часть 4. Аренда VPS KVM на Beget", style_h1))

    story.append(step_box(1, "Проверьте доступность VPS",
        [
            "В панели управления <font face='Courier'>cp.beget.com</font> откройте раздел «VPS» или "
            "«Серверы» → «VPS/VDS».",
            "Если раздел доступен и позволяет создать сервер — отлично, продолжайте.",
            "Если показывается сообщение «Временно недоступно» или «Раздел в разработке» — "
            "это значит, что Beget ещё восстанавливает VPS после кибератаки. "
            "В этом случае либо подождите, либо используйте Timeweb Cloud (см. основную инструкцию).",
        ]))

    story.append(step_box(2, "Создайте сервер VPS",
        [
            "Нажмите «Создать сервер» или «Заказать VPS».",
            "Выберите конфигурацию: <b>2 vCPU, 2 ГБ RAM, 30 ГБ SSD</b> (тариф «Стратегия» или аналог).",
            "Локация: <b>Россия, Санкт-Петербург</b> (или Москва, если доступно).",
            "Операционная система: <b>Ubuntu 22.04 LTS</b>.",
            "Виртуализация: <b>KVM</b> (стоит по умолчанию).",
            "Сетевой интерфейс: публичный IPv4-адрес — обязательно включите.",
            "Название сервера: <font face='Courier'>zhirochist</font>.",
            "Проверьте цену (должна быть ~810 ₽/мес или ~27 ₽/сутки при посуточной тарификации).",
            "Нажмите «Создать» и оплатите (спишется с баланса).",
        ]))

    story.append(step_box(3, "Сохраните IP-адрес и root-пароль",
        [
            "После создания сервера (1–3 минуты) в карточке сервера появится его публичный IP-адрес "
            "вида <font face='Courier'>45.142.122.18</font>.",
            "root-пароль будет выслан на контактную почту и отображается в карточке сервера "
            "(раздел «Параметры» → «Пароль root»).",
            "Запишите IP и пароль в надёжное место — без них не сможете подключиться к серверу.",
        ]))

    # === PART 5: SSH CONNECT ===
    story.append(P("Часть 5. Подключение к серверу по SSH", style_h1))
    story.append(P(
        "Далее работа идёт в терминале — чёрном окне с командами. На Windows 10/11 откройте "
        "PowerShell (Win+R → powershell). На Mac/Linux — Terminal. Команды можно копировать "
        "из этой инструкции и вставлять."
    ))

    story.append(step_box(1, "Подключитесь к серверу",
        [
            "Команда для подключения (замените IP на свой):",
        ]))
    story.append(code_block("ssh root@45.142.122.18"))
    story.append(P(
        "При первом подключении напишите <font face='Courier'>yes</font> и нажмите Enter. "
        "Затем введите root-пароль (символы не отображаются при вводе — это нормально)."
    ))

    story.append(step_box(2, "Обновите систему",
        [
            "Сразу после входа выполните:",
        ]))
    story.append(code_block("apt update && apt upgrade -y"))

    story.append(step_box(3, "Установите Node.js 20, Nginx, Git",
        [
            "Выполните команды по очереди:",
        ]))
    story.append(code_block(
        "curl -fsSL https://deb.nodesource.com/setup_20.x | bash -\n"
        "apt install -y nodejs git nginx\n"
        "npm install -g bun pm2"
    ))
    story.append(P(
        "Проверьте установку: <font face='Courier'>node -v</font> должно показать v20.x.x, "
        "<font face='Courier'>bun -v</font> — версию 1.x.x, <font face='Courier'>nginx -v</font> — версию nginx."
    ))

    # === PART 6: UPLOAD CODE ===
    story.append(P("Часть 6. Загрузка кода сайта на сервер", style_h1))

    story.append(step_box(1, "Создайте папку для сайта",
        [
            "Стандартная папка для веб-проектов на Linux:",
        ]))
    story.append(code_block("mkdir -p /var/www/zhirochist\ncd /var/www/zhirochist"))

    story.append(step_box(2, "Загрузите код через Git (если используете GitHub)",
        [
            "Если вы заранее выложили код на GitHub — просто клонируйте репозиторий:",
        ]))
    story.append(code_block(
        "git clone https://github.com/ВАШ-ЛОГИН/zhirochist-site.git ."
    ))

    story.append(step_box(3, "Альтернатива: загрузите ZIP через файловый менеджер Beget",
        [
            "Если GitHub не используете — в панели Beget откройте раздел «Файлы» или "
            "«Файловый менеджер» (если доступен).",
            "Загрузите ZIP-архив проекта в папку <font face='Courier'>/var/www/zhirochist/</font>.",
            "На сервере распакуйте: <font face='Courier'>unzip archive.zip -d /var/www/zhirochist</font>",
            "Если unzip не установлен: <font face='Courier'>apt install -y unzip</font>",
        ]))

    story.append(step_box(4, "Альтернатива: загрузите через SCP с компьютера",
        [
            "На своём компьютере (не на сервере) выполните:",
        ]))
    story.append(code_block("scp zhirochist-site.zip root@45.142.122.18:/var/www/zhirochist/"))
    story.append(P("Затем на сервере распакуйте архив командой из предыдущего шага."))

    # === PART 7: INSTALL + BUILD ===
    story.append(P("Часть 7. Установка зависимостей и сборка сайта", style_h1))

    story.append(step_box(1, "Установите зависимости",
        [
            "Перейдите в папку проекта и установите все библиотеки:",
        ]))
    story.append(code_block("cd /var/www/zhirochist\nbun install"))

    story.append(step_box(2, "Создайте файл .env",
        [
            "Скопируйте пример в реальный файл и отредактируйте:",
        ]))
    story.append(code_block("cp .env.example .env\nnano .env"))
    story.append(P(
        "Заполните строки (вставьте свои значения, остальное оставьте как есть):"
    ))
    story.append(code_block(
        'DATABASE_URL=file:/var/www/zhirochist/db/custom.db\n\n'
        'TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН_ОТ_BOTFATHER\n'
        'TELEGRAM_CHAT_ID=ВАШ_CHAT_ID'
    ))
    story.append(P("Сохраните: Ctrl+O, Enter, Ctrl+X."))

    story.append(step_box(3, "Примените схему базы данных",
        [
            "Создаст файл SQLite с таблицей Lead для заявок:",
        ]))
    story.append(code_block("bun run db:push"))

    story.append(step_box(4, "Соберите сайт в продакшн-режиме",
        [
            "Сборка займёт 2–5 минут. В конце должно быть сообщение об успехе без красных ошибок:",
        ]))
    story.append(code_block("bun run build"))

    # === PART 8: PM2 START ===
    story.append(P("Часть 8. Запуск сайта через PM2", style_h1))
    story.append(P(
        "PM2 — менеджер процессов. Он держит сайт работающим 24/7, автоматически перезапускает "
        "его при сбое и включает автозапуск при перезагрузке сервера."
    ))

    story.append(step_box(1, "Запустите сайт",
        [
            "В папке проекта выполните:",
        ]))
    story.append(code_block(
        "cd /var/www/zhirochist\n"
        "pm2 start \"bun run start\" --name zhirochist\n"
        "pm2 save"
    ))

    story.append(step_box(2, "Включите автозапуск при перезагрузке сервера",
        [
            "Выполните команду:",
        ]))
    story.append(code_block("pm2 startup"))
    story.append(P(
        "PM2 выведет длинную команду вида "
        "<font face='Courier'>sudo env PATH=... pm2 startup systemd ...</font>. "
        "Скопируйте её целиком и выполните — это включит автозапуск."
    ))

    story.append(step_box(3, "Проверьте, что сайт работает",
        [
            "Внутри сервера проверьте командой:",
        ]))
    story.append(code_block("curl http://localhost:3000"))
    story.append(P(
        "Должно вернуть HTML-код страницы (начинается с <font face='Courier'>&lt;!DOCTYPE html&gt;</font>). "
        "Если ответ пустой или с ошибкой — проверьте <font face='Courier'>pm2 logs zhirochist</font>."
    ))

    # === PART 9: NGINX ===
    story.append(PageBreak())
    story.append(P("Часть 9. Настройка Nginx как обратного прокси", style_h1))
    story.append(P(
        "Сейчас сайт доступен только на порту 3000 внутри сервера. Чтобы он открывался по "
        "стандартным портам 80 (HTTP) и 443 (HTTPS) — нужен Nginx."
    ))

    story.append(step_box(1, "Создайте конфигурационный файл Nginx",
        [
            "Создайте файл:",
        ]))
    story.append(code_block("nano /etc/nginx/sites-available/zhirochist"))
    story.append(P(
        "Вставьте туда следующий конфиг (замените <font face='Courier'>ВАШ_ДОМЕН.ru</font> "
        "на ваш реальный домен):"
    ))
    story.append(code_block(
        "server {\n"
        "    listen 80;\n"
        "    server_name ВАШ_ДОМЕН.ru www.ВАШ_ДОМЕН.ru;\n\n"
        "    location / {\n"
        "        proxy_pass http://localhost:3000;\n"
        "        proxy_http_version 1.1;\n"
        "        proxy_set_header Upgrade $http_upgrade;\n"
        "        proxy_set_header Connection 'upgrade';\n"
        "        proxy_set_header Host $host;\n"
        "        proxy_set_header X-Real-IP $remote_addr;\n"
        "        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n"
        "        proxy_set_header X-Forwarded-Proto $scheme;\n"
        "        proxy_cache_bypass $http_upgrade;\n"
        "    }\n"
        "}"
    ))
    story.append(P("Сохраните: Ctrl+O, Enter, Ctrl+X."))

    story.append(step_box(2, "Включите конфигурацию и перезапустите Nginx",
        [
            "Выполните команды:",
        ]))
    story.append(code_block(
        "ln -s /etc/nginx/sites-available/zhirochist /etc/nginx/sites-enabled/\n"
        "nginx -t\n"
        "systemctl restart nginx"
    ))
    story.append(P(
        "Команда <font face='Courier'>nginx -t</font> должна показать "
        "«test is successful». Если есть ошибки — проверьте синтаксис конфига."
    ))

    # === PART 10: DOMAIN DNS ===
    story.append(P("Часть 10. Подключение домена к серверу", style_h1))

    story.append(step_box(1, "Добавьте A-запись в панели Beget",
        [
            "В панели <font face='Courier'>cp.beget.com</font> откройте «Домены» → ваш домен → "
            "«DNS» → «Управление DNS».",
            "Если домен использует NS-серверы Beget (по умолчанию) — добавьте A-запись:",
            "• <b>Тип:</b> A",
            "• <b>Имя (хост):</b> @ (собака — означает корневой домен)",
            "• <b>Значение:</b> IP вашего сервера (например, 45.142.122.18)",
            "• <b>TTL:</b> оставьте по умолчанию (обычно 3600 секунд)",
            "Сохраните запись.",
        ]))

    story.append(step_box(2, "Добавьте запись для www",
        [
            "Создайте вторую A-запись для поддомена www:",
            "• <b>Тип:</b> A",
            "• <b>Имя (хост):</b> www",
            "• <b>Значение:</b> тот же IP сервера",
            "Сохраните.",
        ]))

    story.append(step_box(3, "Дождитесь обновления DNS",
        [
            "DNS-записи обновляются от 15 минут до 24 часов (обычно 30–60 минут).",
            "Проверьте на своём компьютере командой:",
        ]))
    story.append(code_block("nslookup ВАШ_ДОМЕН.ru"))
    story.append(P(
        "В ответе должен появиться ваш IP сервера. Если показывает другой IP или «не найден» — "
        "подождите ещё, DNS ещё не обновился."
    ))

    # === PART 11: SSL ===
    story.append(P("Часть 11. Бесплатный SSL-сертификат (HTTPS)", style_h1))
    story.append(P(
        "Beget предлагает бесплатный SSL Let's Encrypt через панель управления. Но для VPS "
        "проще и надёжнее установить сертификат прямо на сервере через certbot — он будет "
        "автоматически продлеваться."
    ))

    story.append(step_box(1, "Установите certbot",
        [
            "На сервере выполните:",
        ]))
    story.append(code_block("apt install -y certbot python3-certbot-nginx"))

    story.append(step_box(2, "Запустите получение сертификата",
        [
            "Замените домен на свой и выполните:",
        ]))
    story.append(code_block(
        "certbot --nginx -d ВАШ_ДОМЕН.ru -d www.ВАШ_ДОМЕН.ru"
    ))
    story.append(P(
        "Certbot спросит ваш email — укажите реальный (пришлёт уведомления об истечении). "
        "Согласитесь с условиями (Y). Выберите вариант «2» — автоматическое перенаправление "
        "с HTTP на HTTPS."
    ))

    story.append(step_box(3, "Проверьте, что сайт открывается",
        [
            "Откройте в браузере <font face='Courier'>https://ВАШ_ДОМЕН.ru</font>",
            "Должна открыться главная страница сайта с зелёным замочком в адресной строке.",
            "Заполните тестовую заявку — должно прийти уведомление в Telegram (если настроили).",
        ]))
    story.append(P(
        "Сертификат Let's Encrypt действует 90 дней и автоматически продлевается через "
        "certbot-renew.timer. Ничего делать вручную не нужно.",
        style_note
    ))

    # === PART 12: TELEGRAM BOT ===
    story.append(P("Часть 12. Настройка Telegram-бота для уведомлений", style_h1))
    story.append(P(
        "Чтобы при каждой новой заявке с сайта вам в Telegram приходило сообщение с именем, "
        "телефоном и комментарием клиента — создайте бота."
    ))

    story.append(step_box(1, "Создайте бота через @BotFather",
        [
            "Откройте Telegram, найдите <b>@BotFather</b>, отправьте /newbot.",
            "Придумайте имя: например, «Жиро Чист Заявки».",
            "Придумайте username: например, <font face='Courier'>zhirochist_leads_bot</font> "
            "(должно заканчиваться на _bot).",
            "BotFather пришлёт <b>токен</b> вида <font face='Courier'>7890123456:AAHxxx...xxx</font>. "
            "Сохраните его — это «пароль» бота.",
        ]))

    story.append(step_box(2, "Узнайте свой chat_id",
        [
            "Напишите своему новому боту любое сообщение (например, «Привет»).",
            "Откройте в браузере (замените TOKEN на ваш токен):",
        ]))
    story.append(code_block("https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates"))
    story.append(P(
        "В ответе найдите строку вида <font face='Courier'>\"chat\":{\"id\": 123456789}</font>. "
        "Число 123456789 — это ваш chat_id. Запишите его."
    ))

    story.append(step_box(3, "Запишите токен и chat_id в .env",
        [
            "На сервере откройте файл .env:",
        ]))
    story.append(code_block("nano /var/www/zhirochist/.env"))
    story.append(P("Заполните строки:"))
    story.append(code_block(
        "TELEGRAM_BOT_TOKEN=7890123456:AAHxxx...xxx\n"
        "TELEGRAM_CHAT_ID=123456789"
    ))
    story.append(P("Сохраните (Ctrl+O, Enter, Ctrl+X) и перезапустите сайт:"))
    story.append(code_block("pm2 restart zhirochist"))
    story.append(P(
        "Готово! Заполните тестовую заявку на сайте — вам в Telegram придёт сообщение.",
        style_note
    ))

    # === PART 13: CONTACTS ===
    story.append(P("Часть 13. Замена контактов на реальные", style_h1))
    story.append(P(
        "В коде сайта уже стоят ваши контакты: телефон +7 (996) 213-52-20, Telegram, MAX, "
        "email malofeev-koss@ya.ru. Если нужно изменить — отредактируйте файл."
    ))

    story.append(step_box(1, "Откройте файл page.tsx",
        [
            "На сервере:",
        ]))
    story.append(code_block("nano /var/www/zhirochist/src/app/page.tsx"))
    story.append(P(
        "В начале файла (строки ~29–33) найдите блок с контактами:"
    ))
    story.append(code_block(
        "const PHONE_DISPLAY = '+7 (996) 213-52-20'\n"
        "const PHONE_TEL = '+79962135220'\n"
        "const TELEGRAM_URL = 'https://t.me/+79962135220'\n"
        "const MAX_URL = 'https://max.ru/'\n"
        "const EMAIL = 'malofeev-koss@ya.ru'"
    ))
    story.append(P(
        "Если хотите поменять MAX на прямую ссылку профиля — замените "
        "<font face='Courier'>https://max.ru/</font> на вашу ссылку вида "
        "<font face='Courier'>https://max.ru/u/ВАШ_НИК</font>."
    ))

    story.append(step_box(2, "Пересоберите и перезапустите",
        [
            "После любых изменений в коде:",
        ]))
    story.append(code_block(
        "cd /var/www/zhirochist\n"
        "bun run build\n"
        "pm2 restart zhirochist"
    ))

    # === PART 14: CHECKLIST ===
    story.append(PageBreak())
    story.append(P("Часть 14. Финальный чек-лист запуска", style_h1))
    story.append(P("Проверьте, что всё готово к работе:", style_body))

    checklist = [
        ("Аккаунт Beget зарегистрирован", "cp.beget.com открывается"),
        ("Домен .ru зарегистрирован и делегирован", "nslookup показывает IP Beget NS"),
        ("VPS KVM создан и работает", "Статус: Active в панели Beget"),
        ("IP-адрес и root-пароль сохранены", "В надёжном месте"),
        ("SSH-подключение работает", "Команда ssh root@IP выполняется"),
        ("Node.js 20 + Bun + PM2 + Nginx установлены", "node -v, bun -v, nginx -v показывают версии"),
        ("Код сайта загружен в /var/www/zhirochist", "ls -la показывает package.json и src/"),
        (".env заполнен (DATABASE_URL + Telegram)", "nano .env — строки заполнены"),
        ("База данных создана (db:push)", "Файл db/custom.db существует"),
        ("Сайт собран (bun run build)", "Без ошибок, создана папка .next"),
        ("PM2 запущен и настроен автозапуск", "pm2 status: online, pm2 startup выполнен"),
        ("Nginx настроен как прокси на :3000", "nginx -t: test is successful"),
        ("DNS A-записи @ и www указывают на сервер", "nslookup домен.ру → IP сервера"),
        ("SSL-сертификат установлен через certbot", "Сайт открывается по https://"),
        ("Сайт открывается в браузере", "https://домен.ру показывает главную"),
        ("Telegram-бот присылает уведомления о заявке", "Тестовая заявка → сообщение в TG"),
        ("Контакты на сайте реальные", "Телефон +7 996 213-52-20 и email корректны"),
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

    # === PART 15: TROUBLESHOOTING ===
    story.append(P("Часть 15. Если что-то не работает", style_h1))
    story.append(P("90 % проблем решаются перезапуском или проверкой DNS. Проверяйте в этом порядке:", style_body))

    story.append(P("Сайт не открывается по домену", style_h2))
    items = [
        "DNS ещё не обновился (подождите до 24 часов).",
        "A-запись указывает на неправильный IP — проверьте в панели Beget → Домены → DNS.",
        "Nginx не запущен: <font face='Courier'>systemctl status nginx</font> — если inactive, выполните <font face='Courier'>systemctl start nginx</font>.",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    story.append(P("Сайт открывается, но ошибка 502 Bad Gateway", style_h2))
    items = [
        "Next.js не запущен: <font face='Courier'>pm2 status</font> — zhirochist должен быть online.",
        "Если статус stopped или errored — посмотрите логи: <font face='Courier'>pm2 logs zhirochist --lines 50</font>.",
        "Перезапустите: <font face='Courier'>pm2 restart zhirochist</font>.",
        "Проверьте, что .env существует и DATABASE_URL указывает на правильный путь: <font face='Courier'>cat /var/www/zhirochist/.env</font>.",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    story.append(P("Форма отправляется, но в Telegram ничего не приходит", style_h2))
    items = [
        "Проверьте, что TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID заполнены в .env.",
        "Перезапустите сайт: <font face='Courier'>pm2 restart zhirochist</font>.",
        "Проверьте, что вы писали боту любое сообщение перед запросом chat_id (иначе бот не знает ваш chat_id).",
        "Проверьте вручную: <font face='Courier'>curl https://api.telegram.org/bot<ТОКЕН>/sendMessage -d chat_id=<CHAT_ID> -d text=test</font>.",
        "Заявки сохраняются в SQLite в любом случае: <font face='Courier'>curl http://localhost:3000/api/lead</font>.",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    story.append(P("HTTPS не работает (браузер пишет «Не защищено»)", style_h2))
    items = [
        "Certbot не отработал — повторите команду <font face='Courier'>certbot --nginx -d ВАШ_ДОМЕН.ru</font>.",
        "Убедитесь, что DNS уже смотрит на сервер (см. шаг 10.3).",
        "Дождитесь обновления DNS перед запуском certbot — иначе он не сможет проверить домен.",
        "Проверьте порты: <font face='Courier'>ufw status</font> — должны быть открыты 80 и 443. "
        "Если нет: <font face='Courier'>ufw allow 80, ufw allow 443</font>.",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    story.append(P("VPS Beget недоступен для заказа", style_h2))
    story.append(P(
        "Если на beget.com раздел VPS помечен «Временно недоступно» — это последствия кибератаки. "
        "Варианты:",
        style_body
    ))
    items = [
        "<b>Подождать</b> 1–4 недели до полного восстановления VPS Beget (следите за Telegram @beget).",
        "<b>Использовать Timeweb Cloud</b> — российский аналог, VPS от 250 ₽/мес. См. инструкцию "
        "<font face='Courier'>Инструкция_по_запуску_сайта.pdf</font> в архиве.",
        "<b>Reg.ru VPS</b> — тоже российский провайдер, VPS от 300 ₽/мес.",
        "<b>Selectel</b> — дороже, но очень надёжно для production.",
    ]
    for it in items:
        story.append(P("• " + it, style_bullet))

    story.append(Spacer(1, 18))
    story.append(P(
        "Если самостоятельно разобраться сложно — наймите фрилансера на Kwork.ru или FL.ru "
        "с задачей «Деплой Next.js на Beget VPS». Стоимость: 1 500–3 000 ₽ за полное подключение "
        "под ключ по этой инструкции.",
        style_note
    ))

    # === PART 16: ALTERNATIVES ===
    story.append(P("Часть 16. Если Beget не подойдёт — альтернативы", style_h1))
    story.append(P(
        "Если VPS Beget будет долго недоступен или вы решите использовать другого провайдера — "
        "вот проверенные российские альтернативы. Все они поддерживают Node.js, бесплатный SSL "
        "и оплату российскими картами."
    ))
    story.append(make_table(
        [
            ["Провайдер", "Цена VPS", "Регистрация домена", "Плюсы"],
            ["Timeweb Cloud", "от 250 ₽/мес", "да, .ru от 200 ₽", "Стабильный, не атакован, отличная панель"],
            ["Reg.ru", "от 300 ₽/мес", "да, .ru от 199 ₽", "Крупнейший регистратор доменов в РФ"],
            ["Selectel", "от 400 ₽/мес", "да", "Производственный уровень, SSL бесплатно"],
            ["RU-CENTER", "от 350 ₽/мес", "да", "Старейший регистратор РФ"],
        ],
        col_widths=[35 * mm, 28 * mm, 38 * mm, 65 * mm],
    ))
    story.append(Spacer(1, 10))
    story.append(P(
        "Если выберете другой провайдер — основная инструкция "
        "<font face='Courier'>Инструкция_по_запуску_сайта.pdf</font> (для Timeweb) подойдёт почти без изменений. "
        "Отличается только личный кабинет и кнопки заказа VPS."
    ))

    # === SUMMARY ===
    story.append(P("Итог", style_h1))
    story.append(P(
        "Запуск сайта на Beget состоит из 6 этапов: регистрация домена → заказ VPS KVM → "
        "подключение по SSH и установка ПО → загрузка кода и сборка → настройка Nginx и SSL → "
        "подключение домена и Telegram-бота. Если VPS Beget временно недоступен — следите за "
        "восстановлением или используйте Timeweb Cloud."
    ))
    story.append(P(
        "После успешного запуска сайт работает 24/7, автоматически перезапускается при сбоях "
        "через PM2, SSL продлевается автоматически через certbot. Заявки с формы приходят в "
        "Telegram, дублируются в SQLite-базу на сервере."
    ))

    doc.build(story)
    print(f"✓ Saved: {out}")
    print(f"  Size: {os.path.getsize(out) / 1024:.1f} KB")


if __name__ == "__main__":
    build()
