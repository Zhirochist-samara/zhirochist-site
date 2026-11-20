#!/usr/bin/env python3
"""Generate vizitki.html with embedded QR codes (PNG data URIs), price markers, and discount variant."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qr_data import QR_DATA

# ============================================================
# ЦЕНЫ — МЕНЯЙТЕ ЗДЕСЬ
# После изменений выполните:
#   python3 scripts/generate-vizitki.py
#   node skills/pdf/scripts/html2pdf-next.js scripts/vizitki.html --output download/Визитки.pdf --width 210mm --height 297mm
# ============================================================
PRICES = [
    ('Чистка до 50 л', '1 800 ₽'),
    ('50–200 л', '3 500 ₽'),
    ('200–500 л', '6 000 ₽'),
    ('500+ л', 'от 12 000 ₽'),
    ('Канализация (до 30 м)', '2 500 ₽'),
    ('Договор (от)', '4 500 ₽/мес'),
]

# ============================================================
# СКИДКА — МЕНЯЙТЕ ЗДЕСЬ
# ============================================================
DISCOUNT_PERCENT = '10'           # процент скидки
DISCOUNT_CODE = 'ЖИРО10'           # промо-код
DISCOUNT_TERMS = 'Скидка действует на первую чистку жироуловителя при предъявлении визитки. Не суммируется с договорным обслуживанием.'

# ============================================================
# Контакты — МЕНЯЙТЕ ЗДЕСЬ
# ============================================================
PHONE_DISPLAY = '+7 (996) 213-52-20'
PHONE_SHORT = '+7 996 213-52-20'
EMAIL = 'malofeev-koss@ya.ru'
TELEGRAM_URL = 't.me/+79962135220'
MAX_LINK = 'max.ru'

# ============================================================
# CSS — стили всех вариантов визиток
# ============================================================
CSS = """
  @page { size: A4; margin: 10mm; }
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0;
    font-family: "DejaVu Sans", "Liberation Sans", Arial, sans-serif;
    background: #ffffff; color: #1a1f1c;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }
  .page {
    width: 190mm; height: 277mm;
    page-break-after: always;
    overflow: hidden; display: flex; flex-direction: column;
  }
  .page:last-child { page-break-after: auto; }
  .page-header {
    border-bottom: 1px solid #0E5C3A;
    padding-bottom: 3mm; margin-bottom: 5mm;
    display: flex; justify-content: space-between; align-items: baseline;
  }
  .page-title { font-size: 10pt; font-weight: bold; color: #0E5C3A; }
  .page-meta { font-size: 8pt; color: #5C6A5F; }
  .page-footer {
    margin-top: auto; padding-top: 3mm;
    border-top: 1px dashed #D8E0D3;
    font-size: 7.5pt; color: #5C6A5F; text-align: center;
  }

  /* GRID — 8 cards (90×54mm) per A4 */
  .grid-10 {
    display: grid;
    grid-template-columns: repeat(2, 90mm);
    grid-template-rows: repeat(4, 54mm);
    gap: 4mm; justify-content: center;
    flex: 1; align-content: center;
  }
  .card {
    width: 90mm; height: 54mm;
    border: 0.5mm dashed #B0B8C0;
    overflow: hidden; position: relative; background: white;
  }
  .card-inner {
    width: 88mm; height: 52mm; margin: 1mm;
    position: relative; overflow: hidden;
  }

  /* QR CODE STYLES */
  .qr-img { width: 100%; height: 100%; display: block; object-fit: contain; }
  .qr-box-min {
    position: absolute; top: 3mm; right: 3mm;
    width: 14mm; height: 14mm; background: white;
    padding: 0.5mm; border-radius: 1mm; border: 0.3mm solid #D8E0D3;
  }
  .qr-box-det {
    position: absolute; top: 2.5mm; right: 3mm;
    width: 11mm; height: 11mm; background: white;
    padding: 0.3mm; border-radius: 0.5mm;
  }
  .qr-box-vert {
    width: 18mm; height: 18mm; background: white;
    padding: 0.5mm; border-radius: 1mm; margin: 0 auto 1mm;
  }
  .qr-box-back {
    position: absolute; bottom: 2.5mm; right: 3mm;
    width: 12mm; height: 12mm; background: white;
    padding: 0.3mm; border-radius: 0.5mm; border: 0.3mm solid #D8E0D3;
  }
  .qr-box-disc {
    width: 22mm; height: 22mm; background: white;
    padding: 0.5mm; border-radius: 1.5mm; border: 0.5mm solid #0E5C3A;
  }

  /* PRICE MARKER */
  .price-marker {
    position: absolute; top: -1mm; left: -1mm;
    background: #FEF3C7; color: #92400E;
    font-size: 5pt; font-weight: 700;
    padding: 0.3mm 1mm; border-radius: 0 0 1mm 0;
    border: 0.2mm solid #D97706;
    letter-spacing: 0.3px; text-transform: uppercase; z-index: 10;
  }

  /* VARIANT A — Minimalist */
  .card-min .card-inner {
    background: #FAF6EC; border-radius: 2mm;
    padding: 4mm 5mm; display: flex; flex-direction: column; justify-content: space-between;
    border-left: 2mm solid #0E5C3A;
  }
  .card-min .brand-row { display: flex; align-items: center; gap: 2mm; }
  .card-min .logo-circle {
    width: 9mm; height: 9mm; background: #0E5C3A; color: white;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 11pt; font-weight: 800; flex-shrink: 0;
  }
  .card-min .brand-name { font-size: 14pt; font-weight: 800; color: #0E5C3A; letter-spacing: 0.3px; line-height: 1; }
  .card-min .brand-tag { font-size: 7pt; color: #5C6A5F; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.8mm; }
  .card-min .tagline { font-size: 8pt; color: #1a1f1c; margin-top: 1mm; line-height: 1.2; padding-right: 16mm; }
  .card-min .contacts { display: flex; flex-direction: column; gap: 0.8mm; font-size: 8.5pt; padding-right: 16mm; }
  .card-min .contact-row { display: flex; align-items: center; gap: 1.5mm; }
  .card-min .contact-label { color: #5C6A5F; font-size: 7pt; width: 12mm; flex-shrink: 0; }
  .card-min .contact-value { color: #1a1f1c; font-weight: 600; }
  .card-min .phone-big { font-size: 11pt; font-weight: 800; color: #0E5C3A; line-height: 1.1; }
  .card-min .messengers { display: flex; gap: 1.5mm; margin-top: 0.5mm; }
  .card-min .messenger-pill { background: #0E5C3A; color: white; font-size: 7pt; font-weight: 700; padding: 0.5mm 1.5mm; border-radius: 1mm; }
  .card-min .messenger-pill.max { background: #7C3AED; }
  .card-min .messenger-pill.tg { background: #229ED9; }

  /* VARIANT B — Detailed */
  .card-det .card-inner { background: white; border-radius: 2mm; overflow: hidden; display: flex; flex-direction: column; }
  .card-det .top-bar { background: #0E5C3A; color: white; padding: 2.5mm 4mm; display: flex; align-items: center; gap: 2mm; }
  .card-det .top-bar .logo-circle { width: 7mm; height: 7mm; background: white; color: #0E5C3A; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 9pt; font-weight: 800; flex-shrink: 0; }
  .card-det .top-bar .brand-name { font-size: 12pt; font-weight: 800; letter-spacing: 0.3px; line-height: 1; }
  .card-det .top-bar .brand-tag { font-size: 6.5pt; opacity: 0.85; margin-top: 0.5mm; }
  .card-det .body { padding: 2mm 4mm 2.5mm; display: flex; flex-direction: column; flex: 1; background: #FAF6EC; }
  .card-det .services { font-size: 7pt; color: #1a1f1c; line-height: 1.3; margin-bottom: 1.5mm; padding-bottom: 1.5mm; border-bottom: 0.3mm solid #D8E0D3; padding-right: 12mm; }
  .card-det .services b { color: #0E5C3A; }
  .card-det .contacts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8mm 2mm; font-size: 7.5pt; }
  .card-det .contact-line { display: flex; flex-direction: column; }
  .card-det .contact-line .label { font-size: 6pt; color: #5C6A5F; text-transform: uppercase; letter-spacing: 0.5px; line-height: 1; }
  .card-det .contact-line .value { font-size: 8pt; color: #1a1f1c; font-weight: 700; line-height: 1.2; margin-top: 0.3mm; }
  .card-det .contact-line .value.phone { color: #0E5C3A; font-size: 9pt; }

  /* VARIANT C — Vertical */
  .grid-6-vert {
    display: grid; grid-template-columns: repeat(2, 54mm);
    grid-template-rows: repeat(2, 90mm);
    gap: 8mm 4mm; flex: 1; justify-content: center; align-content: center; padding-top: 2mm;
  }
  .card-vert { width: 54mm; height: 90mm; border: 0.5mm dashed #B0B8C0; overflow: hidden; background: white; }
  .card-vert .card-inner {
    width: 52mm; height: 88mm; margin: 1mm;
    background: #0E5C3A; color: white; border-radius: 2mm;
    padding: 5mm 4mm; display: flex; flex-direction: column; justify-content: space-between;
    position: relative; overflow: hidden;
  }
  .card-vert .card-inner::before {
    content: ""; position: absolute; top: 0; right: 0;
    width: 25mm; height: 25mm; background: rgba(61, 219, 181, 0.15);
    border-radius: 50%; transform: translate(8mm, -8mm);
  }
  .card-vert .brand-block { position: relative; z-index: 1; }
  .card-vert .logo-circle {
    width: 11mm; height: 11mm; background: #3DDBB5; color: #0C1F1A;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 14pt; font-weight: 800; margin-bottom: 2.5mm;
  }
  .card-vert .brand-name { font-size: 14pt; font-weight: 800; color: white; letter-spacing: 0.5px; line-height: 1; }
  .card-vert .brand-tag { font-size: 7pt; color: #3DDBB5; text-transform: uppercase; letter-spacing: 1.2px; margin-top: 1mm; }
  .card-vert .tagline {
    font-size: 8pt; color: rgba(255, 255, 255, 0.85); margin-top: 2mm; line-height: 1.3;
    border-top: 0.3mm solid rgba(61, 219, 181, 0.4); padding-top: 2mm; position: relative; z-index: 1;
  }
  .card-vert .contacts { position: relative; z-index: 1; }
  .card-vert .phone-big { font-size: 11pt; font-weight: 800; color: white; line-height: 1.1; margin-bottom: 1.5mm; }
  .card-vert .messengers-row { display: flex; gap: 1.5mm; margin-bottom: 1.5mm; }
  .card-vert .messenger-pill { background: rgba(255, 255, 255, 0.15); color: white; font-size: 6.5pt; font-weight: 700; padding: 0.8mm 1.8mm; border-radius: 1mm; border: 0.3mm solid rgba(255, 255, 255, 0.3); }
  .card-vert .messenger-pill.tg { background: #229ED9; border-color: #229ED9; }
  .card-vert .messenger-pill.max { background: #7C3AED; border-color: #7C3AED; }
  .card-vert .email { font-size: 7.5pt; color: rgba(255, 255, 255, 0.85); margin-top: 1mm; word-break: break-all; }
  .card-vert .geo { font-size: 7pt; color: #3DDBB5; text-align: center; margin-top: 2mm; padding-top: 2mm; border-top: 0.3mm solid rgba(61, 219, 181, 0.4); position: relative; z-index: 1; }

  /* BACK SIDE */
  .card-back .card-inner {
    background: #FAF6EC; border-radius: 2mm; padding: 3.5mm 4mm;
    display: flex; flex-direction: column; border: 0.3mm solid #D8E0D3; position: relative;
  }
  .card-back .card-inner::before {
    content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 1.5mm;
    background: #0E5C3A; border-radius: 2mm 2mm 0 0;
  }
  .card-back .back-title {
    font-size: 9pt; font-weight: 800; color: #0E5C3A; text-align: center;
    margin-top: 1.5mm; margin-bottom: 1.5mm; text-transform: uppercase; letter-spacing: 0.8px;
  }
  .card-back .services-list { font-size: 7pt; color: #1a1f1c; line-height: 1.4; margin-bottom: 1.5mm; padding-right: 14mm; }
  .card-back .services-list .row {
    display: flex; justify-content: space-between; padding: 0.3mm 0;
    border-bottom: 0.2mm dotted #D8E0D3;
  }
  .card-back .services-list .row:last-child { border-bottom: none; }
  .card-back .services-list .price { color: #0E5C3A; font-weight: 700; }
  .card-back .footer-note {
    margin-top: auto; font-size: 6.5pt; color: #5C6A5F; text-align: center; line-height: 1.3;
    padding-top: 1mm; border-top: 0.2mm dashed #D8E0D3; padding-right: 14mm;
  }
  .card-back .footer-note b { color: #0E5C3A; }

  /* DISCOUNT CARD */
  .card-disc .card-inner {
    background: white; border-radius: 2mm; overflow: hidden;
    display: flex; flex-direction: column; position: relative; border: 0.5mm solid #0E5C3A;
  }
  .card-disc .discount-band { background: #FEF3C7; border-bottom: 0.5mm solid #D97706; padding: 1.5mm 4mm; text-align: center; color: #92400E; }
  .card-disc .discount-band .label { font-size: 7pt; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; line-height: 1; }
  .card-disc .discount-band .percent { font-size: 16pt; font-weight: 800; color: #D97706; line-height: 1; margin-top: 0.5mm; }
  .card-disc .promo-row { background: #0E5C3A; color: white; padding: 1.5mm 4mm; text-align: center; }
  .card-disc .promo-row .label { font-size: 6pt; opacity: 0.85; letter-spacing: 1px; text-transform: uppercase; line-height: 1; }
  .card-disc .promo-row .code { font-size: 12pt; font-weight: 800; color: #3DDBB5; letter-spacing: 1.5px; line-height: 1.1; margin-top: 0.5mm; }
  .card-disc .body-disc { padding: 2mm 4mm 2mm; display: flex; align-items: center; gap: 3mm; flex: 1; background: #FAF6EC; }
  .card-disc .body-disc .text-side { flex: 1; font-size: 7pt; color: #1a1f1c; line-height: 1.3; }
  .card-disc .body-disc .text-side .brand { font-size: 9pt; font-weight: 800; color: #0E5C3A; margin-bottom: 0.5mm; }
  .card-disc .body-disc .text-side .phone { font-size: 9pt; font-weight: 800; color: #0E5C3A; margin-top: 1mm; line-height: 1.1; }
  .card-disc .body-disc .text-side .meta { font-size: 6.5pt; color: #5C6A5F; margin-top: 0.5mm; }
"""

# ============================================================
# Карточные шаблоны
# ============================================================
def minimal_card(qr_name='phone'):
    qr_uri = QR_DATA[qr_name]
    return f'''    <div class="card card-min"><div class="card-inner">
      <div class="qr-box-min"><img src="{qr_uri}" class="qr-img" alt="QR"/></div>
      <div>
        <div class="brand-row">
          <div class="logo-circle">Ж</div>
          <div>
            <div class="brand-name">ЖИРОЧИСТ</div>
            <div class="brand-tag">Самара</div>
          </div>
        </div>
        <div class="tagline">Чистка жироуловителей и канализации</div>
      </div>
      <div class="contacts">
        <div class="phone-big">{PHONE_DISPLAY}</div>
        <div class="messengers">
          <span class="messenger-pill tg">Telegram</span>
          <span class="messenger-pill max">MAX</span>
        </div>
        <div class="contact-row">
          <span class="contact-label">email</span>
          <span class="contact-value">{EMAIL}</span>
        </div>
      </div>
    </div></div>'''

def detailed_card(qr_name='telegram'):
    qr_uri = QR_DATA[qr_name]
    return f'''    <div class="card card-det"><div class="card-inner">
      <div class="top-bar">
        <div class="logo-circle">Ж</div>
        <div>
          <div class="brand-name">ЖИРОЧИСТ</div>
          <div class="brand-tag">Самара · Самозанятый</div>
        </div>
      </div>
      <div class="qr-box-det"><img src="{qr_uri}" class="qr-img" alt="QR"/></div>
      <div class="body">
        <div class="services">
          <b>Чистка жироуловителей</b> · чистка канализации · договорное обслуживание · документы для Роспотребнадзора
        </div>
        <div class="contacts-grid">
          <div class="contact-line">
            <div class="label">Телефон</div>
            <div class="value phone">{PHONE_SHORT}</div>
          </div>
          <div class="contact-line">
            <div class="label">Telegram</div>
            <div class="value">{TELEGRAM_URL}</div>
          </div>
          <div class="contact-line">
            <div class="label">MAX</div>
            <div class="value">{MAX_LINK}</div>
          </div>
          <div class="contact-line">
            <div class="label">Email</div>
            <div class="value">{EMAIL}</div>
          </div>
        </div>
      </div>
    </div></div>'''

def back_card():
    qr_uri = QR_DATA['site']
    rows = '\n'.join(
        f'        <div class="row"><span class="name">{name}</span><span class="price">{price}</span></div>'
        for name, price in PRICES
    )
    return f'''    <div class="card card-back"><div class="card-inner">
      <span class="price-marker">ЦЕНЫ — править в generate-vizitki.py</span>
      <div class="back-title">Услуги и тарифы</div>
      <div class="services-list">
{rows}
      </div>
      <div class="qr-box-back"><img src="{qr_uri}" class="qr-img" alt="QR"/></div>
      <div class="footer-note">
        <b>Выезд за 3 часа · Самара и пригород</b><br>
        Документы для Роспотребнадзора · без НДС
      </div>
    </div></div>'''

def vertical_card(qr_name='phone'):
    qr_uri = QR_DATA[qr_name]
    return f'''    <div class="card-vert"><div class="card-inner">
      <div class="brand-block">
        <div class="logo-circle">Ж</div>
        <div class="brand-name">ЖИРОЧИСТ</div>
        <div class="brand-tag">Самара</div>
        <div class="tagline">Чистка жироуловителей и канализации · Самозанятый</div>
      </div>
      <div class="contacts">
        <div class="phone-big">{PHONE_SHORT}</div>
        <div class="messengers-row">
          <span class="messenger-pill tg">Telegram</span>
          <span class="messenger-pill max">MAX</span>
        </div>
        <div class="qr-box-vert"><img src="{qr_uri}" class="qr-img" alt="QR"/></div>
        <div class="email">{EMAIL}</div>
        <div class="geo">Самара и пригороды</div>
      </div>
    </div></div>'''

def discount_card():
    qr_uri = QR_DATA['site']
    return f'''    <div class="card card-disc"><div class="card-inner">
      <span class="price-marker">СКИДКА — править в generate-vizitki.py</span>
      <div class="discount-band">
        <div class="label">Скидка по визитке</div>
        <div class="percent">−{DISCOUNT_PERCENT}%</div>
      </div>
      <div class="promo-row">
        <div class="label">Промо-код</div>
        <div class="code">{DISCOUNT_CODE}</div>
      </div>
      <div class="body-disc">
        <div class="text-side">
          <div class="brand">ЖИРОЧИСТ Самара</div>
          <div>Чистка жироуловителей и канализации</div>
          <div class="phone">{PHONE_SHORT}</div>
          <div class="meta">Telegram · MAX · {EMAIL}</div>
        </div>
        <div class="qr-box-disc"><img src="{qr_uri}" class="qr-img" alt="QR"/></div>
      </div>
    </div></div>'''

# ============================================================
# Сборка HTML
# ============================================================
page1_cards = '\n'.join(minimal_card('phone') for _ in range(8))
page2_cards = '\n'.join(detailed_card('telegram') for _ in range(8))
page3_cards = '\n'.join(back_card() for _ in range(8))
page4_cards = '\n'.join(vertical_card('phone') for _ in range(4))
page5_cards = '\n'.join(discount_card() for _ in range(8))

price_table_rows = '\n'.join(
    f'      <tr><td style="padding:1.5mm 3mm; border-bottom:0.3mm solid #D8E0D3;"><b>{name}</b></td><td style="padding:1.5mm 3mm; border-bottom:0.3mm solid #D8E0D3; color:#0E5C3A; font-weight:700;">{price}</td></tr>'
    for name, price in PRICES
)

html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Визитки ЖИРОЧИСТ Самара — с QR и скидкой</title>
<style>
{CSS}
</style>
</head>
<body>

<!-- ============ PAGE 1: VARIANT A — Minimalist with QR ============ -->
<div class="page">
  <div class="page-header">
    <div class="page-title">ЖИРОЧИСТ Самара · Вариант A — минималистичная с QR</div>
    <div class="page-meta">Лист 1/6 · 90×54 мм · 8 шт. · QR ведёт на звонок</div>
  </div>
  <div class="grid-10">
{page1_cards}
  </div>
  <div class="page-footer">
    Печатать на плотной бумаге А4 (200–300 г/м²) · резать по пунктирной линии
  </div>
</div>

<!-- ============ PAGE 2: VARIANT B — Detailed with services + QR ============ -->
<div class="page">
  <div class="page-header">
    <div class="page-title">ЖИРОЧИСТ Самара · Вариант B — развёрнутая с QR</div>
    <div class="page-meta">Лист 2/6 · 90×54 мм · 8 шт. · QR ведёт в Telegram</div>
  </div>
  <div class="grid-10">
{page2_cards}
  </div>
  <div class="page-footer">
    Развёрнутая визитка с услугами · для общепита и производств
  </div>
</div>

<!-- ============ PAGE 3: BACK SIDE with prices + QR to site ============ -->
<div class="page">
  <div class="page-header">
    <div class="page-title">ЖИРОЧИСТ Самара · Оборотная сторона с прайсом</div>
    <div class="page-meta">Лист 3/6 · 90×54 мм · 8 шт. · QR ведёт на сайт</div>
  </div>
  <div class="grid-10">
{page3_cards}
  </div>
  <div class="page-footer">
    <b style="color:#92400E;">⚠ ЦЕНЫ МЕНЯЮТСЯ В ФАЙЛЕ:</b> откройте <code style="background:#FEF3C7; padding:0.5mm 1.5mm;">scripts/generate-vizitki.py</code>, найдите <code style="background:#FEF3C7; padding:0.5mm 1.5mm;">PRICES = [</code> и отредактируйте значения
  </div>
</div>

<!-- ============ PAGE 4: VARIANT C — Vertical premium with QR ============ -->
<div class="page">
  <div class="page-header">
    <div class="page-title">ЖИРОЧИСТ Самара · Вариант C — вертикальная премиум с QR</div>
    <div class="page-meta">Лист 4/6 · 54×90 мм · 4 шт.</div>
  </div>
  <div class="grid-6-vert">
{page4_cards}
  </div>
  <div class="page-footer">
    Вертикальная премиум-визитка · тёмный фон, акцент бирюзовый
  </div>
</div>

<!-- ============ PAGE 5: DISCOUNT CARDS ============ -->
<div class="page">
  <div class="page-header">
    <div class="page-title">ЖИРОЧИСТ Самара · Вариант D — визитка со скидкой {DISCOUNT_PERCENT}%</div>
    <div class="page-meta">Лист 5/6 · 90×54 мм · 8 шт. · промо-код {DISCOUNT_CODE}</div>
  </div>
  <div class="grid-10">
{page5_cards}
  </div>
  <div class="page-footer">
    <b style="color:#92400E;">⚠ СКИДКА МЕНЯЕТСЯ В ФАЙЛЕ:</b> откройте <code style="background:#FEF3C7; padding:0.5mm 1.5mm;">scripts/generate-vizitki.py</code>, найдите <code style="background:#FEF3C7; padding:0.5mm 1.5mm;">DISCOUNT_PERCENT</code> и <code style="background:#FEF3C7; padding:0.5mm 1.5mm;">DISCOUNT_CODE</code>
  </div>
</div>

<!-- ============ PAGE 6: USAGE GUIDE ============ -->
<div class="page">
  <div class="page-header">
    <div class="page-title">ЖИРОЧИСТ Самара · Где менять цены, скидку и QR-коды</div>
    <div class="page-meta">Лист 6/6 · Руководство</div>
  </div>
  <div style="padding: 5mm 4mm; font-size: 10pt; line-height: 1.5;">

    <h2 style="color: #0E5C3A; font-size: 13pt; margin: 0 0 3mm;">Где менять ЦЕНЫ (оборот, лист 3)</h2>
    <p style="margin: 0 0 3mm;">Все цены собраны в Python-словаре <code style="background:#FEF3C7; padding:0.5mm 1.5mm; color:#92400E; font-weight:700;">PRICES</code> в файле <code style="background:#F1EDE1; padding:0.5mm 1.5mm;">scripts/generate-vizitki.py</code> (примерно строка 17).</p>
    <pre style="background:#F1EDE1; padding:3mm; font-size:8.5pt; line-height:1.4; border-left:2mm solid #0E5C3A; margin:0 0 3mm; white-space:pre-wrap;">PRICES = [
    ('Чистка до 50 л', '1 800 ₽'),         # ← меняйте здесь
    ('50–200 л', '3 500 ₽'),
    ('200–500 л', '6 000 ₽'),
    ('500+ л', 'от 12 000 ₽'),
    ('Канализация (до 30 м)', '2 500 ₽'),
    ('Договор (от)', '4 500 ₽/мес'),
]</pre>
    <p style="margin: 0 0 4mm;">После изменений выполните:</p>
    <pre style="background:#F1EDE1; padding:3mm; font-size:8.5pt; border-left:2mm solid #0E5C3A; margin:0 0 4mm;">python3 scripts/generate-vizitki.py
node skills/pdf/scripts/html2pdf-next.js scripts/vizitki.html \\
  --output download/Визитки.pdf --width 210mm --height 297mm</pre>

    <h2 style="color: #0E5C3A; font-size: 13pt; margin: 4mm 0 3mm;">Где менять СКИДКУ (лист 5)</h2>
    <p style="margin: 0 0 3mm;">В файле <code style="background:#F1EDE1; padding:0.5mm 1.5mm;">scripts/generate-vizitki.py</code> найдите переменные (около строки 30):</p>
    <pre style="background:#FEF3C7; padding:3mm; font-size:8.5pt; line-height:1.4; border-left:2mm solid #D97706; margin:0 0 3mm; white-space:pre-wrap;">DISCOUNT_PERCENT = '10'              # ← процент скидки
DISCOUNT_CODE = 'ЖИРО10'               # ← промо-код
DISCOUNT_TERMS = 'Скидка действует...'  # ← условия</pre>
    <p style="margin: 0 0 4mm;">Например: <code style="background:#F1EDE1; padding:0.5mm 1.5mm;">DISCOUNT_PERCENT = '15'</code> и <code style="background:#F1EDE1; padding:0.5mm 1.5mm;">DISCOUNT_CODE = 'ЖИР15'</code> — получится скидка 15%.</p>

    <h2 style="color: #0E5C3A; font-size: 13pt; margin: 4mm 0 3mm;">Где менять QR-коды</h2>
    <p style="margin: 0 0 3mm;">QR-коды сейчас ведут на:</p>
    <ul style="margin: 0 0 3mm; padding-left: 6mm; font-size: 9pt;">
      <li><b>Лист 1 (минималистичная)</b> — <code style="background:#F1EDE1; padding:0.5mm 1.5mm;">tel:+79962135220</code> (звонок)</li>
      <li><b>Лист 2 (развёрнутая)</b> — <code style="background:#F1EDE1; padding:0.5mm 1.5mm;">https://t.me/+79962135220</code> (Telegram)</li>
      <li><b>Лист 3 (оборот)</b> — <code style="background:#F1EDE1; padding:0.5mm 1.5mm;">https://zhirochist-samara.ru</code> (сайт — заглушка)</li>
      <li><b>Лист 4 (вертикальная)</b> — <code style="background:#F1EDE1; padding:0.5mm 1.5mm;">tel:+79962135220</code></li>
      <li><b>Лист 5 (скидка)</b> — <code style="background:#F1EDE1; padding:0.5mm 1.5mm;">https://zhirochist-samara.ru</code></li>
    </ul>
    <p style="margin: 0 0 4mm;">Чтобы создать новый QR (например, после регистрации домена):</p>
    <pre style="background:#F1EDE1; padding:3mm; font-size:8.5pt; border-left:2mm solid #0E5C3A; margin:0 0 4mm;"># Откройте scripts/qr_data.py — там лежат data URI всех QR
# Чтобы перегенерировать все QR (например, при смене домена):
python3 -c "
import qrcode, base64
from io import BytesIO
qr = qrcode.QRCode(box_size=10, border=2)
qr.add_data('https://ВАШ-ДОМЕН.ru')
qr.make(fit=True)
img = qr.make_image(fill_color='#0E5C3A', back_color='white')
buf = BytesIO(); img.save(buf, format='PNG')
print('data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode())
"
# Скопируйте вывод в scripts/qr_data.py под ключ 'site'</pre>

    <h2 style="color: #0E5C3A; font-size: 13pt; margin: 4mm 0 3mm;">Текущие цены и скидка — сводка</h2>
    <table style="width:100%; border-collapse:collapse; font-size:9pt; margin-bottom:3mm;">
      <tr style="background:#0E5C3A; color:white;">
        <th style="padding:2mm 3mm; text-align:left;">Услуга</th>
        <th style="padding:2mm 3mm; text-align:left;">Цена</th>
      </tr>
{price_table_rows}
    </table>
    <p style="margin: 0 0 2mm; background:#FEF3C7; padding:2mm 3mm; border-left:2mm solid #D97706;">
      <b>Скидка по визитке:</b> −{DISCOUNT_PERCENT}% промо-код <b>{DISCOUNT_CODE}</b><br>
      <span style="font-size:8.5pt;">{DISCOUNT_TERMS}</span>
    </p>

    <h2 style="color: #0E5C3A; font-size: 13pt; margin: 4mm 0 3mm;">Какие визитки выбрать</h2>
    <p style="margin: 0 0 2mm;"><b>A + оборот</b> — для управляющих кафе и ресторанов.</p>
    <p style="margin: 0 0 2mm;"><b>B</b> — для владельцев производств.</p>
    <p style="margin: 0 0 2mm;"><b>C</b> — для сетевых ресторанов (премиум).</p>
    <p style="margin: 0 0 2mm;"><b>D (скидочная)</b> — для раздачи новым клиентам и на мероприятиях.</p>
  </div>
  <div class="page-footer">
    ЖИРОЧИСТ Самара · Визитки с QR · 6 листов А4 (5 вариантов + руководство)
  </div>
</div>

</body>
</html>
'''

with open('scripts/vizitki.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('✓ vizitki.html обновлён')
print('  Размер:', round(len(html) / 1024, 1), 'KB')
print('  QR-кодов встроено: 3 (phone, telegram, site) — как PNG data URI')
print('  Вариантов визиток: 5 (A, B, C, D скидочная, оборотная)')
print()
print('Текущие цены:')
for name, price in PRICES:
    print(f'  {name}: {price}')
print()
print(f'Скидка: −{DISCOUNT_PERCENT}%, промо-код: {DISCOUNT_CODE}')
print()
print('Чтобы изменить цены или скидку:')
print('  1. Откройте scripts/generate-vizitki.py в текстовом редакторе')
print('  2. Найдите блок PRICES = [...] (строки 17-24) или DISCOUNT_* (строки 30-32)')
print('  3. Отредактируйте значения')
print('  4. Выполните: python3 scripts/generate-vizitki.py')
print('  5. Затем: node skills/pdf/scripts/html2pdf-next.js scripts/vizitki.html --output download/Визитки.pdf --width 210mm --height 297mm')
