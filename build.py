# -*- coding: utf-8 -*-
"""Generates index.html + per-CMS landing pages."""
import datetime
import json
import os

OUT = os.path.dirname(os.path.abspath(__file__))

PHONE = "+7 900 000-00-00"
PHONE_HREF = "tel:+79000000000"
TG = "https://t.me/your_tg"
WA = "https://wa.me/79000000000"
MAX = "https://max.ru/your_max"
VK = "https://vk.com/your_vk"
EMAIL = "help@siterescue24.ru"
DOMAIN = "https://siterescue24.ru"
BUILD_DATE = datetime.date.today().isoformat()
BUILD_DATE_RU = datetime.date.today().strftime("%d.%m.%Y")


def icon(name, cls="icn"):
    with open(os.path.join(OUT, "assets", "icons", f"{name}.svg"), encoding="utf-8") as f:
        svg = f.read().strip()
    return svg.replace("<svg ", f'<svg class="{cls}" aria-hidden="true" ', 1)


def socials(cls="socials"):
    return f"""<div class="{cls}">
      <a class="soc-tg" href="{TG}" aria-label="Telegram" title="Telegram">{icon('telegram')}</a>
      <a class="soc-wa" href="{WA}" aria-label="WhatsApp" title="WhatsApp">{icon('whatsapp')}</a>
      <a class="soc-max" href="{MAX}" aria-label="MAX" title="MAX">{icon('max')}</a>
      <a class="soc-vk" href="{VK}" aria-label="ВКонтакте" title="ВКонтакте">{icon('vk')}</a>
      <a class="soc-ph" href="{PHONE_HREF}" aria-label="Позвонить" title="Позвонить">{icon('phone')}</a>
    </div>"""

def org_schema():
    return {
        "@type": "ProfessionalService",
        "@id": DOMAIN + "/#org",
        "name": "SiteRescue24",
        "alternateName": "Скорая помощь сайтам SiteRescue24",
        "url": DOMAIN + "/",
        "telephone": PHONE.replace(" ", "").replace("-", ""),
        "email": EMAIL,
        "description": "Срочное лечение сайтов от вирусов и восстановление после взлома за 24 часа. Без предоплаты, гарантия 1 год.",
        "areaServed": {"@type": "Country", "name": "Россия"},
        "availableLanguage": ["ru"],
        "priceRange": "6900-30000 RUB",
        "currenciesAccepted": "RUB",
        "openingHours": "Mo-Su 00:00-24:00",
        "sameAs": [TG, WA, MAX, VK],
        "knowsAbout": [
            "лечение сайта от вирусов",
            "восстановление сайта после взлома",
            "WordPress", "WooCommerce", "1С-Битрикс", "OpenCart", "MODX", "Joomla",
            "аудит безопасности PHP-сайтов",
        ],
        "contactPoint": [{
            "@type": "ContactPoint",
            "telephone": PHONE.replace(" ", "").replace("-", ""),
            "email": EMAIL,
            "contactType": "customer support",
            "availableLanguage": ["ru"],
            "hoursAvailable": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "opens": "00:00", "closes": "23:59",
            },
        }],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Ремонт и защита сайтов",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {"@type": "Service", "name": f"Лечение и восстановление сайта на {d['name']}"},
                    "price": d["price_from"].replace(" ", "").replace("\u00a0", ""),
                    "priceCurrency": "RUB",
                    "url": f"{DOMAIN}/{slug}.html",
                }
                for slug, d in CMS.items()
            ],
        },
    }


def website_schema(page, title, desc):
    url = f"{DOMAIN}/" if page == "index.html" else f"{DOMAIN}/{page}"
    return [
        {
            "@type": "WebSite",
            "@id": DOMAIN + "/#website",
            "url": DOMAIN + "/",
            "name": "SiteRescue24",
            "inLanguage": "ru-RU",
            "publisher": {"@id": DOMAIN + "/#org"},
        },
        {
            "@type": "WebPage",
            "@id": url + "#webpage",
            "url": url,
            "name": title,
            "description": desc,
            "inLanguage": "ru-RU",
            "isPartOf": {"@id": DOMAIN + "/#website"},
            "about": {"@id": DOMAIN + "/#org"},
            "dateModified": BUILD_DATE,
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": ["h1", ".facts"],
            },
        },
    ]


def faq_schema():
    qa = [
        ("А если вы не сможете починить?", "Тогда вы не платите ничего. Предоплаты нет: сначала бесплатная диагностика и точная цена, оплата — после того, как вы проверили работающий сайт."),
        ("У меня нет резервной копии. Это конец?", "Нет. Восстанавливаем и без бэкапа: пересобираем сайт из чистых дистрибутивов и переносим ваш контент и базу."),
        ("Взлом повторится?", "Мы закрываем причину взлома, а не только следы. Если в течение года сайт взломают тем же способом — чиним бесплатно."),
        ("Как быстро вы начнёте?", "Отвечаем в течение 10 минут, работаем 24/7. Большинство сайтов возвращаем к жизни за 4–12 часов, максимум — сутки."),
    ]
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa
        ],
    }


def schema_tag(*items):
    data = {"@context": "https://schema.org", "@graph": list(items)}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>\n"


def index_schema(title, desc):
    return schema_tag(org_schema(), *website_schema("index.html", title, desc), faq_schema())


def page_schema(slug, d, title="", desc=""):
    service = {
        "@type": "Service",
        "name": f"Лечение и восстановление сайта на {d['name']}",
        "provider": {"@type": "ProfessionalService", "name": "SiteRescue24", "url": DOMAIN + "/"},
        "areaServed": "RU",
        "offers": {"@type": "Offer", "price": d["price_from"].replace(" ", "").replace("\u00a0", ""), "priceCurrency": "RUB"},
    }
    crumbs = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": d["name"], "item": f"{DOMAIN}/{slug}.html"},
        ],
    }
    return schema_tag(org_schema(), *website_schema(f"{slug}.html", title, desc), service, crumbs, faq_schema())


CMS = {
    "wordpress": {
        "name": "WordPress и WooCommerce",
        "short": "WordPress",
        "logo": "wordpress", "color": "#21759b",
        "kw": "лечение сайта wordpress от вирусов, взломали сайт wordpress, редирект на чужой сайт wordpress, восстановление woocommerce",
        "tag": "самая массовая CMS",
        "price_from": "6 900",
        "hero": "Сайт на WordPress не работает?<br><em>Вернём его за 24 часа</em>",
        "sub": "Редиректы на чужие сайты, спам в поиске, белый экран, блокировка хостинга — каждый час это минус заявки и минус деньги. Найдём причину, вычистим заражение и защитим, чтобы не повторилось.",
        "pains": [
            ("Реклама льётся впустую", "Вы платите за клики, а посетители улетают на чужие сайты"),
            ("Позиции в поиске рушатся", "Яндекс и Google понижают заражённый сайт с каждым днём"),
            ("Магазин WooCommerce стоит", "Заказы не проходят — клиенты покупают у конкурентов"),
            ("Хостинг грозит блокировкой", "Письмо о вредоносном коде — до отключения остались часы"),
        ],
        "extras": [
            "Чистка файлов, базы данных и всех плагинов",
            "Восстановление каталога и заказов WooCommerce",
            "Поиск причины взлома по логам — а не «просто почистили»",
            "Защита: файрвол, двойная авторизация, лимит попыток входа",
        ],
    },
    "bitrix": {
        "name": "1С-Битрикс",
        "short": "Bitrix",
        "logo": "bitrix24", "color": "#d24a43",
        "kw": "лечение сайта битрикс от вирусов, взломали сайт 1с-битрикс, вирус на битрикс, восстановление сайта битрикс",
        "tag": "магазины и корпорации",
        "price_from": "14 900",
        "hero": "Магазин на Битрикс лежит?<br><em>Каждый час — минус выручка</em>",
        "sub": "Заказы не проходят, обмен с 1С сломан, в админке чужие «агенты». Поднимем сайт без остановки продаж, сохраним интеграцию с 1С. Договор, закрывающие документы, полная конфиденциальность.",
        "pains": [
            ("Продажи остановились", "Клиенты не могут оформить заказ и уходят к конкурентам"),
            ("Обмен с 1С сломался", "Остатки и цены не обновляются — менеджеры работают вслепую"),
            ("Заражение возвращается", "Чистили уже не раз, а вирус появляется снова"),
            ("Репутация под ударом", "Антивирусы пугают клиентов красным экраном на вашем сайте"),
        ],
        "extras": [
            "Проверка агентов, событий и служебного кода на закладки",
            "Сохранение обмена с 1С и торгового каталога",
            "Обновление платформы до безопасной версии",
            "Настройка проактивной защиты Битрикс",
        ],
    },
    "opencart": {
        "name": "OpenCart",
        "short": "OpenCart",
        "logo": "opencart", "color": "#2ac2ef",
        "kw": "лечение сайта opencart от вирусов, взломали магазин opencart, вирус opencart, спам заказы opencart",
        "tag": "интернет-магазины",
        "price_from": "9 900",
        "hero": "Магазин на OpenCart заражён?<br><em>Вернём продажи за 1 день</em>",
        "sub": "Крадут данные карт покупателей, тысячи спам-заказов, магазин еле грузится. Уберём заражение из файлов, базы и кэша модификаторов — и закроем лазейку, через которую зашли.",
        "pains": [
            ("Воруют карты ваших клиентов", "Это претензии, возвраты и риск блокировки эквайринга"),
            ("Спам-заказы завалили почту", "Реальные покупатели тонут в мусоре — вы их теряете"),
            ("Вирус возвращается после чистки", "Причина в кэше модификаторов и базе, куда никто не смотрит"),
            ("Магазин тормозит", "Покупатели не ждут — 3 секунды загрузки и они ушли"),
        ],
        "extras": [
            "Чистка кэша модификаторов и базы — не только файлов",
            "Проверка страницы оплаты на кражу данных карт",
            "Защита от спам-ботов и фейковых регистраций",
            "Перенос админки и усиление доступов",
        ],
    },
    "modx": {
        "name": "MODX",
        "short": "MODX",
        "logo": "modx", "color": "#8bc34a",
        "kw": "лечение сайта modx от вирусов, взломали сайт modx, вирус modx revolution, восстановление сайта modx",
        "tag": "Revolution и Evolution",
        "price_from": "9 900",
        "hero": "Сайт на MODX взломан или упал?<br><em>Мы знаем MODX изнутри</em>",
        "sub": "Специалистов по MODX мало, и вредоносный код здесь прячется там, где обычные «чистильщики» не ищут — прямо в базе данных. Вычистим полностью, вернём сайт в поиск, дадим гарантию на год.",
        "pains": [
            ("Некому доверить сайт", "Подрядчики разводят руками: «мы с MODX не работаем»"),
            ("Чистили — не помогло", "Код сидит в сниппетах и чанках в базе, файловый антивирус его не видит"),
            ("Сайт вылетел из поиска", "Пометка «сайт может угрожать безопасности» отпугивает всех"),
            ("Страницы подменяются", "Вместо вашего контента — чужая реклама и дорвеи"),
        ],
        "extras": [
            "Проверка сниппетов, чанков и плагинов в базе данных",
            "Переустановка ядра из чистого дистрибутива",
            "Обновление уязвимых компонентов",
            "Снятие меток в Яндекс Вебмастере и Google Search Console",
        ],
    },
    "joomla": {
        "name": "Joomla",
        "short": "Joomla",
        "logo": "joomla", "color": "#f9a541",
        "kw": "лечение сайта joomla от вирусов, взломали сайт joomla, дефейс joomla, восстановление сайта joomla после взлома",
        "tag": "включая шаблоны Helix",
        "price_from": "7 900",
        "hero": "Сайт на Joomla подменили или взломали?<br><em>Восстановим за 4–12 часов</em>",
        "sub": "Сейчас идёт волна взломов сайтов на Joomla со старыми шаблонами и редакторами. Если вместо сайта чужая страница или хостинг прислал предупреждение — действовать нужно сегодня, пока сайт не вылетел из поиска.",
        "pains": [
            ("Вместо сайта — чужая страница", "Клиенты видят это прямо сейчас и уходят навсегда"),
            ("Сайт вылетает из Яндекса", "Каждый день промедления — минус позиции, которые копились годами"),
            ("Хостинг предупредил о вирусах", "Следующий шаг хостинга — полная блокировка аккаунта"),
            ("В корне сайта чужие файлы", "Через них злоумышленник заходит на сайт как к себе домой"),
        ],
        "extras": [
            "Удаление всех посторонних файлов и закладок",
            "Закрытие уязвимости шаблона и редактора (включая Helix)",
            "Пересборка из чистых дистрибутивов с переносом контента",
            "Возврат в поиск: снятие меток в Вебмастере и Search Console",
        ],
    },
    "php": {
        "name": "Самописные PHP-проекты",
        "short": "PHP-проект",
        "logo": "php", "color": "#777bb3",
        "kw": "лечение самописного сайта php от вирусов, взломали сайт php, аудит безопасности php сайта, восстановление php сайта",
        "tag": "legacy и фреймворки",
        "price_from": "12 900",
        "hero": "Самописный сайт сломался,<br>а разработчика нет? <em>Спасём</em>",
        "sub": "Старый код без документации, автор пропал, а сайт взломали или он упал после переезда. Разберёмся в чужом коде руками, вычистим заражение, поднимем проект и оставим вам понятную документацию.",
        "pains": [
            ("Разработчик пропал", "Никто не знает, как проект устроен — а бизнес на нём держится"),
            ("Слили базу клиентов", "Дыры в старом коде открыты для любого школьника со сканером"),
            ("Упал после обновления сервера", "Старый код несовместим с новым PHP — сайт лежит"),
            ("Страшно трогать код", "Любое изменение может уронить всё окончательно"),
        ],
        "extras": [
            "Ручной разбор кода и логов — найдём, как именно вас взломали",
            "Совместимость с современными версиями PHP",
            "Закрытие дыр: инъекции, загрузки файлов, формы",
            "Документация по проекту, чтобы вы больше не зависели от одного человека",
        ],
    },
}

def base_head(title, desc, page, kw="", schema=""):
    canonical = f"{DOMAIN}/" if page == "index.html" else f"{DOMAIN}/{page}"
    kw_meta = f'<meta name="keywords" content="{kw}">\n' if kw else ""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; img-src 'self' data:; font-src 'self' https://fonts.gstatic.com; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title}</title>
<meta name="description" content="{desc}">
{kw_meta}<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/favicon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SiteRescue24">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
{schema}</head>
<body>
<header>
  <div class="container nav">
    <a class="logo" href="index.html"><img src="assets/logo.png" alt="IntelPrime — защита от взлома сайтов"></a>
    <nav class="nav-links">
      <a href="index.html#cms">Платформы</a>
      <a href="{page}#process">Как работаем</a>
      <a href="{page}#pricing">Цены</a>
      <a href="{page}#faq">Вопросы</a>
    </nav>
    {socials('socials nav-socials')}
    <a class="nav-phone" href="{PHONE_HREF}">{PHONE}</a>
    <a class="nav-phone-icon soc-ph" href="{PHONE_HREF}" aria-label="Позвонить">{icon('phone')}</a>
    <a class="btn btn-cta nav-cta" href="{page}#contact">Спасти сайт</a>
    <button class="burger" id="burger" aria-label="Открыть меню" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="mm-overlay" id="mm-overlay"></div>
<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
    <div class="mm-head">
      <a class="logo" href="index.html"><img src="assets/logo.png" alt="IntelPrime — защита от взлома сайтов"></a>
      <button class="mm-close" id="mm-close" aria-label="Закрыть меню">✕</button>
    </div>
    <nav>
      <a href="index.html#cms">Платформы</a>
      <a href="{page}#process">Как работаем</a>
      <a href="{page}#pricing">Цены</a>
      <a href="{page}#faq">Вопросы</a>
      <a href="{page}#contact" class="mm-cta">Спасти сайт — 0 ₽</a>
    </nav>
    <a class="mm-phone" href="{PHONE_HREF}">{icon('phone')}{PHONE}</a>
    {socials('socials mm-socials')}
</div>
"""

FACT_ICONS = {
    "bolt": '<svg class="fact-ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "clock": '<svg class="fact-ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "search": '<svg class="fact-ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    "wallet": '<svg class="fact-ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>',
    "shield": '<svg class="fact-ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>',
    "globe": '<svg class="fact-ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
}


def facts_section(price_from, scope):
    """Короткий блок фактов: его цитируют ИИ-ответы Яндекса, Google и чат-боты."""
    cards = [
        ("bolt", "Услуга", f"Срочное лечение от вирусов и восстановление после взлома для {scope}"),
        ("clock", "Срок", "<b>4–12 часов</b> в большинстве случаев, максимум 24 часа"),
        ("search", "Диагностика", "<b>Бесплатно</b>: результат и точная цена — за 30 минут"),
        ("wallet", "Предоплата", "<b>0 ₽</b> — оплата после проверки работающего сайта"),
        ("shield", "Гарантия", "<b>1 год письменно</b> в договоре: повторный взлом того же типа чиним бесплатно"),
        ("globe", "Режим и география", "Заявки <b>24/7</b> · вся Россия и СНГ, работаем удалённо"),
    ]
    items = "".join(
        f'<div class="fact reveal">{FACT_ICONS[ic]}<dt>{t}</dt><dd>{v}</dd></div>'
        for ic, t, v in cards
    )
    return f"""
<section class="light facts-sec" id="short">
  <div class="container">
    <div class="wm" data-wm="Факты"><h2>Кратко: что, за сколько <br>и <span class="red">как быстро</span></h2>
    <p class="lead">Вся суть предложения на одном экране — без мелкого шрифта и звёздочек.</p></div>
    <div class="facts-wrap">
      <dl class="facts">{items}</dl>
      <aside class="facts-cta reveal">
        <span class="facts-cta-tag">Разово, фиксированная цена</span>
        <div class="facts-price">от <b>{price_from} ₽</b></div>
        <p class="facts-price-note">или подписка «Охрана» — 1 990 ₽/мес: мониторинг, бэкапы и защита</p>
        <a class="btn btn-cta facts-btn" href="#contact">Узнать точную цену — 0 ₽</a>
        <div class="facts-contacts">
          <a href="{PHONE_HREF}">{icon('phone')}{PHONE}</a>
          <a href="{TG}">{icon('telegram')}Telegram</a>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </div>
        <p class="fine">Ответим за 10 минут · Обновлено: <time datetime="{BUILD_DATE}">{BUILD_DATE_RU}</time></p>
      </aside>
    </div>
  </div>
</section>
"""


STRIP = """
<section style="padding:44px 0" class="light">
  <div class="container">
    <div class="strip reveal">
      <div><b>30 мин</b><span>и вы знаете, что случилось и сколько стоит ремонт</span></div>
      <div><b>24 часа</b><span>максимум — и сайт снова приносит деньги</span></div>
      <div><b>0 ₽</b><span>предоплаты: платите, когда сайт уже работает</span></div>
      <div><b>1 год</b><span>гарантии: повторный взлом чиним бесплатно</span></div>
    </div>
  </div>
</section>
"""

def pain_section(pains, money_line):
    items = "".join(
        f'<div class="pain reveal"><b>{t}</b><p>{p}</p></div>' for t, p in pains
    )
    return f"""
<section class="light">
  <div class="container">
    <div class="wm" data-wm="Потери"><h2>Пока сайт не работает —<br><span class="red">вы теряете деньги</span></h2>
    <p class="lead">Взлом — это не «технические проблемы». Это прямые потери бизнеса, которые растут с каждым часом:</p></div>
    <div class="pain-list">{items}</div>
    <div class="money reveal">{money_line}</div>
  </div>
</section>
"""

PROC_ICONS = {
    "chat": '<svg class="proc-ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>',
    "lock": '<svg class="proc-ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "tool": '<svg class="proc-ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
    "check": '<svg class="proc-ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
}


def process_section():
    steps = [
        ("chat", "10 минут", "Ответим за 10 минут", "Возьмём сайт в работу и за 30 минут скажем: что случилось, сколько стоит и когда заработает.", "Бесплатно"),
        ("lock", "До старта работ", "Фиксируем цену", "Называем точную сумму до начала работ. Никаких «в процессе выяснилось, доплатите».", "Цена не меняется"),
        ("tool", "4–12 часов", "Чиним и чистим", "Убираем заражение из файлов и базы, находим и закрываем причину взлома.", "Работаем на копии"),
        ("check", "Финал", "Проверяете — потом платите", "Сдаём работающий сайт, возвращаем его в поиск, ставим защиту. Оплата — после проверки.", "Гарантия 1 год письменно"),
    ]
    cards = "".join(
        f"""
      <article class="proc-step reveal">
        <div class="proc-head"><span class="proc-num">{i}</span><span class="proc-ic-wrap">{PROC_ICONS[ic]}</span></div>
        <span class="proc-time">{time}</span>
        <h3>{title}</h3>
        <p>{text}</p>
        <span class="proc-badge">{badge}</span>
      </article>"""
        for i, (ic, time, title, text, badge) in enumerate(steps, 1)
    )
    return f"""
<section id="process">
  <div class="container">
    <div class="center reveal"><span class="sec-tag">Как мы работаем</span>
    <h2>Что будет после <span class="red">вашей заявки</span></h2>
    <p class="lead">Никакой магии и туманных обещаний — четыре понятных шага от заявки до работающего сайта:</p></div>
    <div class="proc">
      <div class="proc-track" aria-hidden="true"></div>{cards}
    </div>
    <div class="proc-cta reveal">
      <div class="proc-cta-txt">
        <b>Сайт лежит прямо сейчас?</b>
        <span>Опишите проблему — через 30 минут вы будете знать диагноз и точную цену. Это бесплатно и ни к чему не обязывает.</span>
      </div>
      <div class="proc-cta-btns">
        <a class="btn btn-cta" href="#contact">Спасти сайт — 0 ₽</a>
        <a class="btn btn-outline proc-btn-tg" href="{TG}">{icon('telegram')}Написать в Telegram</a>
      </div>
    </div>
  </div>
</section>
"""

def pricing_section(p_from, cms_name):
    full = f"{int(p_from.replace(' ', '').replace(chr(160), '')) * 2:,}".replace(",", "\u00a0")
    return f"""
<section id="pricing" class="light">
  <div class="container">
    <div class="center reveal"><h2>Сколько стоит вернуть сайт</h2>
    <p class="lead">Точную цену фиксируем после бесплатной диагностики — и она не меняется.</p></div>
    <div class="grid grid-3" style="margin-top:48px">
      <div class="card price-card reveal">
        <span class="plan">Реанимация</span>
        <div class="cost">от {p_from} ₽</div>
        <ul>
          <li>Сайт снова работает</li>
          <li>Заражение удалено полностью</li>
          <li>Причина взлома закрыта</li>
          <li>Гарантия 6 месяцев</li>
        </ul>
        <a class="btn btn-outline" href="#contact">Выбрать</a>
      </div>
      <div class="card price-card featured reveal">
        <div class="ribbon">Выбирают 8 из 10</div>
        <span class="plan">Реанимация + защита</span>
        <div class="cost">от {full} ₽</div>
        <ul>
          <li>Всё из «Реанимации»</li>
          <li>Чистка базы данных и кэша</li>
          <li>Обновление {cms_name} до безопасной версии</li>
          <li>Возврат сайта в Яндекс и Google</li>
          <li>Защита от повторного взлома</li>
          <li>Гарантия 1 год</li>
        </ul>
        <a class="btn btn-red" href="#contact">Выбрать</a>
      </div>
      <div class="card price-card reveal">
        <span class="plan">Подписка «Охрана»</span>
        <div class="cost">1 990 ₽ <span>/мес</span></div>
        <ul>
          <li>Ежедневная проверка на вирусы</li>
          <li>Мониторинг работы сайта 24/7</li>
          <li>Резервные копии у нас</li>
          <li>Обновления безопасности</li>
          <li>Взлом — чиним бесплатно</li>
        </ul>
        <a class="btn btn-outline" href="#contact">Подключить</a>
      </div>
    </div>
    <p class="center" style="margin-top:22px;color:#777;font-size:.9rem">Оплата по счёту с договором или картой. Для юрлиц — закрывающие документы. Ваши данные и доступы никому не передаём — это прописано в договоре.</p>
  </div>
</section>
"""

FAQ = """
<section id="faq" class="light" style="padding-top:0">
  <div class="container" style="max-width:840px">
    <div class="center reveal"><h2>Частые вопросы</h2></div>
    <div style="margin-top:36px">
      <details class="faq-item reveal"><summary>А если вы не сможете починить?</summary><div class="answer">Тогда вы не платите ничего. Предоплаты нет: сначала бесплатная диагностика и точная цена, оплата — после того, как вы проверили работающий сайт.</div></details>
      <details class="faq-item reveal"><summary>У меня нет резервной копии. Это конец?</summary><div class="answer">Нет. Восстанавливаем и без бэкапа: пересобираем сайт из чистых дистрибутивов и переносим ваш контент и базу. Часть контента при необходимости достаём из кэша поисковиков.</div></details>
      <details class="faq-item reveal"><summary>Взлом повторится?</summary><div class="answer">Мы закрываем причину взлома, а не только следы. Если в течение года сайт взломают тем же способом — чиним бесплатно. Это прописано в договоре.</div></details>
      <details class="faq-item reveal"><summary>Как быстро вы начнёте?</summary><div class="answer">Отвечаем в течение 10 минут, работаем 24/7. Большинство сайтов возвращаем к жизни за 4–12 часов, максимум — сутки.</div></details>
      <details class="faq-item reveal"><summary>Придётся давать доступы к хостингу?</summary><div class="answer">Да, без доступа к файлам и базе вылечить сайт нельзя. Работаем по договору: ваши данные и доступы никому не передаются. После работ рекомендуем сменить пароли — поможем всё настроить.</div></details>
      <details class="faq-item reveal"><summary>Хостинг уже заблокировал сайт. Что делать?</summary><div class="answer">Оставьте заявку — свяжемся с поддержкой хостинга от вашего имени, получим логи и снимем блокировку после чистки. Это входит в стоимость.</div></details>
    </div>
  </div>
</section>
"""

def contact_section():
    return f"""
<section id="contact" class="cta-final">
  <div class="container center">
    <div class="reveal">
      <h2>Сайт не работает <span class="red">прямо сейчас?</span></h2>
      <p class="lead" style="margin:0 auto;color:#c9c9c9">Оставьте заявку — через 30 минут вы будете точно знать, что случилось, сколько стоит ремонт и когда сайт снова начнёт приносить деньги. Бесплатно и без обязательств.</p>
    </div>
    <form class="form-card reveal" id="lead-form" novalidate>
      <input type="text" name="name" placeholder="Ваше имя" maxlength="60" required autocomplete="name">
      <input type="url" name="site" placeholder="Ссылка на ваш сайт" maxlength="200" autocomplete="url" required>
      <input type="tel" name="phone" class="js-phone" placeholder="+7 (___) ___-__-__" inputmode="tel" autocomplete="tel" required>
      <input type="text" name="company" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">
      <p class="form-error" aria-live="polite"></p>
      <button class="btn btn-cta btn-lg" type="submit">Узнать, что с сайтом — бесплатно</button>
      <p class="fine">Нажимая кнопку, вы соглашаетесь с политикой обработки персональных данных.</p>
    </form>
    {socials('socials form-socials')}
    <div class="messengers">
      <a class="btn btn-outline" href="{TG}">Написать в Telegram</a>
      <a class="btn btn-outline" href="{PHONE_HREF}">{PHONE}</a>
    </div>
    <p style="margin-top:18px;color:#8a8a8a;font-size:.9rem">Работаем 24/7 · Отвечаем за 10 минут</p>
  </div>
</section>
"""

FOOTER = """
<footer>
  <div class="container">
    <div class="footer-cta">
      <div>
        <h3>Нужна помощь прямо сейчас?</h3>
        <p>Напишите в мессенджер — отвечаем за 10 минут, 24/7</p>
      </div>
      <div class="footer-cta-btns">
        <a class="btn btn-cta" href="%TG%">Telegram</a>
        <a class="btn btn-outline" href="%PHONE_HREF%">%PHONE%</a>
      </div>
    </div>
    <div class="footer-grid footer-grid-3">
      <div class="footer-col footer-brand">
        <a class="logo" href="index.html"><img src="assets/logo.png" alt="IntelPrime — защита от взлома сайтов"></a>
        <p>Скорая помощь сайтам: срочный ремонт, лечение от вирусов и защита от взлома. Работаем по всей России и СНГ — удалённо, по договору.</p>
        <div class="footer-work">Работаем 10:00–22:00 МСК<br><span>Экстренные случаи — 24/7</span></div>
      </div>
      <div class="footer-col">
        <b>Платформы</b>
        <a href="wordpress.html">WordPress и WooCommerce</a>
        <a href="bitrix.html">1С-Битрикс</a>
        <a href="opencart.html">OpenCart</a>
        <a href="modx.html">MODX</a>
        <a href="joomla.html">Joomla</a>
        <a href="php.html">Самописный PHP</a>
      </div>
      <div class="footer-col">
        <b>Контакты</b>
        <a href="%PHONE_HREF%" class="footer-phone">%PHONE%</a>
        <a href="mailto:help@siterescue24.ru">help@siterescue24.ru</a>
        %SOCIALS%
        <div class="footer-badges"><span>Договор</span><span>Конфиденциально</span><span>Гарантия 1 год</span></div>
      </div>
    </div>
    <div class="footer-bottom">
      <div>© 2026 SiteRescue24. Все права защищены.</div>
      <div><a href="#">Политика конфиденциальности</a> · <a href="#">Договор-оферта</a> · <a href="#">Реквизиты</a></div>
    </div>
  </div>
  <a class="scrollup" href="#" aria-label="Наверх">↑</a>
</footer>""".replace("%TG%", TG).replace("%PHONE_HREF%", PHONE_HREF).replace("%PHONE%", PHONE).replace("%SOCIALS%", socials("socials footer-socials")) + """
<div class="sticky-cta"><a class="btn btn-cta btn-lg" href="#contact">Спасти сайт — диагностика 0 ₽</a></div>
<div class="modal-overlay" id="lead-modal" aria-hidden="true">
  <div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <button class="modal-close" id="modal-close" aria-label="Закрыть">✕</button>
    <div class="modal-badge"><span class="pulse"></span>Ответим за 10 минут</div>
    <h3 id="modal-title">Спасём ваш сайт<span class="modal-cms" id="modal-cms"></span></h3>
    <p class="modal-sub">Оставьте контакты — через 30 минут вы будете знать, что случилось и сколько стоит ремонт. Бесплатно.</p>
    <form id="modal-form" novalidate>
      <input type="text" name="name" placeholder="Ваше имя" maxlength="60" required autocomplete="name">
      <input type="url" name="site" placeholder="Ссылка на ваш сайт" maxlength="200" autocomplete="url" required>
      <input type="tel" name="phone" class="js-phone" placeholder="+7 (___) ___-__-__" inputmode="tel" autocomplete="tel" required>
      <input type="text" name="company" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">
      <p class="form-error" aria-live="polite"></p>
      <button class="btn btn-cta btn-lg" type="submit">Получить бесплатную диагностику</button>
      <p class="fine">Нажимая кнопку, вы соглашаетесь с политикой обработки персональных данных.</p>
    </form>
    <div class="modal-ok" id="modal-ok">
      <div class="ok-ic">✓</div>
      <b>Заявка принята!</b>
      <p>Свяжемся с вами в течение 10 минут.</p>
    </div>
  </div>
</div>
<script src="assets/main.js"></script>
</body>
</html>
"""

def cms_page(slug, d):
    title = f"Срочный ремонт и лечение сайта на {d['name']} за 24 часа — без предоплаты | SiteRescue24"
    desc = f"Сайт на {d['name']} взломан или не работает? Удалим вирусы и вернём сайт за 24 часа. Цена от {d['price_from']} ₽, без предоплаты, гарантия 1 год. Бесплатная диагностика за 30 минут, работаем 24/7 по всей России."
    head = base_head(
        title=title,
        desc=desc,
        page=f"{slug}.html",
        kw=d["kw"],
        schema=page_schema(slug, d, title, desc),
    )
    extras = "".join(f'<li><span class="ic">✓</span>{x}</li>' for x in d["extras"])
    money = f"Средний магазин теряет <b>от 10 000 ₽ в день</b> простоя. Ремонт — от {d['price_from']} ₽ один раз. Считайте сами."
    return head + f"""
<section class="hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Все платформы</a> → {d['name']}</div>
    <div class="hero-grid">
      <div>
        <div class="badge"><span class="pulse"></span>Принимаем заявки 24/7</div>
        <h1>{d['hero']}</h1>
        <p class="lead">{d['sub']}</p>
        <div class="hero-ctas">
          <a class="btn btn-cta btn-lg" href="#contact">Узнать, что с сайтом — 0 ₽</a>
          <a class="btn btn-outline btn-lg" href="#pricing">Цены — от {d['price_from']} ₽</a>
        </div>
        <div class="hero-points">
          <span><b>—</b> Без предоплаты</span>
          <span><b>—</b> Гарантия 1 год</span>
          <span><b>—</b> Работаем по договору</span>
        </div>
      </div>
      <div class="promise reveal visible">
        <h3>Что мы сделаем с вашим {d['short']}</h3>
        <ul>{extras}</ul>
        <p class="fine">Не починим — не платите. Это условие договора, а не обещание на словах.</p>
      </div>
    </div>
  </div>
</section>
{facts_section(d['price_from'], d['name'])}
{STRIP}
{pain_section(d['pains'], money)}
{process_section()}
{pricing_section(d['price_from'], d['short'])}
{FAQ}
{contact_section()}
{FOOTER}"""

def index_page():
    title = "Сайт взломали или он не работает? Лечение и восстановление за 24 часа | SiteRescue24"
    desc = "Срочное лечение сайтов от вирусов и восстановление после взлома: WordPress, WooCommerce, 1С-Битрикс, OpenCart, MODX, Joomla, самописный PHP. Без предоплаты, гарантия 1 год, диагностика бесплатно за 30 минут. Работаем 24/7 по всей России."
    head = base_head(
        title=title,
        desc=desc,
        page="index.html",
        kw="лечение сайта от вирусов, взломали сайт что делать, восстановление сайта после взлома, удаление вирусов с сайта, сайт не работает",
        schema=index_schema(title, desc),
    )
    cards = ""
    for slug, d in CMS.items():
        cards += f"""
      <div class="card cms-card reveal">
        <span class="tag">{d['tag']}</span>
        <div class="cms-logo" style="background:{d['color']}">{icon(d['logo'], 'cms-icn')}</div>
        <h3><a href="{slug}.html">{d['name']}</a></h3>
        <p>{d['pains'][0][0]} — и другие проблемы. Починим и защитим.</p>
        <span class="price">от {d['price_from']} ₽</span>
        <button class="go js-open-modal" type="button" data-cms="{d['name']}">Оставить заявку →</button>
      </div>"""
    pains = [
        ("Клиенты уходят к конкурентам", "Человек зашёл, увидел ошибку или чужую страницу — и купил у других. Он не вернётся."),
        ("Реклама сливается впустую", "Директ и таргет продолжают списывать деньги за трафик, который никуда не приводит."),
        ("Сайт вылетает из поиска", "Яндекс и Google выкидывают заражённые сайты. Позиции, которые копились годами, сгорают за неделю."),
        ("Хостинг блокирует аккаунт", "Получили письмо о вредоносном коде? Следующий шаг хостинга — полное отключение."),
    ]
    money = "Средний бизнес-сайт теряет <b>от 10 000 ₽ за день</b> простоя. Ремонт стоит от 6 900 ₽ один раз. Чем раньше начнём — тем дешевле обойдётся."
    return head + f"""
<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <div class="badge"><span class="pulse"></span>Скорая помощь сайтам · 24/7</div>
        <h1>Сайт не работает — бизнес теряет деньги. <em>Вернём за&nbsp;24&nbsp;часа</em></h1>
        <p class="lead">Взлом, вирусы, подмена страниц, блокировка хостинга, вылет из поиска. Пришлите ссылку — через 30 минут скажем, что случилось и сколько стоит ремонт. Бесплатно.</p>
        <div class="hero-ctas">
          <a class="btn btn-cta btn-lg" href="#contact">Узнать, что с сайтом — 0 ₽</a>
          <a class="btn btn-outline btn-lg" href="#cms">Моя платформа</a>
        </div>
        <div class="hero-points">
          <span><b>—</b> Без предоплаты</span>
          <span><b>—</b> Гарантия 1 год</span>
          <span><b>—</b> Работаем по договору</span>
        </div>
      </div>
      <div class="promise promise-v2 reveal visible">
        <div class="promise-badge"><span class="pulse"></span>Онлайн · отвечаем за 10 минут</div>
        <h3>Платите только<br>за <span class="red">работающий</span> сайт</h3>
        <ul>
          <li><span class="ic">✓</span><div><b>Не починим — не платите</b><span>Оплата после проверки работающего сайта</span></div></li>
          <li><span class="ic">✓</span><div><b>Цена фиксируется до старта</b><span>Никаких доплат «по ходу дела»</span></div></li>
          <li><span class="ic">✓</span><div><b>Работаем 24/7 без выходных</b><span>Начинаем в течение 30 минут</span></div></li>
          <li><span class="ic">✓</span><div><b>Гарантия 1 год</b><span>Повторный взлом чиним бесплатно</span></div></li>
        </ul>
        <a class="btn btn-cta promise-btn" href="#contact">Получить диагностику — 0 ₽</a>
        <p class="fine">Восстановим даже без резервной копии</p>
      </div>
    </div>
  </div>
</section>
{facts_section('6 900', 'любой CMS и самописных PHP-сайтов')}
{STRIP}
{pain_section(pains, money)}
<section id="cms">
  <div class="container">
    <div class="wm" data-wm="CMS"><h2>Выберите вашу платформу</h2>
    <p class="lead" style="color:#a3a3a3">Под каждую систему — своя методика: мы знаем, где именно прячутся проблемы в вашей CMS.</p></div>
    <div class="grid grid-3" style="margin-top:44px">{cards}
    </div>
  </div>
</section>
<section class="light" style="padding-top:0">
  <div class="container">
    <div class="center reveal" style="padding-top:90px"><h2>Почему мы, а не «мастер с Авито»</h2></div>
    <div class="vs-grid reveal" style="margin-top:44px">
      <div class="vs-card vs-featured">
        <div class="vs-tag">Ваш выбор</div>
        <h3>SiteRescue24</h3>
        <ul>
          <li><span class="vi ok">✓</span><div><b>Находим причину взлома</b><span>всегда — а не только следы</span></div></li>
          <li><span class="vi ok">✓</span><div><b>Чистим файлы и базу данных</b><span>вирусы не возвращаются</span></div></li>
          <li><span class="vi ok">✓</span><div><b>Письменная гарантия 1 год</b><span>прописана в договоре</span></div></li>
          <li><span class="vi ok">✓</span><div><b>Предоплата 0 ₽</b><span>платите за работающий сайт</span></div></li>
          <li><span class="vi ok">✓</span><div><b>Повторный взлом исключаем</b><span>закрываем дыру, а не маскируем</span></div></li>
        </ul>
        <button class="btn btn-cta vs-btn js-open-modal" type="button">Получить бесплатную диагностику</button>
      </div>
      <div class="vs-card">
        <h3>Фрилансер</h3>
        <ul>
          <li><span class="vi no">✕</span><div><b>Причину ищет редко</b><span>чаще просто удаляет файлы</span></div></li>
          <li><span class="vi no">✕</span><div><b>Базу чистит через раз</b><span>заражение остаётся внутри</span></div></li>
          <li><span class="vi no">✕</span><div><b>Гарантии нет</b><span>«на словах» — не гарантия</span></div></li>
          <li><span class="vi no">✕</span><div><b>Предоплата 30–100%</b><span>и может пропасть с деньгами</span></div></li>
          <li><span class="vi no">✕</span><div><b>Повторный взлом — как повезёт</b><span>риски на вас</span></div></li>
        </ul>
      </div>
      <div class="vs-card">
        <h3>«Откатить бэкап»</h3>
        <ul>
          <li><span class="vi no">✕</span><div><b>Причину не находит никогда</b><span>дыра остаётся открытой</span></div></li>
          <li><span class="vi no">✕</span><div><b>База не чистится</b><span>вирус может сидеть в бэкапе</span></div></li>
          <li><span class="vi no">✕</span><div><b>Гарантий нет</b><span>это вообще не ремонт</span></div></li>
          <li><span class="vi no">✕</span><div><b>Бэкап может отсутствовать</b><span>или уже быть заражённым</span></div></li>
          <li><span class="vi no">✕</span><div><b>Взломают снова</b><span>тем же способом, через дни</span></div></li>
        </ul>
      </div>
    </div>
  </div>
</section>
{process_section()}
{pricing_section('6 900', 'CMS')}
{FAQ}
{contact_section()}
{FOOTER}"""

pages = {"index.html": index_page()}
for slug, d in CMS.items():
    pages[f"{slug}.html"] = cms_page(slug, d)

for fname, html in pages.items():
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("written", fname)

sitemap_urls = "".join(
    f"  <url><loc>{DOMAIN}/{'' if p == 'index.html' else p}</loc><lastmod>{BUILD_DATE}</lastmod><changefreq>weekly</changefreq><priority>{'1.0' if p == 'index.html' else '0.8'}</priority></url>\n"
    for p in pages
)
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + sitemap_urls + "</urlset>\n")
print("written sitemap.xml")

# Краулеры ИИ-поисковиков и чат-ботов: разрешены явно, иначе часть из них не индексирует сайт
AI_BOTS = [
    "OAI-SearchBot", "ChatGPT-User", "GPTBot",           # OpenAI / ChatGPT Search
    "PerplexityBot", "Perplexity-User",                   # Perplexity
    "ClaudeBot", "Claude-User", "Claude-SearchBot",        # Anthropic / Claude
    "Google-Extended", "GoogleOther",                     # Gemini / AI Overviews
    "YandexBot", "YandexAdditional", "YandexAdditionalBot",  # Яндекс, в т.ч. Нейро
    "Bingbot", "BingPreview",                             # Bing / Copilot
    "Applebot", "Applebot-Extended",                      # Apple Intelligence
    "DuckAssistBot", "MistralAI-User", "meta-externalagent", "CCBot",
]
robots = "User-agent: *\nAllow: /\n\n"
robots += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in AI_BOTS)
robots += f"Sitemap: {DOMAIN}/sitemap.xml\n"
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(robots)
print("written robots.txt")

# llms.txt — краткая машинночитаемая выжимка для языковых моделей
llms = f"""# SiteRescue24

> Срочное лечение сайтов от вирусов и восстановление после взлома за 24 часа.
> Работаем по всей России и СНГ удалённо, заявки принимаем круглосуточно.

Ключевые факты:
- Диагностика бесплатная, точная цена и причина проблемы — в течение 30 минут.
- Срок ремонта: 4–12 часов в большинстве случаев, максимум 24 часа.
- Цены: от 6 900 ₽ (WordPress), от 7 900 ₽ (Joomla), от 9 900 ₽ (OpenCart, MODX),
  от 12 900 ₽ (самописный PHP), от 14 900 ₽ (1С-Битрикс). Подписка «Охрана» — 1 990 ₽/мес.
- Предоплаты нет: оплата после того, как клиент проверил работающий сайт.
- Гарантия 1 год письменно: повторный взлом тем же способом устраняем бесплатно.
- Восстанавливаем сайты без резервной копии, чистим и файлы, и базу данных.
- Возвращаем сайт в поиск: снимаем метки в Яндекс Вебмастере и Google Search Console.
- Работаем по договору, для юрлиц — закрывающие документы.
- Контакты: {PHONE}, Telegram {TG}, WhatsApp {WA}, e-mail {EMAIL}.

Страницы:
- [Главная]({DOMAIN}/): все платформы, цены, порядок работы, ответы на вопросы.
"""
for slug, d in CMS.items():
    llms += f"- [{d['name']}]({DOMAIN}/{slug}.html): лечение и восстановление, от {d['price_from']} ₽.\n"
llms += f"\nОбновлено: {BUILD_DATE}\n"
with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as f:
    f.write(llms)
print("written llms.txt")
