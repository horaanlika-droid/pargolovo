/* ============================================================
   Futurama Shop — скрипт (New New York, 3000 год)
   Валюты + Подарочные карты, у каждой — свой курс
   ============================================================ */

/* ---------- Валюты (старый блок) ---------- */
const BASE_RATES = {
  USD: 1,
  EUR: 1.085,
  RUB: 0.0107,
  GBP: 1.265,
  JPY: 0.0066,
  BTC: 96500
};
const SPREAD = 0.025;
let rates = { ...BASE_RATES };

/* ---------- Подарочные карты — КАЖДАЯ СО СВОИМ КУРСОМ ---------- */
const GIFT_CARDS = [
  {
    id: 'apple',
    brand: 'Apple',
    title: 'Apple & iTunes',
    country: 'США',
    flag: '🇺🇸',
    icon: '🍎',
    category: 'shop',
    nominalCurrency: 'USD',
    nominalSymbol: '$',
    payoutCurrency: 'RUB',
    buyRate: 82.50,
    sellRate: 94.80,
    fee: 2.5,
    change: 0.84,
    trend: 'up',
    badge: 'Топ продаж',
    badgeClass: 'badge-top',
    desc: 'App Store, iCloud, Apple Music — код за 2 минуты',
    popular: true
  },
  {
    id: 'google',
    brand: 'Google Play',
    title: 'Google Play',
    country: 'США',
    flag: '🇺🇸',
    icon: '▶️',
    category: 'shop',
    nominalCurrency: 'USD',
    nominalSymbol: '$',
    payoutCurrency: 'RUB',
    buyRate: 79.90,
    sellRate: 92.00,
    fee: 3.0,
    change: -0.42,
    trend: 'down',
    badge: 'Выгодно',
    badgeClass: 'badge-good',
    desc: 'Игры, приложения, подписки — работает везде',
    popular: false
  },
  {
    id: 'steam',
    brand: 'Steam',
    title: 'Steam Wallet',
    country: 'США',
    flag: '🇺🇸',
    icon: '🎮',
    category: 'games',
    nominalCurrency: 'USD',
    nominalSymbol: '$',
    payoutCurrency: 'RUB',
    buyRate: 77.80,
    sellRate: 90.50,
    fee: 4.2,
    change: 1.12,
    trend: 'up',
    badge: 'Хит',
    badgeClass: 'badge-hit',
    desc: 'Лучший подарок геймеру, код на почту',
    popular: true
  },
  {
    id: 'psn',
    brand: 'PlayStation',
    title: 'PlayStation Store',
    country: 'США',
    flag: '🇺🇸',
    icon: '🎧',
    category: 'games',
    nominalCurrency: 'USD',
    nominalSymbol: '$',
    payoutCurrency: 'RUB',
    buyRate: 84.00,
    sellRate: 95.60,
    fee: 2.8,
    change: 0.35,
    trend: 'up',
    badge: null,
    badgeClass: '',
    desc: 'PS Plus, игры, DLC — регион США',
    popular: false
  },
  {
    id: 'xbox',
    brand: 'Xbox',
    title: 'Xbox Gift Card',
    country: 'США',
    flag: '🇺🇸',
    icon: '🟩',
    category: 'games',
    nominalCurrency: 'USD',
    nominalSymbol: '$',
    payoutCurrency: 'RUB',
    buyRate: 83.20,
    sellRate: 94.90,
    fee: 2.9,
    change: -0.18,
    trend: 'down',
    badge: null,
    badgeClass: '',
    desc: 'Game Pass, игры и баланс Microsoft',
    popular: false
  },
  {
    id: 'amazon',
    brand: 'Amazon',
    title: 'Amazon',
    country: 'США',
    flag: '🇺🇸',
    icon: '📦',
    category: 'shop',
    nominalCurrency: 'USD',
    nominalSymbol: '$',
    payoutCurrency: 'RUB',
    buyRate: 81.10,
    sellRate: 93.40,
    fee: 3.2,
    change: 0.67,
    trend: 'up',
    badge: null,
    badgeClass: '',
    desc: 'Товары и баланс аккаунта Amazon.com',
    popular: false
  },
  {
    id: 'netflix',
    brand: 'Netflix',
    title: 'Netflix Premium',
    country: 'Турция',
    flag: '🇹🇷',
    icon: '🎬',
    category: 'media',
    nominalCurrency: 'TRY',
    nominalSymbol: '₺',
    payoutCurrency: 'RUB',
    buyRate: 2.85,
    sellRate: 3.40,
    fee: 3.5,
    change: -1.05,
    trend: 'down',
    badge: 'Акция',
    badgeClass: 'badge-sale',
    desc: 'Подписка на 1 месяц, работает в РФ',
    popular: true
  },
  {
    id: 'spotify',
    brand: 'Spotify',
    title: 'Spotify Premium',
    country: 'США',
    flag: '🇺🇸',
    icon: '🎵',
    category: 'media',
    nominalCurrency: 'USD',
    nominalSymbol: '$',
    payoutCurrency: 'RUB',
    buyRate: 86.30,
    sellRate: 97.20,
    fee: 2.2,
    change: 0.22,
    trend: 'up',
    badge: null,
    badgeClass: '',
    desc: 'Индивидуальная подписка на 1 год',
    popular: false
  },
  {
    id: 'ozon',
    brand: 'Ozon',
    title: 'Ozon',
    country: 'Россия',
    flag: '🇷🇺',
    icon: '🛒',
    category: 'ru',
    nominalCurrency: 'RUB',
    nominalSymbol: '₽',
    payoutCurrency: 'RUB',
    buyRate: 0.88,
    sellRate: 0.98,
    fee: 1.8,
    change: 0.05,
    trend: 'up',
    badge: 'Моментально',
    badgeClass: 'badge-ru',
    desc: 'Сертификат OZON 500–30 000 ₽, за 60 секунд',
    popular: true
  }
];

// Мутабельные курсы карт (для живых обновлений)
let giftRates = {};
GIFT_CARDS.forEach(c => {
  giftRates[c.id] = {
    buy: c.buyRate,
    sell: c.sellRate,
    change: c.change,
    trend: c.trend
  };
});

let selectedGiftId = 'apple';
let giftMode = 'sell'; // sell = клиент продаёт карту, buy = клиент покупает карту
let activeFilter = 'all';

/* ---------- DOM ---------- */
const els = {
  amountFrom: document.getElementById('amountFrom'),
  amountTo: document.getElementById('amountTo'),
  currencyFrom: document.getElementById('currencyFrom'),
  currencyTo: document.getElementById('currencyTo'),
  swapBtn: document.getElementById('swapBtn'),
  exchangeBtn: document.getElementById('exchangeBtn'),
  liveRate: document.getElementById('liveRate'),
  ratesBody: document.getElementById('ratesBody'),
  reviewsList: document.getElementById('reviewsList'),
  // gift
  giftGrid: document.getElementById('giftGrid'),
  giftRatesBody: document.getElementById('giftRatesBody'),
  giftSelect: document.getElementById('giftSelect'),
  giftAmount: document.getElementById('giftAmount'),
  giftResult: document.getElementById('giftResult'),
  giftSwapBtn: document.getElementById('giftSwapBtn'),
  giftActionBtn: document.getElementById('giftActionBtn'),
  giftCalcRate: document.getElementById('giftCalcRate'),
  giftCalcTitle: document.getElementById('giftCalcTitle'),
  giftCalcSubtitle: document.getElementById('giftCalcSubtitle'),
  giftFromLabel: document.getElementById('giftFromLabel'),
  giftToLabel: document.getElementById('giftToLabel'),
  giftNominalHint: document.getElementById('giftNominalHint'),
  giftResultHint: document.getElementById('giftResultHint'),
  giftFeeNote: document.getElementById('giftFeeNote'),
  detailCard: document.getElementById('detailCard'),
  detailRate: document.getElementById('detailRate'),
  detailFee: document.getElementById('detailFee'),
  modeSwitch: document.getElementById('modeSwitch')
};

function getSelectedGift() {
  return GIFT_CARDS.find(g => g.id === selectedGiftId);
}

function formatNumber(n, decimals = 2) {
  return n.toFixed(decimals).replace('.', ',');
}

function formatRate(n) {
  return n.toFixed(2).replace('.', ',');
}

/* ---------- Валютный обмен (старый) ---------- */
function toUSD(amount, currency) { return amount * rates[currency]; }
function fromUSD(usd, currency) { return usd / rates[currency]; }

function convert() {
  if (!els.amountFrom || !els.currencyFrom) return;
  const from = els.currencyFrom.value;
  const to = els.currencyTo.value;
  const amount = parseFloat(els.amountFrom.value) || 0;
  const usd = toUSD(amount, from);
  const result = fromUSD(usd, to);
  if (els.amountTo) els.amountTo.value = result ? result.toFixed(2) : '';
  if (els.liveRate) {
    const pairRate = (rates[from] ? (rates[to] / rates[from]) : 0);
    els.liveRate.textContent = `1 ${from} ≈ ${pairRate.toFixed(4)} ${to}  •  обновление каждые 3 сек`;
  }
}
function onAmountChange(){ convert(); }

if (els.exchangeBtn) {
  els.exchangeBtn.addEventListener('click', () => {
    const from = els.currencyFrom.value;
    const to = els.currencyTo.value;
    const amount = parseFloat(els.amountFrom.value) || 0;
    const result = parseFloat(els.amountTo.value) || 0;
    if (amount <= 0) {
      alert('Эй, человек! Введи сумму больше нуля. Ноль не принимаем — это ж не бесплатный Слёрм.');
      return;
    }
    const quotes = [
      `Сделка совершена! ${amount} ${from} → ${result.toFixed(2)} ${to}. Бендер уже считает комиссию.`,
      `Ура! Курс выгодный, как у Цойдберга в банке. ${amount} ${from} обменяли на ${result.toFixed(2)} ${to}.`,
      `Готово! Лила везёт твои ${result.toFixed(2)} ${to} на корабле Planet Express.`,
      `Бендер говорит: «Отличная сделка!». ${amount} ${from} = ${result.toFixed(2)} ${to}.`
    ];
    alert(quotes[Math.floor(Math.random() * quotes.length)]);
  });
}
if (els.swapBtn) {
  els.swapBtn.addEventListener('click', () => {
    const from = els.currencyFrom.value;
    const to = els.currencyTo.value;
    els.currencyFrom.value = to;
    els.currencyTo.value = from;
    const tmp = els.amountFrom.value;
    els.amountFrom.value = els.amountTo.value || '';
    els.amountTo.value = tmp || '';
    convert();
  });
}

function buildRatesTable() {
  if (!els.ratesBody) return;
  const pairs = [
    ['USD','EUR'],['EUR','USD'],
    ['USD','RUB'],['RUB','USD'],
    ['USD','GBP'],['GBP','USD'],
    ['USD','JPY'],['JPY','USD'],
    ['BTC','USD'],['USD','BTC']
  ];
  let html='';
  pairs.forEach(([base,quote])=>{
    const buy=(rates[quote]/rates[base])*(1-SPREAD/2);
    const sell=(rates[quote]/rates[base])*(1+SPREAD/2);
    const change=(Math.random()*4-2).toFixed(2);
    const dir=change>=0?'up':'down';
    const sign=change>=0?'+':'';
    html+=`<tr><td><strong>${base} → ${quote}</strong></td><td>${buy.toFixed(4).replace('.',',')}</td><td>${sell.toFixed(4).replace('.',',')}</td><td class="change ${dir}">${sign}${change.replace('.',',')} %</td></tr>`;
  });
  els.ratesBody.innerHTML=html;
}

/* ---------- Подарочные карты: рендер сетки ---------- */
function renderGiftGrid() {
  if (!els.giftGrid) return;
  const filtered = GIFT_CARDS.filter(c => {
    if (activeFilter==='all') return true;
    return c.category===activeFilter;
  });

  els.giftGrid.innerHTML = filtered.map(card=>{
    const r = giftRates[card.id];
    const isSelected = card.id===selectedGiftId;
    const trendIcon = r.trend==='up' ? '▲' : '▼';
    const trendClass = r.trend==='up' ? 'up' : 'down';
    const sign = r.change>=0?'+':'';
    const buyFormatted = formatRate(r.buy);
    const sellFormatted = formatRate(r.sell);
    const nominalLabel = card.nominalCurrency==='RUB' ? '1 ₽ номинала' : `1 ${card.nominalSymbol} =`;
    const unit = card.payoutCurrency==='RUB' ? '₽' : card.payoutCurrency;

    return `
      <article class="gift-card ${isSelected?'selected':''}" data-id="${card.id}" data-category="${card.category}">
        ${card.badge?`<span class="gift-badge ${card.badgeClass}">${card.badge}</span>`:''}
        ${isSelected?'<span class="gift-chosen">✓ выбрано</span>':''}
        <div class="gift-card-top">
          <div class="gift-icon-wrap">
            <div class="gift-icon">${card.icon}</div>
            <div class="gift-flag">${card.flag}</div>
          </div>
          <div class="gift-title-wrap">
            <div class="gift-brand">${card.brand} <span class="gift-country">• ${card.country}</span></div>
            <div class="gift-title">${card.title}</div>
            <div class="gift-desc">${card.desc}</div>
          </div>
        </div>

        <div class="gift-rates-mini">
          <div class="rate-box buy">
            <span class="rate-label">Покупка</span>
            <span class="rate-value">${buyFormatted} ${unit}</span>
            <span class="rate-sub">${nominalLabel}</span>
          </div>
          <div class="rate-divider"></div>
          <div class="rate-box sell">
            <span class="rate-label">Продажа</span>
            <span class="rate-value">${sellFormatted} ${unit}</span>
            <span class="rate-sub">${nominalLabel}</span>
          </div>
        </div>

        <div class="gift-card-bottom">
          <span class="gift-change ${trendClass}">${trendIcon} ${sign}${formatRate(r.change)} % за день</span>
          <span class="gift-fee">комиссия ${card.fee}% в курсе</span>
        </div>
        <button class="gift-mini-btn" type="button">Выбрать курс →</button>
      </article>
    `;
  }).join('');

  // навешиваем клики
  document.querySelectorAll('.gift-card').forEach(el=>{
    el.addEventListener('click', ()=>{
      selectedGiftId = el.dataset.id;
      renderGiftGrid();
      renderGiftRatesTable();
      syncGiftSelect();
      calcGift();
      // мягкий скролл к калькулятору на мобилках
      if (window.innerWidth < 700) {
        document.getElementById('giftCalc').scrollIntoView({behavior:'smooth', block:'start'});
      }
    });
  });
}

function renderGiftRatesTable(){
  if (!els.giftRatesBody) return;
  els.giftRatesBody.innerHTML = GIFT_CARDS.map(card=>{
    const r = giftRates[card.id];
    const trendIcon = r.trend==='up' ? '▲' : '▼';
    const trendClass = r.trend==='up' ? 'up' : 'down';
    const sign = r.change>=0?'+':'';
    const buy = formatRate(r.buy);
    const sell = formatRate(r.sell);
    const nominal = card.nominalCurrency==='RUB' ? 'за 1 ₽' : `за 1 ${card.nominalSymbol}`;
    const isSelected = card.id===selectedGiftId;
    return `
      <tr class="${isSelected?'row-selected':''}">
        <td>
          <div class="table-card">
            <span class="table-icon">${card.icon}</span>
            <span><strong>${card.title}</strong><br><small>${card.flag} ${card.country} • ${card.nominalCurrency}</small></span>
          </div>
        </td>
        <td><strong>${buy} ₽</strong><br><small>${nominal}</small></td>
        <td><strong>${sell} ₽</strong><br><small>${nominal}</small></td>
        <td class="change ${trendClass}">${trendIcon} ${sign}${formatRate(r.change)} %</td>
        <td><button class="table-pick ${isSelected?'active':''}" data-pick="${card.id}">${isSelected?'✓ выбран':'Выбрать'}</button></td>
      </tr>
    `;
  }).join('');

  document.querySelectorAll('[data-pick]').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      selectedGiftId = btn.dataset.pick;
      renderGiftGrid();
      renderGiftRatesTable();
      syncGiftSelect();
      calcGift();
    });
  });
}

function syncGiftSelect(){
  if (!els.giftSelect) return;
  els.giftSelect.value = selectedGiftId;
  updateGiftCalcHeader();
}

function updateGiftCalcHeader(){
  const card = getSelectedGift();
  const r = giftRates[card.id];
  if (!card) return;
  const modeLabelSell = `🍎 ${card.title} — калькулятор`;
  const modeLabelBuy = `🛍️ ${card.title} — покупка`;
  els.giftCalcTitle.textContent = giftMode==='sell' ? `${card.icon} ${card.title} — продать` : `${card.icon} ${card.title} — купить`;
  els.giftCalcSubtitle.textContent = card.desc + ` • Номинал в ${card.nominalCurrency}`;
  // rate badge
  const activeRate = giftMode==='sell' ? r.buy : r.sell;
  const verb = giftMode==='sell' ? 'покупка' : 'продажа';
  els.giftCalcRate.textContent = `${formatRate(activeRate)} ₽ ${verb} за 1 ${card.nominalSymbol}`;
  // labels
  els.giftFromLabel.textContent = giftMode==='sell' ? `Номинал карты (${card.nominalCurrency})` : `Сколько хотите карт (${card.nominalCurrency})`;
  els.giftToLabel.textContent = giftMode==='sell' ? `Вы получите (${card.payoutCurrency})` : `Вы заплатите (${card.payoutCurrency})`;
  els.giftNominalHint.textContent = card.nominalCurrency==='RUB' ? 'Например: 1000 ₽, 3000 ₽, 5000 ₽' : `Например: 25 ${card.nominalSymbol}, 50 ${card.nominalSymbol}, 100 ${card.nominalSymbol}`;
  els.giftResultHint.textContent = giftMode==='sell' ? `По курсу ${formatRate(activeRate)} ₽ за 1 ${card.nominalSymbol}` : `По курсу ${formatRate(activeRate)} ₽ за 1 ${card.nominalSymbol}`;
  els.detailCard.textContent = `${card.title} (${card.flag} ${card.country})`;
  els.detailRate.textContent = `${formatRate(activeRate)} ₽ за 1 ${card.nominalSymbol} • ${verb}`;
  els.detailFee.textContent = `${card.fee}% — уже включена в курс`;
  els.giftFeeNote.textContent = giftMode==='sell'
    ? `Мы покупаем ваш ${card.title} по ${formatRate(r.buy)} ₽ за 1 ${card.nominalSymbol}, продаём по ${formatRate(r.sell)} ₽. Комиссия ${card.fee}% уже в курсе.`
    : `Мы продаём ${card.title} по ${formatRate(r.sell)} ₽ за 1 ${card.nominalSymbol}, покупаем по ${formatRate(r.buy)} ₽. Комиссия ${card.fee}% уже в курсе.`;
  els.giftActionBtn.textContent = giftMode==='sell' ? `Продать ${card.title} → получить рубли` : `Купить ${card.title} → оплатить`;
}

function calcGift(){
  const card = getSelectedGift();
  if (!card) return;
  const r = giftRates[card.id];
  const amount = parseFloat(els.giftAmount.value) || 0;
  const rate = giftMode==='sell' ? r.buy : r.sell;
  const result = amount * rate;
  if (amount <= 0) {
    els.giftResult.value = '';
    return;
  }
  // для RUB номиналов не нужно много знаков
  if (card.nominalCurrency==='RUB') {
    els.giftResult.value = result.toFixed(2);
  } else {
    els.giftResult.value = result.toFixed(2);
  }
  updateGiftCalcHeader();
}

/* ---------- События подарочных карт ---------- */
function initGiftSelect(){
  if (!els.giftSelect) return;
  els.giftSelect.innerHTML = GIFT_CARDS.map(c=> `<option value="${c.id}">${c.icon} ${c.title} — ${c.flag} ${c.country} (${c.nominalCurrency})</option>`).join('');
  els.giftSelect.value = selectedGiftId;
  els.giftSelect.addEventListener('change', ()=>{
    selectedGiftId = els.giftSelect.value;
    renderGiftGrid();
    renderGiftRatesTable();
    calcGift();
  });
}

if (els.giftAmount) {
  els.giftAmount.addEventListener('input', calcGift);
}
if (els.giftSwapBtn) {
  els.giftSwapBtn.addEventListener('click', ()=>{
    giftMode = giftMode==='sell' ? 'buy' : 'sell';
    document.querySelectorAll('.mode-btn').forEach(b=>{
      b.classList.toggle('active', b.dataset.mode===giftMode);
    });
    calcGift();
  });
}
document.querySelectorAll('.mode-btn').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    giftMode = btn.dataset.mode;
    document.querySelectorAll('.mode-btn').forEach(b=> b.classList.remove('active'));
    btn.classList.add('active');
    calcGift();
  });
});
if (els.giftActionBtn) {
  els.giftActionBtn.addEventListener('click', ()=>{
    const card = getSelectedGift();
    const amount = parseFloat(els.giftAmount.value) || 0;
    const result = parseFloat(els.giftResult.value) || 0;
    if (amount <= 0) {
      alert('Введи номинал карты, человек! Бендер не работает с нулём — даже Цойдберг больше принесёт.');
      return;
    }
    if (giftMode==='sell') {
      alert(`Заявка принята! ✅\n\nКарта: ${card.title} (${card.country})\nНоминал: ${amount} ${card.nominalSymbol}\nКурс: ${formatRate(giftRates[card.id].buy)} ₽ за 1 ${card.nominalSymbol} (свой курс карты)\nВы получите: ${result.toFixed(2)} ₽\n\nЛила проверит код и переведёт рубли за 2–5 минут. Не закрывай вкладку — робот уже бежит!`);
    } else {
      alert(`Заявка на покупку принята! 🛍️\n\nКарта: ${card.title} (${card.country})\nНоминал: ${amount} ${card.nominalSymbol}\nКурс: ${formatRate(giftRates[card.id].sell)} ₽ за 1 ${card.nominalSymbol} (свой курс карты)\nК оплате: ${result.toFixed(2)} ₽\n\nОплати и получи код на почту. Бендер гарантирует — код свежий, как вчерашняя голова Фрая!`);
    }
  });
}

// Фильтры
document.querySelectorAll('.filter-btn').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    activeFilter = btn.dataset.filter;
    renderGiftGrid();
  });
});

/* ---------- Отзывы ---------- */
const REVIEWS = [
  { mascot: 'Бендер', text: 'Продал Apple на 100 $ по 82,50 ₽ — выхлоп 8 250 ₽. Обменял душу бы дешевле, но её нет.', stars: '★★★★★' },
  { mascot: 'Фрай', text: 'Не понял, чем Steam по 77,8 ₽ отличается от Google по 79,9 ₽, но деньги пришли. Вау!', stars: '★★★★★' },
  { mascot: 'Лила', text: 'У каждой карты — свой курс, всё честно. Проверила все коды, жуликов выкинула в космос.', stars: '★★★★☆' },
  { mascot: 'Цойдберг', text: 'Купил Ozon по 0,98 ₽ за рубль — ура! Почти даром! Все завидуют!', stars: '★★★★★' }
];
function buildReviews(){
  if (!els.reviewsList) return;
  els.reviewsList.innerHTML = REVIEWS.map(r=>`<div class="review-card"><p>${r.text}</p><div class="author"><span>${r.mascot}</span><span class="stars">${r.stars}</span></div></div>`).join('');
}

/* ---------- Живые обновления курсов ---------- */
function tickRates(){
  // валюты
  Object.keys(rates).forEach(c=>{
    const jitter=1+(Math.random()*0.006-0.003);
    rates[c]=parseFloat((BASE_RATES[c]*jitter).toFixed(6));
  });
  convert();
  buildRatesTable();

  // подарочные карты — каждая дёргается отдельно
  GIFT_CARDS.forEach(card=>{
    const curr = giftRates[card.id];
    const jitterBuy = 1 + (Math.random()*0.008 - 0.004); // ±0.4%
    const jitterSell = 1 + (Math.random()*0.008 - 0.004);
    curr.buy = parseFloat((curr.buy * jitterBuy).toFixed(2));
    // сохраняем коридор: продажа всегда выше покупки минимум на 8 ₽
    curr.sell = parseFloat((curr.sell * jitterSell).toFixed(2));
    if (curr.sell < curr.buy + 6) curr.sell = parseFloat((curr.buy + 8 + Math.random()*4).toFixed(2));
    // изменение за день тоже скачет
    curr.change = parseFloat((curr.change + (Math.random()*0.4 - 0.2)).toFixed(2));
    curr.trend = curr.change >= 0 ? 'up' : 'down';
    // ограничим
    if (curr.change > 2.5) curr.change = 2.5;
    if (curr.change < -2.5) curr.change = -2.5;
  });
  renderGiftGrid();
  renderGiftRatesTable();
  calcGift();
}

/* ---------- Фон ---------- */
function initBackground(){
  const canvas=document.getElementById('bgCanvas');
  if (!canvas) return;
  const ctx=canvas.getContext('2d');
  let width,height;
  function resize(){ width=canvas.width=window.innerWidth; height=canvas.height=window.innerHeight; }
  window.addEventListener('resize', resize); resize();
  const buildings=[];
  for(let i=0;i<14;i++) buildings.push({ x:(i/14)*width-60, w:90+Math.random()*140, h:220+Math.random()*460, color:`hsl(${200+Math.random()*60},35%,${18+Math.random()*20}%)`, windows:Math.floor(10+Math.random()*14) });
  const ships=[];
  for(let i=0;i<6;i++) ships.push({ x:Math.random()*width, y:Math.random()*(height*0.55), vx:0.8+Math.random()*1.6, size:12+Math.random()*18, color:i%2===0?'#ffeb3b':'#0ff' });
  function draw(){
    ctx.clearRect(0,0,width,height);
    const grad=ctx.createLinearGradient(0,height*0.6,0,height);
    grad.addColorStop(0,'rgba(0,20,40,0.35)'); grad.addColorStop(1,'rgba(5,16,32,0.9)');
    ctx.fillStyle=grad; ctx.fillRect(0,height*0.55,width,height*0.45);
    buildings.forEach(b=>{
      ctx.fillStyle=b.color; ctx.fillRect(b.x,height-b.h,b.w,b.h);
      const cols=4; const rows=Math.ceil(b.windows/cols); const bw=b.w/cols-6; const bh=14;
      for(let r=0;r<rows;r++) for(let c=0;c<cols;c++){
        const wx=b.x+6+c*(b.w/cols); const wy=height-b.h+10+r*22;
        if(wy>height-40||wx>b.x+b.w-8) continue;
        ctx.fillStyle=Math.random()>0.75 ? (Math.random()>0.5?'#ffeb3b':'#ff00ff') : (Math.random()>0.6?'rgba(255,255,220,0.9)':'rgba(0,255,255,0.55)');
        ctx.fillRect(wx,wy,bw,bh); ctx.strokeStyle='#111'; ctx.lineWidth=1.5; ctx.strokeRect(wx,wy,bw,bh);
      }
    });
    ships.forEach(s=>{
      s.x+=s.vx; if(s.x>width+40) s.x=-40;
      ctx.fillStyle=s.color; ctx.shadowColor=s.color; ctx.shadowBlur=12;
      ctx.beginPath(); ctx.arc(s.x,s.y,s.size/2,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0;
      ctx.strokeStyle=s.color; ctx.globalAlpha=0.35; ctx.beginPath(); ctx.moveTo(s.x-s.size/2,s.y); ctx.lineTo(s.x-s.size*1.6,s.y); ctx.stroke(); ctx.globalAlpha=1;
    });
    requestAnimationFrame(draw);
  }
  draw();
}

/* ---------- Инициализация ---------- */
if (els.amountFrom) els.amountFrom.addEventListener('input', onAmountChange);
if (els.amountTo) els.amountTo.addEventListener('input', onAmountChange);
if (els.currencyFrom) els.currencyFrom.addEventListener('change', convert);
if (els.currencyTo) els.currencyTo.addEventListener('change', convert);
document.querySelectorAll('.mascot-quote').forEach(btn=> btn.addEventListener('click', ()=> alert(btn.textContent)));

initBackground();
initGiftSelect();
renderGiftGrid();
renderGiftRatesTable();
calcGift();
convert();
buildRatesTable();
buildReviews();
setInterval(tickRates, 3000);
