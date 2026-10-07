const { chromium } = require("playwright");
const base = "http://127.0.0.1:5000";
const output = "C:/Users/GAMER/Documents/GitHub/Skillnest_fullStack_Python/python/flask/Simulaciones/TaskTrack_mauricio_flores_06-10-2026/resources/Capturas";

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1050 }, deviceScaleFactor: 1 });

  await page.goto(`${base}/`, { waitUntil: "networkidle" });
  const url1 = page.url();
  console.log("Initial URL:", url1);

  // Registro
  const formReg = page.locator("form").nth(0);
  await formReg.locator("input[name=nombre]").fill("Mauricio");
  await formReg.locator("input[name=apellido]").fill("Test");
  await formReg.locator("input[name=email]").fill("mauricio.tasktrack.20261007@example.com");
  await formReg.locator("input[name=password]").fill("TaskTrack2026!");
  await formReg.locator("input[name=confirmar_password]").fill("TaskTrack2026!");
  await formReg.getByRole("button", { name: "Registrarse" }).click();
  await page.waitForLoadState("networkidle");
  const url2 = page.url();
  console.log("After register URL:", url2);
  const title = page.title();
  console.log("Title:", title);

  // Check if logged in by looking for dashboard elements
  const h1 = page.locator("h1");
  if (await h1.count() > 0) {
    console.log("H1 text:", await h1.first().innerText());
  }

  await browser.close();
})().catch(async (error) => { console.error(error); process.exit(1); });