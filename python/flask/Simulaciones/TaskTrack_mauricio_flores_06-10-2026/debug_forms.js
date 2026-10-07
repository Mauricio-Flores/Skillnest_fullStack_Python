const { chromium } = require("playwright");
const base = "http://127.0.0.1:5000";
const output = "C:/Users/GAMER/Documents/GitHub/Skillnest_fullStack_Python/python/flask/Simulaciones/TaskTrack_mauricio_flores_06-10-2026/resources/Capturas";

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1050 }, deviceScaleFactor: 1 });
  await page.goto(`${base}/`, { waitUntil: "networkidle" });
  const forms = await page.$$("form");
  console.log("Number of forms:", forms.length);
  for (let i = 0; i < forms.length; i++) {
    const action = await forms[i].getAttribute("action");
    console.log(`Form ${i}:`, action);
  }
  await browser.close();
})().catch(async (error) => { console.error(error); process.exit(1); });