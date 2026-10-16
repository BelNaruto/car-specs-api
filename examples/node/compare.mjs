#!/usr/bin/env node
/**
 * Compare two (or up to four) models side by side (Node.js 18+, no dependencies)
 * Takes the first EPA trim of each model.
 *
 * API:     https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/car-specs-api
 * Support: Telegram @pintoflow
 *
 *   export RAPIDAPI_KEY=your_key
 *   node compare.mjs "toyota|rav4|2021" "honda|cr-v|2021"
 */
const HOST = 'car-specs-api.p.rapidapi.com';
const KEY = process.env.RAPIDAPI_KEY;
if (!KEY) { console.error('Set RAPIDAPI_KEY first: export RAPIDAPI_KEY=your_key'); process.exit(1); }
const cars = process.argv.slice(2).length ? process.argv.slice(2) : ['toyota|rav4|2021', 'honda|cr-v|2021'];

async function api(path, params) {
  const res = await fetch(`https://${HOST}${path}?${new URLSearchParams(params)}`, { headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': KEY } });
  const body = await res.json();
  if (!body.success) throw new Error(`${path}: ${body.error?.code} ${body.error?.message}`);
  return body.data;
}

const ids = [];
for (const c of cars.slice(0, 4)) {
  const [make, model, year] = c.split('|');
  const d = await api('/trims', { make, model, year });
  const t = (d.trims || d)[0];
  if (!t) { console.log(`No trims for ${c}`); continue; }
  ids.push(t.id);
}
if (ids.length < 2) process.exit(1);

const { vehicles, comparison } = await api('/compare', { ids: ids.join(',') });
const pad = (s, n) => String(s ?? '–').slice(0, n).padEnd(n);
console.log(pad('', 26) + vehicles.map((v) => pad(v.name, 30)).join(''));
for (const [k, row] of Object.entries(comparison)) {
  if (row.values.every((x) => x == null)) continue;
  console.log(pad(k, 26) + row.values.map((x, i) => pad((x ?? '–') + (row.bestId === vehicles[i].id ? ' ✓' : ''), 30)).join(''));
}
