'use client'

import { useState } from 'react'
import {
  Phone,
  MessageCircle,
  Send,
  Mail,
  Clock,
  ShieldCheck,
  Leaf,
  Truck,
  Droplets,
  FileText,
  Star,
  MapPin,
  Wrench,
  CalendarClock,
  CheckCircle2,
  ChevronDown,
  Menu,
  X,
  Zap,
  Users,
  Building2,
  Utensils,
} from 'lucide-react'

const PHONE_DISPLAY = '+7 (996) 213-52-20'
const PHONE_TEL = '+79962135220'
const TELEGRAM_URL = 'https://t.me/+79962135220'
const MAX_URL = 'https://max.ru/'
const EMAIL = 'malofeev-koss@ya.ru'

const services = [
  {
    icon: Droplets,
    title: 'Чистка жироуловителей',
    desc: 'Механическая и гидродинамическая очистка жироуловителей всех типов — от бытовых сепараторов под мойкой до промышленных цеховых установок объёмом 1000+ литров.',
    points: [
      'Удаление жировой корки и осадка',
      'Промывка и дезинфекция корпуса',
      'Проверка работы поплавков и клапанов',
      'Акт выполненных работ для Роспотребнадзора',
    ],
    price: 'от 1 800 ₽',
  },
  {
    icon: Wrench,
    title: 'Чистка канализации',
    desc: 'Устранение жировых пробок и засоров в трубах канализации пищевых производств и общепита. Гидродинамическая промывка до полного восстановления сечения.',
    points: [
      'Диагностика места засора',
      'Гидродинамическая промывка до 30 м',
      'Удаление жировых отложений со стенок',
      'Профилактическая обработка',
    ],
    price: 'от 2 500 ₽',
  },
  {
    icon: CalendarClock,
    title: 'Договорное обслуживание',
    desc: 'Регулярное обслуживание по графику: раз в месяц, в две недели или в квартал. Фиксированная стоимость, приоритетный выезд, отчётность и напоминания о следующей чистке.',
    points: [
      'Фиксированный график визитов',
      'Приоритетный выезд в день обращения',
      'Стикеры с датами чистки на оборудование',
      'Скидка 10% к разовому прайсу',
    ],
    price: 'от 4 500 ₽/мес',
  },
]

const advantages = [
  {
    icon: Zap,
    title: 'Выезд за 3 часа',
    desc: 'Принимаю заявки с 7:00 до 22:00. Экстренный выезд по Самаре — в течение 3 часов.',
  },
  {
    icon: ShieldCheck,
    title: 'Документы для проверок',
    desc: 'Акт выполненных работ и журнал обслуживания — готовы к проверке Роспотребнадзора.',
  },
  {
    icon: Leaf,
    title: 'Экологичная утилизация',
    desc: 'Жировые отходы передаём лицензированному партнёру на переработку, а не в канализацию.',
  },
  {
    icon: FileText,
    title: 'Самозанятый — без НДС',
    desc: 'Работаю как самозанятый: чек через «Мой налог», без НДС, цена ниже, чем у компаний.',
  },
]

const pricing = [
  {
    volume: 'до 50 л',
    target: 'Бар, пекарня, кофейня, малое кафе',
    price: '1 800 ₽',
    time: '30–45 минут',
    popular: false,
  },
  {
    volume: '50–200 л',
    target: 'Ресторан, кафе, столовая, фастфуд',
    price: '3 500 ₽',
    time: '45–60 минут',
    popular: true,
  },
  {
    volume: '200–500 л',
    target: 'Сетевой ресторан, пищевое производство',
    price: '6 000 ₽',
    time: '1–1,5 часа',
    popular: false,
  },
  {
    volume: '500+ л',
    target: 'Завод, фабрика-кухня, больница, школа',
    price: 'от 12 000 ₽',
    time: '2–3 часа',
    popular: false,
  },
]

const segments = [
  {
    icon: Utensils,
    title: 'Общепит',
    examples: 'Рестораны, кафе, столовые, фастфуд',
    volume: '50–500 л',
    frequency: 'Раз в месяц',
    desc: 'Основной сегмент. Требования СанПиН 2.3.6.1079-01 обязывают заведение иметь рабочий жироуловитель и журнал его обслуживания. Чек стабильный, частота регулярная.',
  },
  {
    icon: Users,
    title: 'Малый общепит',
    examples: 'Бары, пекарни, кофейни, кулинарии',
    volume: 'до 50 л',
    frequency: 'Раз в 1–2 месяца',
    desc: 'Малый жироуловитель под мойкой. Чек невысокий, но клиентов много и почти все на повторных договорах. Идеальный сегмент для старта.',
  },
  {
    icon: Building2,
    title: 'Производство',
    examples: 'Пищевые цеха, школьные и больничные кухни, фабрики-кухни',
    volume: '500+ л',
    frequency: 'Раз в 2–4 недели',
    desc: 'Высокий чек, но более сложное оборудование. Часто требуется договорное обслуживание и документооборот. Жёсткие требования к охране труда.',
  },
]

const steps = [
  { num: '1', title: 'Заявка', desc: 'Звонок, WhatsApp или форма на сайте. Уточняю тип жироуловителя и объём.' },
  { num: '2', title: 'Выезд', desc: 'Приезжаю в течение 3 часов по Самаре или согласованного времени в пригороде.' },
  { num: '3', title: 'Чистка', desc: 'Удаляю жировую массу, промываю корпус, проверяю работу узлов. 30 минут – 3 часа.' },
  { num: '4', title: 'Документы', desc: 'Подписываем акт, клею стикер с датой следующей чистки, отправляю чек через «Мой налог».' },
]

const areas = [
  'Самара (все районы)',
  'Новокуйбышевск',
  'Чапаевск',
  'Кинель',
  'Волжский (посёлок)',
  'Пригород Самары',
]

const faq = [
  {
    q: 'Как часто нужно чистить жироуловитель?',
    a: 'По СанПиН — не реже одного раза в квартал. На практике рестораны и кафе с интенсивной кухней чистят раз в месяц, бары и пекарни — раз в 2 месяца, производства — раз в 2–4 недели. После первой чистки я рекомендую оптимальный интервал под вашу нагрузку.',
  },
  {
    q: 'Какие документы вы выдаёте?',
    a: 'Акт выполненных работ с указанием объёма и даты чистки, стикер на оборудование с датой следующей чистки, чек через приложение «Мой налог». По запросу — журнал обслуживания жироуловителя для Роспотребнадзора.',
  },
  {
    q: 'Вы увозите жировые отходы?',
    a: 'Самозанятый не имеет лицензии на транспортировку отходов, поэтому откачанную жировую массу я передаю партнёру — лицензированной компании по вывозу и переработке. В договоре на обслуживание этот пункт прописан отдельно.',
  },
  {
    q: 'Можно ли заключить договор на регулярное обслуживание?',
    a: 'Да, это выгоднее на 10% от разового прайса. Фиксируем график визитов, вы получаете приоритетный выезд в случае аварийной ситуации и напоминание в WhatsApp за 3 дня до следующей чистки.',
  },
  {
    q: 'Вы работаете с юридическими лицами?',
    a: 'Да. Самозанятый может работать с юрлицами — ставка налога 6%, чек формируется через «Мой налог». Для постоянных клиентов заключаю договор оказания услуг.',
  },
  {
    q: 'В какое время вы выезжаете?',
    a: 'Принимаю заявки с 7:00 до 22:00 ежедневно. Экстренный выезд по Самаре — в течение 3 часов. В пригород (Новокуйбышевск, Чапаевск, Кинель) — по согласованию, обычно в день заявки или на следующий день.',
  },
]

export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [openFaq, setOpenFaq] = useState<number | null>(0)
  const [form, setForm] = useState({ name: '', phone: '', service: 'Чистка жироуловителя', address: '', comment: '' })
  const [status, setStatus] = useState<'idle' | 'loading' | 'ok' | 'err'>('idle')
  const [errorMsg, setErrorMsg] = useState('')

  const navLinks = [
    { href: '#services', label: 'Услуги' },
    { href: '#pricing', label: 'Тарифы' },
    { href: '#segments', label: 'Кому подходит' },
    { href: '#process', label: 'Как работаю' },
    { href: '#contacts', label: 'Контакты' },
  ]

  // Ключ Web3Forms — получите на https://web3forms.com (бесплатно, без регистрации)
  // Вставьте свой email → придёт access key → вставьте его в .env как NEXT_PUBLIC_WEB3FORMS_KEY
  // Если ключ не задан, форма попытается отправить через серверный /api/lead (для VPS-версии)
  const WEB3FORMS_KEY = process.env.NEXT_PUBLIC_WEB3FORMS_KEY || ''

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setStatus('loading')
    setErrorMsg('')
    try {
      let ok = false
      let errorMsg = ''

      if (WEB3FORMS_KEY) {
        // Статический режим (SourceCraft Sites) — отправка через Web3Forms
        const res = await fetch('https://api.web3forms.com/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({
            access_key: WEB3FORMS_KEY,
            name: form.name,
            phone: form.phone,
            service: form.service,
            address: form.address || '',
            comment: form.comment || '',
            subject: 'Новая заявка с сайта ЖИРОЧИСТ Самара',
            from: 'ЖИРОЧИСТ Самара <noreply@zhirochist-samara.ru>',
          }),
        })
        const data = await res.json()
        ok = data.success
        if (!ok) errorMsg = data.message || 'Не удалось отправить заявку'
      } else {
        // Серверный режим (VPS) — отправка через /api/lead с сохранением в SQLite + Telegram
        const res = await fetch('/api/lead', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(form),
        })
        const data = await res.json()
        ok = data.ok
        if (!ok) errorMsg = data.error || 'Не удалось отправить заявку'
      }

      if (ok) {
        setStatus('ok')
        setForm({ name: '', phone: '', service: 'Чистка жироуловителя', address: '', comment: '' })
      } else {
        setStatus('err')
        setErrorMsg(errorMsg)
      }
    } catch {
      setStatus('err')
      setErrorMsg('Ошибка сети. Позвоните или напишите в Telegram.')
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-[#faf6ec]/90 backdrop-blur border-b border-border">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 lg:h-20">
            <a href="#top" className="flex items-center gap-2">
              <div className="w-9 h-9 lg:w-10 lg:h-10 rounded-lg bg-primary flex items-center justify-center">
                <Leaf className="w-5 h-5 lg:w-6 lg:h-6 text-primary-foreground" />
              </div>
              <div className="flex flex-col leading-tight">
                <span className="text-lg lg:text-xl font-extrabold tracking-tight text-primary">ЖИРОЧИСТ</span>
                <span className="text-[10px] lg:text-xs text-muted-foreground uppercase tracking-wider">Самара</span>
              </div>
            </a>

            <nav className="hidden lg:flex items-center gap-7">
              {navLinks.map((l) => (
                <a key={l.href} href={l.href} className="text-sm font-medium text-foreground/80 hover:text-primary transition-colors">
                  {l.label}
                </a>
              ))}
            </nav>

            <div className="flex items-center gap-2">
              <a
                href={`tel:${PHONE_TEL}`}
                className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground font-semibold hover:bg-primary/90 transition-colors"
              >
                <Phone className="w-4 h-4" />
                <span className="text-sm">{PHONE_DISPLAY}</span>
              </a>
              <button
                onClick={() => setMenuOpen(!menuOpen)}
                className="lg:hidden p-2 rounded-md hover:bg-muted"
                aria-label="Меню"
              >
                {menuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>

          {menuOpen && (
            <nav className="lg:hidden pb-4 flex flex-col gap-2 border-t border-border pt-3">
              {navLinks.map((l) => (
                <a
                  key={l.href}
                  href={l.href}
                  onClick={() => setMenuOpen(false)}
                  className="text-sm font-medium py-2 px-2 rounded hover:bg-muted"
                >
                  {l.label}
                </a>
              ))}
              <a href={`tel:${PHONE_TEL}`} className="mt-2 flex items-center gap-2 px-4 py-3 rounded-lg bg-primary text-primary-foreground font-semibold">
                <Phone className="w-4 h-4" />
                <span>{PHONE_DISPLAY}</span>
              </a>
            </nav>
          )}
        </div>
      </header>

      {/* Hero */}
      <section id="top" className="relative overflow-hidden bg-gradient-to-br from-[#0e5c3a] to-[#0a3f27] text-white">
        <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 20% 30%, white 1px, transparent 1px), radial-gradient(circle at 70% 60%, white 1px, transparent 1px)', backgroundSize: '60px 60px' }} />
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative py-16 lg:py-24">
          <div className="grid lg:grid-cols-12 gap-8 items-center">
            <div className="lg:col-span-7">
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/10 border border-white/20 mb-5">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-xs font-medium tracking-wide">На связи с 7:00 до 22:00 · Самара и пригород</span>
              </div>
              <h1 className="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-extrabold leading-[1.1] tracking-tight">
                Чистка жироуловителей <br className="hidden sm:block" />и канализации в Самаре
              </h1>
              <p className="mt-5 text-base lg:text-lg text-white/85 max-w-xl">
                Самозанятый специалист. Выезжаю за 3 часа, выдаю акт для Роспотребнадзора,
                работаю с общепитом, малым бизнесом и пищевыми производствами. Без НДС —
                дешевле крупных компаний.
              </p>

              <div className="mt-7 flex flex-wrap gap-3">
                <a
                  href={`tel:${PHONE_TEL}`}
                  className="inline-flex items-center gap-2 px-5 py-3 rounded-lg bg-white text-primary font-semibold hover:bg-white/95 transition-colors"
                >
                  <Phone className="w-5 h-5" />
                  Позвонить
                </a>
                <a
                  href={MAX_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-3 rounded-lg bg-[#7C3AED] text-white font-semibold hover:bg-[#6D28D9] transition-colors"
                >
                  <MessageCircle className="w-5 h-5" />
                  MAX
                </a>
                <a
                  href={TELEGRAM_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-3 rounded-lg bg-[#229ED9] text-white font-semibold hover:bg-[#1d8cc2] transition-colors"
                >
                  <Send className="w-5 h-5" />
                  Telegram
                </a>
              </div>

              <div className="mt-8 grid grid-cols-3 gap-4 max-w-lg">
                <div>
                  <div className="text-2xl lg:text-3xl font-extrabold">3 ч</div>
                  <div className="text-xs lg:text-sm text-white/70 mt-1">выезд по Самаре</div>
                </div>
                <div>
                  <div className="text-2xl lg:text-3xl font-extrabold">120+</div>
                  <div className="text-xs lg:text-sm text-white/70 mt-1">точек обслуживается</div>
                </div>
                <div>
                  <div className="text-2xl lg:text-3xl font-extrabold">4 года</div>
                  <div className="text-xs lg:text-sm text-white/70 mt-1">опыт работы</div>
                </div>
              </div>
            </div>

            <div className="lg:col-span-5">
              <div className="bg-white/95 rounded-2xl p-6 shadow-2xl text-foreground">
                <h3 className="text-lg font-bold mb-1">Оставить заявку</h3>
                <p className="text-sm text-muted-foreground mb-4">Перезвоню в течение 15 минут в рабочее время</p>
                <form onSubmit={submit} className="space-y-3">
                  <div>
                    <label className="block text-xs font-medium text-muted-foreground mb-1">Имя</label>
                    <input
                      type="text"
                      required
                      value={form.name}
                      onChange={(e) => setForm({ ...form, name: e.target.value })}
                      className="w-full px-3 py-2.5 rounded-md border border-input bg-card text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                      placeholder="Как к вам обращаться"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-muted-foreground mb-1">Телефон</label>
                    <input
                      type="tel"
                      required
                      value={form.phone}
                      onChange={(e) => setForm({ ...form, phone: e.target.value })}
                      className="w-full px-3 py-2.5 rounded-md border border-input bg-card text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                      placeholder="+7 (___) ___-__-__"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-muted-foreground mb-1">Услуга</label>
                    <select
                      value={form.service}
                      onChange={(e) => setForm({ ...form, service: e.target.value })}
                      className="w-full px-3 py-2.5 rounded-md border border-input bg-card text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                    >
                      <option>Чистка жироуловителя</option>
                      <option>Чистка канализации</option>
                      <option>Договорное обслуживание</option>
                      <option>Срочный выезд</option>
                      <option>Другое (уточню в комментарии)</option>
                    </select>
                  </div>
                  <button
                    type="submit"
                    disabled={status === 'loading'}
                    className="w-full px-4 py-3 rounded-md bg-primary text-primary-foreground font-semibold hover:bg-primary/90 transition-colors disabled:opacity-60"
                  >
                    {status === 'loading' ? 'Отправляю...' : 'Отправить заявку'}
                  </button>
                  {status === 'ok' && (
                    <div className="flex items-center gap-2 text-sm text-primary font-medium bg-accent/60 rounded-md px-3 py-2">
                      <CheckCircle2 className="w-4 h-4" />
                      Заявка принята. Перезвоню в течение 15 минут.
                    </div>
                  )}
                  {status === 'err' && (
                    <div className="text-sm text-destructive bg-destructive/10 rounded-md px-3 py-2">{errorMsg}</div>
                  )}
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Advantages */}
      <section className="py-14 lg:py-20 bg-background">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10 lg:mb-14">
            <div className="text-xs font-semibold uppercase tracking-widest text-primary mb-2">Почему выбирают</div>
            <h2 className="text-2xl lg:text-4xl font-extrabold tracking-tight">Преимущества работы со мной</h2>
            <p className="mt-3 text-muted-foreground max-w-2xl mx-auto">Работаю как самозанятый — без посредников, лишних документов и наценок. Отвечаю на заявки лично.</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {advantages.map((a) => (
              <div key={a.title} className="bg-card rounded-xl p-6 border border-border hover:border-primary/40 hover:shadow-md transition-all">
                <div className="w-12 h-12 rounded-lg bg-accent flex items-center justify-center mb-4">
                  <a.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-lg font-bold mb-2">{a.title}</h3>
                <p className="text-sm text-muted-foreground">{a.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Services */}
      <section id="services" className="py-14 lg:py-20 bg-secondary/40">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10 lg:mb-14">
            <div className="text-xs font-semibold uppercase tracking-widest text-primary mb-2">Что я делаю</div>
            <h2 className="text-2xl lg:text-4xl font-extrabold tracking-tight">Услуги</h2>
            <p className="mt-3 text-muted-foreground max-w-2xl mx-auto">Полный цикл обслуживания жироуловителей и канализации: от разовой чистки до регулярного договора.</p>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {services.map((s) => (
              <div key={s.title} className="bg-card rounded-2xl p-6 lg:p-7 border border-border flex flex-col">
                <div className="flex items-start justify-between mb-4">
                  <div className="w-12 h-12 rounded-lg bg-primary flex items-center justify-center">
                    <s.icon className="w-6 h-6 text-primary-foreground" />
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-muted-foreground">Цена</div>
                    <div className="text-lg font-bold text-primary">{s.price}</div>
                  </div>
                </div>
                <h3 className="text-xl font-bold mb-2">{s.title}</h3>
                <p className="text-sm text-muted-foreground mb-4">{s.desc}</p>
                <ul className="space-y-2 mb-5">
                  {s.points.map((p) => (
                    <li key={p} className="flex items-start gap-2 text-sm">
                      <CheckCircle2 className="w-4 h-4 text-primary shrink-0 mt-0.5" />
                      <span>{p}</span>
                    </li>
                  ))}
                </ul>
                <a href="#contacts" className="mt-auto inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-md bg-secondary text-secondary-foreground font-semibold hover:bg-accent transition-colors">
                  Заказать
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-14 lg:py-20 bg-background">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10 lg:mb-14">
            <div className="text-xs font-semibold uppercase tracking-widest text-primary mb-2">Тарифы</div>
            <h2 className="text-2xl lg:text-4xl font-extrabold tracking-tight">Цены на чистку жироуловителей</h2>
            <p className="mt-3 text-muted-foreground max-w-2xl mx-auto">Стоимость зависит от объёма оборудования. Точную цену называю после звонка — может быть ниже, если у вас несколько точек или вы на договоре.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            {pricing.map((p) => (
              <div
                key={p.volume}
                className={`relative bg-card rounded-2xl p-6 border-2 ${p.popular ? 'border-primary shadow-lg' : 'border-border'}`}
              >
                {p.popular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-primary text-primary-foreground text-xs font-bold">
                    Чаще всего заказывают
                  </div>
                )}
                <div className="text-sm text-muted-foreground uppercase tracking-wide mb-1">Объём</div>
                <div className="text-2xl font-extrabold text-primary mb-3">{p.volume}</div>
                <div className="text-3xl font-extrabold mb-1">{p.price}</div>
                <div className="text-xs text-muted-foreground mb-4">≈ {p.time} на объекте</div>
                <div className="text-sm font-medium mb-4 min-h-[40px]">{p.target}</div>
                <a href="#contacts" className={`block text-center px-4 py-2.5 rounded-md font-semibold transition-colors ${p.popular ? 'bg-primary text-primary-foreground hover:bg-primary/90' : 'bg-secondary text-secondary-foreground hover:bg-accent'}`}>
                  Заказать
                </a>
              </div>
            ))}
          </div>

          <div className="mt-10 max-w-3xl mx-auto bg-accent/40 rounded-xl p-5 lg:p-6 border border-primary/20">
            <div className="flex items-start gap-3">
              <Star className="w-5 h-5 text-primary shrink-0 mt-0.5" />
              <p className="text-sm">
                <b className="text-primary">Договорное обслуживание — скидка 10%.</b> Фиксируем график,
                вы получаете приоритетный выезд, стикеры на оборудование с датой следующей чистки и
                напоминание в WhatsApp. От 4 500 ₽/мес за одну точку.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Segments */}
      <section id="segments" className="py-14 lg:py-20 bg-secondary/40">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10 lg:mb-14">
            <div className="text-xs font-semibold uppercase tracking-widest text-primary mb-2">Кому подходит</div>
            <h2 className="text-2xl lg:text-4xl font-extrabold tracking-tight">С кем я работаю</h2>
            <p className="mt-3 text-muted-foreground max-w-2xl mx-auto">Понимаю специфику каждого сегмента: от объёма жировых отходов до требований проверяющих органов.</p>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {segments.map((s) => (
              <div key={s.title} className="bg-card rounded-2xl p-6 lg:p-7 border border-border">
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-12 h-12 rounded-lg bg-primary flex items-center justify-center">
                    <s.icon className="w-6 h-6 text-primary-foreground" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold">{s.title}</h3>
                    <div className="text-xs text-muted-foreground">{s.examples}</div>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground mb-4">{s.desc}</p>
                <div className="grid grid-cols-2 gap-3 pt-4 border-t border-border">
                  <div>
                    <div className="text-xs text-muted-foreground uppercase">Объём</div>
                    <div className="text-sm font-bold mt-1">{s.volume}</div>
                  </div>
                  <div>
                    <div className="text-xs text-muted-foreground uppercase">Частота</div>
                    <div className="text-sm font-bold mt-1">{s.frequency}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Process */}
      <section id="process" className="py-14 lg:py-20 bg-background">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10 lg:mb-14">
            <div className="text-xs font-semibold uppercase tracking-widest text-primary mb-2">Как я работаю</div>
            <h2 className="text-2xl lg:text-4xl font-extrabold tracking-tight">Четыре шага от заявки до акта</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {steps.map((s) => (
              <div key={s.num} className="relative bg-card rounded-xl p-6 border border-border">
                <div className="absolute -top-3 -left-3 w-10 h-10 rounded-full bg-primary text-primary-foreground font-bold flex items-center justify-center text-lg">
                  {s.num}
                </div>
                <h3 className="text-lg font-bold mb-2 mt-2">{s.title}</h3>
                <p className="text-sm text-muted-foreground">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Geography */}
      <section className="py-14 lg:py-20 bg-primary text-primary-foreground">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-8 items-center">
            <div>
              <div className="text-xs font-semibold uppercase tracking-widest text-emerald-200 mb-2">География работы</div>
              <h2 className="text-2xl lg:text-4xl font-extrabold tracking-tight mb-4">Самара и пригород</h2>
              <p className="text-white/85 mb-6 max-w-xl">
                Выезжаю во все районы Самары и города-спутники. По Самаре — выезд в течение 3 часов
                с момента заявки. В пригороды — в день обращения или на следующий день по согласованию.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {areas.map((a) => (
                  <div key={a} className="flex items-center gap-2 text-sm">
                    <MapPin className="w-4 h-4 text-emerald-300 shrink-0" />
                    <span>{a}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-white/10 rounded-2xl p-6 border border-white/15">
              <div className="flex items-center gap-3 mb-4">
                <Truck className="w-6 h-6 text-emerald-300" />
                <h3 className="text-lg font-bold">Стоимость выезда</h3>
              </div>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between border-b border-white/15 pb-2">
                  <span className="text-white/80">Самара (все районы)</span>
                  <span className="font-bold">бесплатно</span>
                </div>
                <div className="flex justify-between border-b border-white/15 pb-2">
                  <span className="text-white/80">Новокуйбышевск</span>
                  <span className="font-bold">+300 ₽</span>
                </div>
                <div className="flex justify-between border-b border-white/15 pb-2">
                  <span className="text-white/80">Чапаевск, Кинель</span>
                  <span className="font-bold">+500 ₽</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/80">Другие пригороды</span>
                  <span className="font-bold">по договорённости</span>
                </div>
              </div>
              <p className="text-xs text-white/70 mt-4">
                Для клиентов на договоре — выезд в пригород бесплатный при графике от 1 раза в месяц.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-14 lg:py-20 bg-background">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-3xl">
          <div className="text-center mb-10 lg:mb-14">
            <div className="text-xs font-semibold uppercase tracking-widest text-primary mb-2">FAQ</div>
            <h2 className="text-2xl lg:text-4xl font-extrabold tracking-tight">Частые вопросы</h2>
          </div>
          <div className="space-y-3">
            {faq.map((f, i) => (
              <div key={i} className="bg-card rounded-xl border border-border overflow-hidden">
                <button
                  onClick={() => setOpenFaq(openFaq === i ? null : i)}
                  className="w-full flex items-center justify-between gap-3 px-5 py-4 text-left hover:bg-muted/40 transition-colors"
                >
                  <span className="font-semibold">{f.q}</span>
                  <ChevronDown className={`w-5 h-5 text-muted-foreground shrink-0 transition-transform ${openFaq === i ? 'rotate-180' : ''}`} />
                </button>
                {openFaq === i && (
                  <div className="px-5 pb-5 text-sm text-muted-foreground leading-relaxed">{f.a}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contacts / CTA */}
      <section id="contacts" className="py-14 lg:py-20 bg-secondary/40">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-8">
            <div>
              <div className="text-xs font-semibold uppercase tracking-widest text-primary mb-2">Контакты</div>
              <h2 className="text-2xl lg:text-4xl font-extrabold tracking-tight mb-4">Свяжитесь любым удобным способом</h2>
              <p className="text-muted-foreground mb-6 max-w-md">
                Принимаю заявки с 7:00 до 22:00. Если не удалось дозвониться — пишите в WhatsApp или
                Telegram, отвечу в течение 15 минут.
              </p>

              <div className="space-y-3">
                <a href={`tel:${PHONE_TEL}`} className="flex items-center gap-3 bg-card rounded-xl p-4 border border-border hover:border-primary/40 transition-colors">
                  <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center shrink-0">
                    <Phone className="w-5 h-5 text-primary-foreground" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs text-muted-foreground">Телефон</div>
                    <div className="font-bold">{PHONE_DISPLAY}</div>
                  </div>
                </a>
                <a href={MAX_URL} target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 bg-card rounded-xl p-4 border border-border hover:border-primary/40 transition-colors">
                  <div className="w-10 h-10 rounded-lg bg-[#7C3AED] flex items-center justify-center shrink-0">
                    <MessageCircle className="w-5 h-5 text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs text-muted-foreground">MAX</div>
                    <div className="font-bold truncate">{PHONE_DISPLAY}</div>
                  </div>
                </a>
                <a href={TELEGRAM_URL} target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 bg-card rounded-xl p-4 border border-border hover:border-primary/40 transition-colors">
                  <div className="w-10 h-10 rounded-lg bg-[#229ED9] flex items-center justify-center shrink-0">
                    <Send className="w-5 h-5 text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs text-muted-foreground">Telegram</div>
                    <div className="font-bold truncate">{PHONE_DISPLAY}</div>
                  </div>
                </a>
                <a href={`mailto:${EMAIL}`} className="flex items-center gap-3 bg-card rounded-xl p-4 border border-border hover:border-primary/40 transition-colors">
                  <div className="w-10 h-10 rounded-lg bg-secondary flex items-center justify-center shrink-0">
                    <Mail className="w-5 h-5 text-primary" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs text-muted-foreground">Email</div>
                    <div className="font-bold truncate">{EMAIL}</div>
                  </div>
                </a>
              </div>

              <div className="mt-5 flex items-center gap-3 text-sm bg-card rounded-xl p-4 border border-border">
                <Clock className="w-5 h-5 text-primary" />
                <span><b>Режим работы:</b> ежедневно, 7:00–22:00. Экстренные заявки — по договорённости.</span>
              </div>
            </div>

            <div className="bg-card rounded-2xl p-6 lg:p-8 border border-border">
              <h3 className="text-xl font-bold mb-1">Оставить заявку</h3>
              <p className="text-sm text-muted-foreground mb-5">Заполните форму — перезвоню в течение 15 минут в рабочее время.</p>
              <form onSubmit={submit} className="space-y-4">
                <div className="grid sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-muted-foreground mb-1">Имя *</label>
                    <input
                      type="text"
                      required
                      value={form.name}
                      onChange={(e) => setForm({ ...form, name: e.target.value })}
                      className="w-full px-3 py-2.5 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                      placeholder="Иван"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-muted-foreground mb-1">Телефон *</label>
                    <input
                      type="tel"
                      required
                      value={form.phone}
                      onChange={(e) => setForm({ ...form, phone: e.target.value })}
                      className="w-full px-3 py-2.5 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                      placeholder="+7 (___) ___-__-__"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium text-muted-foreground mb-1">Услуга</label>
                  <select
                    value={form.service}
                    onChange={(e) => setForm({ ...form, service: e.target.value })}
                    className="w-full px-3 py-2.5 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                  >
                    <option>Чистка жироуловителя</option>
                    <option>Чистка канализации</option>
                    <option>Договорное обслуживание</option>
                    <option>Срочный выезд</option>
                    <option>Другое (уточню в комментарии)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-muted-foreground mb-1">Адрес объекта</label>
                  <input
                    type="text"
                    value={form.address}
                    onChange={(e) => setForm({ ...form, address: e.target.value })}
                    className="w-full px-3 py-2.5 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                    placeholder="г. Самара, ул. ..."
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-muted-foreground mb-1">Комментарий</label>
                  <textarea
                    rows={3}
                    value={form.comment}
                    onChange={(e) => setForm({ ...form, comment: e.target.value })}
                    className="w-full px-3 py-2.5 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                    placeholder="Объём жироуловителя, удобное время, особенности объекта..."
                  />
                </div>
                <button
                  type="submit"
                  disabled={status === 'loading'}
                  className="w-full px-4 py-3 rounded-md bg-primary text-primary-foreground font-bold hover:bg-primary/90 transition-colors disabled:opacity-60"
                >
                  {status === 'loading' ? 'Отправляю...' : 'Отправить заявку'}
                </button>
                {status === 'ok' && (
                  <div className="flex items-center gap-2 text-sm text-primary font-medium bg-accent/60 rounded-md px-3 py-2">
                    <CheckCircle2 className="w-4 h-4" />
                    Заявка принята. Перезвоню в течение 15 минут.
                  </div>
                )}
                {status === 'err' && (
                  <div className="text-sm text-destructive bg-destructive/10 rounded-md px-3 py-2">{errorMsg}</div>
                )}
                <p className="text-xs text-muted-foreground">
                  Нажимая «Отправить», вы соглашаетесь на обработку персональных данных для связи по заявке.
                </p>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#0a3f27] text-white/80 mt-auto">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <div className="w-9 h-9 rounded-lg bg-primary flex items-center justify-center">
                  <Leaf className="w-5 h-5 text-primary-foreground" />
                </div>
                <div>
                  <div className="text-base font-extrabold text-white">ЖИРОЧИСТ</div>
                  <div className="text-[10px] uppercase tracking-wider text-white/60">Самара</div>
                </div>
              </div>
              <p className="text-sm text-white/70">
                Самозанятый специалист по чистке жироуловителей и канализации. Самара и пригороды.
              </p>
            </div>

            <div>
              <h4 className="text-sm font-bold text-white mb-3">Услуги</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#services" className="hover:text-white">Чистка жироуловителей</a></li>
                <li><a href="#services" className="hover:text-white">Чистка канализации</a></li>
                <li><a href="#services" className="hover:text-white">Договорное обслуживание</a></li>
                <li><a href="#pricing" className="hover:text-white">Тарифы</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-sm font-bold text-white mb-3">Контакты</h4>
              <ul className="space-y-2 text-sm">
                <li><a href={`tel:${PHONE_TEL}`} className="hover:text-white">{PHONE_DISPLAY}</a></li>
                <li><a href={MAX_URL} className="hover:text-white">MAX</a></li>
                <li><a href={TELEGRAM_URL} className="hover:text-white">Telegram</a></li>
                <li><a href={`mailto:${EMAIL}`} className="hover:text-white">{EMAIL}</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-sm font-bold text-white mb-3">Режим работы</h4>
              <ul className="space-y-2 text-sm text-white/70">
                <li>Пн–Вс: 7:00–22:00</li>
                <li>Экстренный выезд: по договорённости</li>
                <li>Заявки с сайта — круглосуточно</li>
              </ul>
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-white/15 flex flex-col sm:flex-row gap-3 sm:justify-between text-xs text-white/60">
            <div>© {new Date().getFullYear()} ЖИРОЧИСТ Самара. Самозанятый, НПД.</div>
            <div>Самара, Новокуйбышевск, Чапаевск, Кинель, Волжский</div>
          </div>
        </div>
      </footer>
    </div>
  )
}
