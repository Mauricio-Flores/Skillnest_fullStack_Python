const { chromium } = require("playwright");
const base = "http://127.0.0.1:5000";
const output = "C:/Users/GAMER/Documents/GitHub/Skillnest_fullStack_Python/python/flask/Simulaciones/TaskTrack_mauricio_flores_06-10-2026/resources/Capturas";

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1050 }, deviceScaleFactor: 1 });

  await page.goto(`${base}/`, { waitUntil: "networkidle" });

  // Registro
  const formReg = page.locator("form").nth(0);
  await formReg.locator("input[name=nombre]").fill("Mauricio");
  await formReg.locator("input[name=apellido]").fill("Test");
  await formReg.locator("input[name=email]").fill("mauricio.tasktrack.20261007@example.com");
  await formReg.locator("input[name=password]").fill("TaskTrack2026!");
  await formReg.locator("input[name=confirmar_password]").fill("TaskTrack2026!");
  await formReg.getByRole("button", { name: "Registrarse" }).click();
  await page.waitForTimeout(2000); // wait a bit
  
  const url = page.url();
  const title = await page.textContent("title");
  console.log("Page URL:", url);
  console.log("Page title:", title);

  // Show body HTML snippet
  const body = await page.locator("body").innerHTML();
  console.log("Body HTML snippet (first 500):", body.substring(0, 500));

  await browser.close();
})().catch(async (error) => { console.error(error); process.exit(1); });