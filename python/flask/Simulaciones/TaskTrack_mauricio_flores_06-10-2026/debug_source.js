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
  await page.waitForLoadState("networkidle");

  // Get page content
  const content = await page.content();
  // Search for error messages
  const errors = content.match(/errores[^<]*<[^>]*>/gi) || [];
  console.log("Error messages found:", errors.length);
  errors.forEach((e, i) => console.log(`Error ${i+1}:`, e.substring(0, 100)));

  // Search for success messages
  const success = content.match(/exito[^<]*<[^>]*>/gi) || [];
  console.log("Success messages found:", success.length);
  success.forEach((s, i) => console.log(`Success ${i+1}:`, s.substring(0, 100)));

  // Check form inputs still have values
  const nombre = formReg.locator("input[name=nombre]").inputValue();
  console.log("Nombre input value:", nombre);

  await browser.close();
})().catch(async (error) => { console.error(error); process.exit(1); });