# Контекст работы с Devin (для продолжения с любого аккаунта)

Актуальная сессия: https://app.devin.ai/sessions/12d6faf7084146f1bf1d381ea5792e61
(история диалога хранится в сессии; при смене аккаунта используйте этот файл как контекст)

## Проект

Статический сайт SiteRescue24 / IntelPrime — срочное лечение сайтов от вирусов и восстановление
после взлома (WordPress, Bitrix, OpenCart, MODX, Joomla, самописный PHP).

- Репозиторий: https://github.com/bratkaprod-cell/new
- Рабочая ветка с правками: `devin/1787589000-facts-block-redesign`
- PR в `main`: https://github.com/bratkaprod-cell/new/pull/1 (открыт, не смержен)
- Скачать zip актуальной ветки:
  https://github.com/bratkaprod-cell/new/archive/refs/heads/devin/1787589000-facts-block-redesign.zip

## Как собирать и запускать

- Все страницы (`index.html`, `wordpress.html`, `bitrix.html`, `opencart.html`, `modx.html`,
  `joomla.html`, `php.html`, `sitemap.xml`, `robots.txt`, `llms.txt`) генерируются из `build.py`:
  `python build.py`. **HTML руками не править — только build.py.**
- Стили: `assets/style.css`, JS (бургер-меню, модалка, формы, sticky CTA): `assets/main.js`.
- Локальный просмотр: `python -m http.server 8000` из корня репозитория.

## Что сделано в текущей ветке (PR #1)

1. Блок «Кратко: что, за сколько и как быстро» переделан из таблицы в карточки с SVG-иконками
   (`facts_section()` в build.py) + тёмная CTA-панель с ценой «от 6 900 ₽», кнопкой и контактами.
   Адаптив: desktop 2 колонки + панель справа; ≤960px панель вниз; ≤600px одна колонка.
2. Исправлен баг мобильной шапки: на ≤480px кнопка «Спасти сайт» скрывается, логотип меньше —
   бургер больше не уходит за край экрана на 375px.
3. Исправлено «мигание» тега «самая массовая CMS» на карточках CMS: у `.card:hover` убран
   `translateY` (вызывал дребезг hover), оставлены border + box-shadow. Цвет тегов — `#5b5b5b`.
4. Вставлены логотип IntelPrime (`assets/logo.png`, в шапке/футере/мобильном меню; высота
   36px desktop / 30px ≤560px / 26px ≤480px) и favicon (`assets/favicon.png`).

Всё протестировано на desktop, 768px и 375px — записи и скриншоты в комментариях к PR #1.

## Коммерческие данные сайта

Диагностика бесплатно · ответ за 10 минут · срок 4–12 ч (макс. 24 ч) · без предоплаты ·
цена от 6 900 ₽ · подписка «Охрана» 1 990 ₽/мес · гарантия 1 год письменно · заявки 24/7 ·
вся Россия и СНГ, удалённо. Контакты в build.py — плейсхолдеры (+7 900 000-00-00 и т.п.),
их нужно заменить на реальные.

## Прочее

- В `cms/textolite/` лежит CMS Textolite; аудит безопасности — `docs/textolite-audit.md`,
  общий security-обзор — `docs/security-review-site-and-cms.md`.
- Возможная будущая задача: своя лёгкая CMS для правки текстов/картинок/цветов без кода
  (хранение в JSON + интеграция с build.py или PHP-рантайм под Apache/.htaccess).
