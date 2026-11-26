/* ============================================================
   Futurama Shop — скрипт обменника (New New York, 3000 год)
   ============================================================ */

// Курсы: сколько 1 единица валюты стоит в USD (база для расчётов)
const BASE_RATES = {
  USD: 1,
  EUR: 1.085,
  RUB: 0.0107,
  GBP: 1.265,
  JPY: 0.0066,
  BTC: 96500
};

const CURRENCY_LABELS = {
  USD: '💵 USD (Земля ХХ в.)',
  EUR: '💶 EUR (Евро- redundant)',
  RUB: '₽ RUB (Старый Нью-Джерси)',
  GBP: '£ GBP (Лондон Луны)',
  JPY: '¥ JPY (Токио-ORB)',
  BTC: '₿ BTC (Крипто-роботы)'
};

const SPREAD = 0.025; // 2,5 % спред между покупкой и продажей (комиссия робота)

let rates = { ...BASE_RATES };

const els = {
  amountFrom: document.getElementById('amountFrom'),
  amountTo: document.getElementById('amountTo'),
  currencyFrom: document.getElementById('currencyFrom'),
  currencyTo: document.getElementById('currencyTo'),
  swapBtn: document.getElementById('swapBtn'),
  exchangeBtn: document.getElementById('exchangeBtn'),
  feeNote: document.getElementById('feeNote'),
  liveRate: document.getElementById('liveRate'),
  ratesBody: document.getElementById('ratesBody'),
  reviewsList: document.getElementById('reviewsList')
};

// ---------- Конвертация ----------
function toUSD(amount, currency) {
  return amount * rates[currency];
}

function fromUSD(usd, currency) {
  return usd / rates[currency];
}

function convert() {
  const from = els.currencyFrom.value;
  const to = els.currencyTo.value;
  const amount = parseFloat(els.amountFrom.value) || 0;

  const usd = toUSD(amount, from);
  const result = fromUSD(usd, to);
  els.amountTo.value = result.toFixed(2);

  // курс пары
  const pairRate = (rates[to] / rates[from]);
  els.liveRate.textContent = `1 ${from} ≈ ${pairRate.toFixed(4)} ${to}  |  робот Бендер уже считает комиссию…`;
}

function onAmountChange() { convert(); }

// ---------- Обмен ----------
els.exchangeBtn.addEventListener('click', () => {
  const from = els.currencyFrom.value;
  const to = els.currencyTo.value;
  const amount = parseFloat(els.amountFrom.value) || 0;
  const result = parseFloat(els.amountTo.value) || 0;

  if (amount <= 0) {
    alert('Эй, человек! Введи сумму побольше. Ноль не принимаем — это же не доставка Fry.');
    return;
  }

  const quotes = [
    `Сделка совершена! ${amount} ${from} → ${result.toFixed(2)} ${to}. Бендер забирает свою комиссию.`,
    `Ура! Курс выгодный, как уЗойдберговский счёт в банке. ${amount} ${from} обменены на ${result.toFixed(2)} ${to}.`,
    `Готово! Лила уже летит с твоими ${result.toFixed(2)} ${to} на корабле Planet Express.`,
    `Бендер говорит: «Отличная сделка!». ${amount} ${from} = ${result.toFixed(2)} ${to}.`
  ];
  alert(quotes[Math.floor(Math.random() * quotes.length)]);
});

// ---------- Поменять валюты местами ----------
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

// ---------- Таблица курсов ----------
function buildRatesTable() {
  const pairs = [
    ['USD', 'EUR'], ['EUR', 'USD'],
    ['USD', 'RUB'], ['RUB', 'USD'],
    ['USD', 'GBP'], ['GBP', 'USD'],
    ['USD', 'JPY'], ['JPY', 'USD'],
    ['BTC', 'USD'], ['USD', 'BTC']
  ];

  let html = '';
  pairs.forEach(([base, quote]) => {
    const buy = (rates[quote] / rates[base]) * (1 - SPREAD / 2);
    const sell = (rates[quote] / rates[base]) * (1 + SPREAD / 2);
    const change = (Math.random() * 4 - 2).toFixed(2); // -2 .. +2 %
    const dir = change >= 0 ? 'up' : 'down';
    const sign = change >= 0 ? '+' : '';
    html += `
      <tr>
        <td><strong>${base} → ${quote}</strong></td>
        <td>${buy.toFixed(4)}</td>
        <td>${sell.toFixed(4)}</td>
        <td class="change ${dir}">${sign}${change} %</td>
      </tr>
    `;
  });
  els.ratesBody.innerHTML = html;
}

// ---------- Отзывы маскотов ----------
const REVIEWS = [
  { mascot: 'Бендер', text: 'Обменял свою душу на BTC. Не пожалел. (У меня её и так не было.)', stars: '★★★★★' },
  { mascot: 'Фрай', text: 'Я не понял, как это работает, но деньги где-то есть. Вау!', stars: '★★★☆☆' },
  { mascot: 'Лила', text: 'Быстро и надёжно. Курс лучше, чем у任何 робота на Луне.', stars: '★★★★☆' },
  { mascot: 'Цойдберг', text: 'Ура! Бесплатные валюты! Подождите, это не бесплатно? Ой.', stars: '★★☆☆☆' }
];

function buildReviews() {
  els.reviewsList.innerHTML = REVIEWS.map(r => `
    <div class="review-card">
      <p>${r.text}</p>
      <div class="author"><span>${r.mascot}</span><span class="stars">${r.stars}</span></div>
    </div>
  `).join('');
}

// ---------- Симulating live rate updates ----------
function tickRates() {
  Object.keys(rates).forEach(c => {
    const jitter = 1 + (Math.random() * 0.006 - 0.003); // ±0.3 %
    rates[c] = parseFloat((BASE_RATES[c] * jitter).toFixed(6));
  });
  convert();
  buildRatesTable();
}

// ---------- Фон Нью-Нью-Йорка ----------
function initBackground() {
  const canvas = document.getElementById('bgCanvas');
  const ctx = canvas.getContext('2d');
  let width, height;

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  // Здания
  const buildings = [];
  for (let i = 0; i < 14; i++) {
    buildings.push({
      x: (i / 14) * width - 60,
      w: 90 + Math.random() * 140,
      h: 220 + Math.random() * 460,
      color: `hsl(${200 + Math.random() * 60}, 35%, ${18 + Math.random() * 20}%)`,
      windows: Math.floor(10 + Math.random() * 14)
    });
  }

  // Летающие корабли
  const ships = [];
  for (let i = 0; i < 6; i++) {
    ships.push({
      x: Math.random() * width,
      y: Math.random() * (height * 0.55),
      vx: 0.8 + Math.random() * 1.6,
      size: 12 + Math.random() * 18,
      color: i % 2 === 0 ? '#ffeb3b' : '#0ff'
    });
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);

    // Земля / туман
    const grad = ctx.createLinearGradient(0, height * 0.6, 0, height);
    grad.addColorStop(0, 'rgba(0, 20, 40, 0.35)');
    grad.addColorStop(1, 'rgba(5, 16, 32, 0.9)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, height * 0.55, width, height * 0.45);

    // Здания
    buildings.forEach(b => {
      ctx.fillStyle = b.color;
      ctx.fillRect(b.x, height - b.h, b.w, b.h);
      // окна
      ctx.fillStyle = 'rgba(255, 255, 220, 0.85)';
      const cols = 4;
      const rows = Math.ceil(b.windows / cols);
      const bw = b.w / cols - 6;
      const bh = 14;
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const wx = b.x + 6 + c * (b.w / cols);
          const wy = height - b.h + 10 + r * 22;
          if (wy > height - 40 || wx > b.x + b.w - 8) continue;
          if (Math.random() > 0.75) {
            ctx.fillStyle = Math.random() > 0.5 ? '#ffeb3b' : '#ff00ff';
          } else {
            ctx.fillStyle = Math.random() > 0.6 ? 'rgba(255,255,220,0.9)' : 'rgba(0,255,255,0.55)';
          }
          ctx.fillRect(wx, wy, bw, bh);
          ctx.strokeStyle = '#111';
          ctx.lineWidth = 1.5;
          ctx.strokeRect(wx, wy, bw, bh);
        }
      }
    });

    // корабли
    ships.forEach(s => {
      s.x += s.vx;
      if (s.x > width + 40) s.x = -40;
      ctx.fillStyle = s.color;
      ctx.shadowColor = s.color;
      ctx.shadowBlur = 12;
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.size / 2, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;
      // шлейф
      ctx.strokeStyle = s.color;
      ctx.globalAlpha = 0.35;
      ctx.beginPath();
      ctx.moveTo(s.x - s.size / 2, s.y);
      ctx.lineTo(s.x - s.size * 1.6, s.y);
      ctx.stroke();
      ctx.globalAlpha = 1;
    });

    requestAnimationFrame(draw);
  }
  draw();
}

// ---------- Инициализация ----------
els.amountFrom.addEventListener('input', onAmountChange);
els.amountTo.addEventListener('input', onAmountChange);
els.currencyFrom.addEventListener('change', convert);
els.currencyTo.addEventListener('change', convert);

// маскот-цитаты при клике
document.querySelectorAll('.mascot-quote').forEach(btn => {
  btn.addEventListener('click', () => alert(btn.textContent));
});

initBackground();
convert();
buildRatesTable();
buildReviews();
setInterval(tickRates, 3000);
