#!/usr/bin/env node
import { readFile } from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";

function parseArgs(argv) {
  const output = {};
  for (let index = 0; index < argv.length; index += 1) {
    if (!argv[index].startsWith("--")) continue;
    const key = argv[index].slice(2);
    output[key] = argv[index + 1] && !argv[index + 1].startsWith("--") ? argv[++index] : true;
  }
  return output;
}

const args = parseArgs(process.argv.slice(2));
const manifest = JSON.parse(await readFile(path.resolve(String(args.project || "production.json")), "utf8"));
let chromium;
const require = createRequire(import.meta.url);
try { ({ chromium } = require("playwright")); }
catch { throw new Error("playwright is required to audit the browser preview"); }

const width = Number(manifest.project?.width);
const height = Number(manifest.project?.height);
const hook = String(args.hook || "__AE_VIDEO__");
const url = String(args.url || "http://127.0.0.1:4173/?capture=1");
const launchOptions = { headless: true };
if (args.chrome) launchOptions.executablePath = path.resolve(String(args.chrome));
const browser = await chromium.launch(launchOptions);
const page = await browser.newPage({ viewport: { width, height } });
const errors = [];
const warnings = [];

function pointInRect(x, y, rect) {
  return x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom;
}

try {
  await page.goto(url, { waitUntil: "load" });
  await page.evaluate(async () => { await document.fonts.ready; });
  if (!await page.evaluate((name) => Boolean(window[name]?.render), hook)) {
    throw new Error(`window.${hook}.render(t) was not found`);
  }

  for (const scene of manifest.scenes || []) {
    const audit = scene.audit || {};
    const times = Array.isArray(audit.checkpoints) && audit.checkpoints.length
      ? audit.checkpoints
      : [(Number(scene.start) + Number(scene.end)) / 2];
    for (const time of times) {
      await page.evaluate(({ hook, time }) => window[hook].render(time), { hook, time });
      await page.evaluate(() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      const report = await page.evaluate(({ audit, focus }) => {
        const rect = (selector) => {
          const element = document.querySelector(selector);
          if (!element) return null;
          const box = element.getBoundingClientRect();
          const style = getComputedStyle(element);
          const range = document.createRange();
          range.selectNodeContents(element);
          const lineRects = [...range.getClientRects()].filter((item) => item.width > 0 && item.height > 0);
          return {
            selector, left: box.left, top: box.top, right: box.right, bottom: box.bottom,
            width: box.width, height: box.height, visible: style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0.01,
            fontSize: parseFloat(style.fontSize), scrollWidth: element.scrollWidth, clientWidth: element.clientWidth,
            scrollHeight: element.scrollHeight, clientHeight: element.clientHeight, lineCount: lineRects.length,
          };
        };
        return {
          requiredVisible: (audit.requiredVisible || []).map(rect),
          singleLine: (audit.singleLine || []).map(rect),
          exactLines: Object.entries(audit.exactLines || {}).map(([selector, expected]) => ({ ...rect(selector), selector, expected })),
          noOverflow: (audit.noOverflow || []).map(rect),
          importantText: (audit.importantText || []).map(rect),
          visualGroup: audit.visualGroup ? rect(audit.visualGroup) : null,
          focus,
          viewport: { width: innerWidth, height: innerHeight },
        };
      }, { audit, focus: scene.focus || null });

      for (const item of report.requiredVisible) {
        if (!item || !item.visible || item.width <= 0 || item.height <= 0) errors.push(`${scene.id}@${time}s missing visible ${item?.selector || "selector"}`);
      }
      for (const item of report.singleLine) {
        if (!item) errors.push(`${scene.id}@${time}s single-line selector missing`);
        else if (item.lineCount !== 1) errors.push(`${scene.id}@${time}s ${item.selector} rendered ${item.lineCount} lines`);
      }
      for (const item of report.exactLines) {
        if (!item || !item.width) errors.push(`${scene.id}@${time}s exact-lines selector missing: ${item?.selector || "selector"}`);
        else if (item.lineCount !== Number(item.expected)) errors.push(`${scene.id}@${time}s ${item.selector} rendered ${item.lineCount} lines; expected ${item.expected}`);
      }
      for (const item of report.noOverflow) {
        if (!item) errors.push(`${scene.id}@${time}s overflow selector missing`);
        else if (item.scrollWidth > item.clientWidth + 1 || item.scrollHeight > item.clientHeight + 1) errors.push(`${scene.id}@${time}s ${item.selector} overflows (${item.scrollWidth}x${item.scrollHeight} content in ${item.clientWidth}x${item.clientHeight})`);
      }
      const minimum = Number(manifest.constraints?.minImportantFontPxAtOutput || 0) / Number(manifest.render?.pixelScale || 1);
      for (const item of report.importantText) {
        if (!item) errors.push(`${scene.id}@${time}s important-text selector missing`);
        else if (minimum && item.fontSize < minimum) warnings.push(`${scene.id}@${time}s ${item.selector} font ${item.fontSize}px is below logical minimum ${minimum}px`);
      }
      if (report.visualGroup && report.focus) {
        const gx = (report.visualGroup.left + report.visualGroup.right) / 2 / report.viewport.width;
        const gy = (report.visualGroup.top + report.visualGroup.bottom) / 2 / report.viewport.height;
        if (Math.hypot(gx - report.focus.x, gy - report.focus.y) > 0.1) warnings.push(`${scene.id}@${time}s visual group (${gx.toFixed(3)},${gy.toFixed(3)}) and declared focus (${report.focus.x},${report.focus.y}) differ`);
      }
    }
  }

  for (const [index, interaction] of (manifest.interactions || []).entries()) {
    if (interaction.action !== "click" || !interaction.target) continue;
    await page.evaluate(({ hook, time }) => window[hook].render(time), { hook, time: interaction.time });
    await page.evaluate(() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    const target = await page.evaluate((selector) => {
      const element = document.querySelector(selector);
      if (!element) return null;
      const box = element.getBoundingClientRect();
      return { left: box.left, top: box.top, right: box.right, bottom: box.bottom };
    }, interaction.target);
    if (!target) errors.push(`interactions[${index}] target not found: ${interaction.target}`);
    else if (!pointInRect(interaction.x * width, interaction.y * height, target)) errors.push(`interactions[${index}] click (${(interaction.x * width).toFixed(1)},${(interaction.y * height).toFixed(1)}) misses ${interaction.target} rect (${target.left.toFixed(1)},${target.top.toFixed(1)})-(${target.right.toFixed(1)},${target.bottom.toFixed(1)})`);
  }
} finally {
  await browser.close();
}

for (const warning of warnings) console.log(`warning: ${warning}`);
for (const error of errors) console.log(`error: ${error}`);
console.log(`${errors.length} error(s), ${warnings.length} warning(s)`);
process.exitCode = errors.length || (args.strict && warnings.length) ? 1 : 0;
