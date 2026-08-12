#!/usr/bin/env node
import { access, mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";
import { createRequire } from "node:module";

function parseArgs(argv) {
  const output = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = argv[index + 1];
    output[key] = !next || next.startsWith("--") ? true : next;
    if (output[key] !== true) index += 1;
  }
  return output;
}

async function exists(filePath) {
  try { await access(filePath); return true; } catch { return false; }
}

function run(command, args, capture = false) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    const child = spawn(command, args, { stdio: capture ? ["ignore", "pipe", "pipe"] : "inherit" });
    if (capture) {
      child.stdout.on("data", (chunk) => chunks.push(chunk));
      child.stderr.on("data", (chunk) => chunks.push(chunk));
    }
    child.once("error", reject);
    child.once("exit", (code) => code === 0
      ? resolve(Buffer.concat(chunks).toString("utf8"))
      : reject(new Error(`${command} exited with ${code}${capture ? `: ${Buffer.concat(chunks)}` : ""}`)));
  });
}

const args = parseArgs(process.argv.slice(2));
const manifestPath = path.resolve(String(args.project || "production.json"));
const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
const projectRoot = path.dirname(manifestPath);
const { duration, fps, width, height } = manifest.project || {};
if (![duration, fps, width, height].every((value) => Number(value) > 0)) {
  throw new Error("production.json needs positive duration, fps, width, and height");
}
if (manifest.approval?.status !== "approved" || !manifest.approval?.approvedVersion) {
  throw new Error("final render blocked: the exact preview version is not approved");
}
if (manifest.approval?.exportRequested !== true || manifest.approval?.exportSpecConfirmed !== true) {
  throw new Error("final render blocked: ask whether to export, explain quality options, and record explicit export-spec confirmation");
}
if (!manifest.approval?.exportSpec) {
  throw new Error("final render blocked: approval.exportSpec is missing");
}

const pixelScale = Number(args.scale || manifest.render?.pixelScale || 1);
const expectedWidth = Math.round(Number(width) * pixelScale);
const expectedHeight = Math.round(Number(height) * pixelScale);
if (manifest.render?.outputWidth && Number(manifest.render.outputWidth) !== expectedWidth) {
  throw new Error("render.outputWidth does not match project.width * pixelScale");
}
if (manifest.render?.outputHeight && Number(manifest.render.outputHeight) !== expectedHeight) {
  throw new Error("render.outputHeight does not match project.height * pixelScale");
}

const url = String(args.url || "http://127.0.0.1:4173/?capture=1");
const outputPath = path.resolve(String(args.output || "output.mp4"));
const exportSpec = manifest.approval.exportSpec;
if (Number(exportSpec.width) !== expectedWidth || Number(exportSpec.height) !== expectedHeight) {
  throw new Error("confirmed export dimensions do not match the render target");
}
if (Number(exportSpec.fps) !== Number(fps)) throw new Error("confirmed export FPS does not match project.fps");
if (String(exportSpec.format).toLowerCase() !== "mp4") throw new Error("this renderer currently requires a confirmed MP4 export");
if (String(exportSpec.videoCodec).toLowerCase() !== "h264" || String(exportSpec.audioCodec).toLowerCase() !== "aac") {
  throw new Error("this renderer currently requires confirmed H.264 video and AAC audio");
}
if (path.basename(outputPath) !== String(exportSpec.filename)) {
  throw new Error("output filename does not match the user-confirmed export filename");
}
if (await exists(outputPath)) throw new Error(`refusing to overwrite existing output: ${outputPath}`);
const version = String(manifest.approval.approvedVersion).replace(/[^a-zA-Z0-9_-]+/g, "-");
const framesDir = path.resolve(String(args["frames-dir"] || `frames-${version}`));
if (await exists(framesDir)) throw new Error(`refusing to reuse an existing frame directory: ${framesDir}`);
await mkdir(framesDir, { recursive: true });

let chromium;
const require = createRequire(import.meta.url);
try { ({ chromium } = require("playwright")); }
catch { throw new Error("playwright is required: install it in the project before rendering"); }

const launchOptions = {
  headless: true,
  args: [
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-renderer-backgrounding",
    "--run-all-compositor-stages-before-draw",
    "--disable-features=CalculateNativeWinOcclusion",
  ],
};
if (args.chrome) launchOptions.executablePath = path.resolve(String(args.chrome));
const browser = await chromium.launch(launchOptions);
const page = await browser.newPage({
  viewport: { width: Number(width), height: Number(height) },
  deviceScaleFactor: pixelScale,
});
await page.goto(url, { waitUntil: "load" });
await page.evaluate(async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map((image) => image.complete
    ? Promise.resolve()
    : new Promise((resolve) => {
        image.addEventListener("load", resolve, { once: true });
        image.addEventListener("error", resolve, { once: true });
      })));
});

const hook = String(args.hook || "__AE_VIDEO__");
const hookExists = await page.evaluate((name) => Boolean(window[name]?.render), hook);
if (!hookExists) throw new Error(`window.${hook}.render(t) was not found`);
const settleFrames = Math.max(2, Number(args["settle-frames"] || 2));
const maxAttempts = Math.max(2, Number(args["max-attempts"] || 6));
const quality = Number(args.quality || 94);

async function settle() {
  await page.evaluate(async (count) => {
    void document.documentElement.getBoundingClientRect();
    for (let index = 0; index < count; index += 1) {
      await new Promise((resolve) => requestAnimationFrame(resolve));
    }
    void document.body.offsetHeight;
  }, settleFrames);
}

async function stableScreenshot(time) {
  let previous = null;
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    await page.evaluate(({ name, time }) => window[name].render(time), { name: hook, time });
    await settle();
    const candidate = await page.screenshot({ type: "jpeg", quality, animations: "disabled" });
    if (previous && Buffer.compare(previous, candidate) === 0) return candidate;
    previous = candidate;
  }
  throw new Error(`frame at ${time.toFixed(6)}s did not reach compositor stability after ${maxAttempts} attempts`);
}

try {
  const totalFrames = Math.round(Number(duration) * Number(fps));
  for (let frame = 0; frame < totalFrames; frame += 1) {
    const buffer = await stableScreenshot(frame / Number(fps));
    await writeFile(path.join(framesDir, `${String(frame).padStart(6, "0")}.jpg`), buffer);
    if (frame % Math.max(1, Math.round(Number(fps) * 2)) === 0) {
      process.stdout.write(`rendered ${frame}/${totalFrames} stable frames\n`);
    }
  }
} finally {
  await browser.close();
}

const audioPath = path.resolve(projectRoot, String(args.audio || manifest.audio?.path || ""));
if (!(await exists(audioPath))) throw new Error(`audio file not found: ${audioPath}`);
await run("ffmpeg", [
  "-hide_banner", "-y", "-framerate", String(fps),
  "-i", path.join(framesDir, "%06d.jpg"), "-i", audioPath,
  "-map", "0:v:0", "-map", "1:a:0", "-vf", "scale=in_range=full:out_range=tv,format=yuv420p",
  "-c:v", "libx264", "-preset", String(args.preset || "faster"), "-crf", String(args.crf || 18),
  "-profile:v", "high", "-threads", String(args.threads || 4), "-tag:v", "avc1", "-r", String(fps),
  "-c:a", "aac", "-b:a", String(args["audio-bitrate"] || "320k"), "-ar", "48000", "-ac", "2",
  "-t", String(duration), "-movflags", "+faststart", outputPath,
]);

const probe = JSON.parse(await run("ffprobe", [
  "-v", "error", "-show_entries", "format=duration,size:stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels",
  "-of", "json", outputPath,
], true));
const video = probe.streams?.find((stream) => stream.codec_type === "video");
if (!video || Number(video.width) !== expectedWidth || Number(video.height) !== expectedHeight) {
  throw new Error(`encoded dimensions do not match expected ${expectedWidth}x${expectedHeight}`);
}
await run("ffmpeg", ["-v", "error", "-i", outputPath, "-f", "null", "-"]);
console.log(JSON.stringify({ complete: outputPath, expectedWidth, expectedHeight, fps, probe }, null, 2));
