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
  await Promise.all([page.waitForURL("**/dashboard"), formReg.getByRole("button", { name: "Registrarse" }).click()]);
  await page.waitForLoadState("networkidle");

  // Listar links
  const links = await page.$$("a");
  console.log("Number of links:", links.length);
  for (let i = 0; i < links.length; i++) {
    const text = await links[i].innerText();
    const href = await links[i].getAttribute("href");
    if (text.trim()) {
      console.log(`Link ${i}: text="${text}", href="${href}"`);
    }
  }

  await browser.close();
})().catch(async (error) => { console.error(error); process.exit(1); });