#!/usr/bin/env node
/**
 * VIN → full specs in your terminal (Node.js 18+, no dependencies)
 *
 * API:     https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/car-specs-api
 * Support: Telegram @pintoflow
 *
 *   export RAPIDAPI_KEY=your_key
 *   node vin-to-specs.mjs 1HGCM82633A004352
 */
const HOST = 'car-specs-api.p.rapidapi.com';
const KEY = process.env.RAPIDAPI_KEY;
if (!KEY) { console.error('Set RAPIDAPI_KEY first: export RAPIDAPI_KEY=your_key'); process.exit(1); }
const vin = (process.argv[2] || '1HGCM82633A004352').toUpperCase();

const res = await fetch(`https://${HOST}/vin/specs?vin=${encodeURIComponent(vin)}`, { headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': KEY } });
const body = await res.json();
if (!body.success) { console.error(`${body.error?.code}: ${body.error?.message}`); process.exit(1); }

const { vin: v, trims = [], specs = [], dimensions = [], safetyRatings = [], images = [], likelyTrimIds = [] } = body.data;
(body.meta.warnings || []).forEach((w) => console.log('⚠️  ' + w));
console.log(`\n${v.modelYear} ${v.make} ${v.model} ${v.trim || ''}  (${v.bodyClass || ''})`);
console.log(`Engine: ${v.engine?.displacementL ?? '?'} L ${v.engine?.cylinders ?? '?'}-cyl${v.engine?.horsepower ? `, ${v.engine.horsepower} hp` : ''}`);
console.log(`Built in: ${[v.plant?.city, v.plant?.state, v.plant?.country].filter(Boolean).join(', ')}`);

console.log('\nMatching trims:');
for (const t of trims) console.log(`  ${likelyTrimIds.includes(t.id) ? '✓' : ' '} [${t.id}] ${t.model} – ${t.option}`);

const s = specs.find((x) => likelyTrimIds.includes(x.id)) || specs[0];
if (s) console.log(`\nMPG ${s.fuelEconomy?.mpg?.city}/${s.fuelEconomy?.mpg?.highway}/${s.fuelEconomy?.mpg?.combined} (city/hwy/comb) · ${s.emissions?.co2GramsPerMile} g CO₂/mi · ~$${s.costs?.annualFuelCostUsd}/yr fuel`);
const d = dimensions[0];
if (d) console.log(`Size ${d.imperial.lengthIn}" L × ${d.imperial.widthIn}" W × ${d.imperial.heightIn}" H, ${d.imperial.curbWeightLb} lb`);
if (safetyRatings[0]) console.log(`NHTSA overall: ${safetyRatings[0].overallRating}/5`);
if (images[0]) console.log(`Photo: ${images[0].url}\n  (${images[0].attribution})`);
