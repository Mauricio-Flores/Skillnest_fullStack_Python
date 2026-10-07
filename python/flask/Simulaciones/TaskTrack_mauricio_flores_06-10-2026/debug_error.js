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
  const [newPage] = await Promise.all([
    page.waitForEvent("navigate"),
    formReg.getByRole("button", { name: "Registrarse" }).click()
  ]);
  const registerPage = newPage || page;
  await registerPage.waitForLoadState("networkidle");

  // Get page content
  const content = await registerPage.content();
  // Search for error messages
  const errorStart = content.indexOf('class="errores"');
  if (errorStart >= 0) {
    const errorSection = content.substring(errorStart);
    const errorEnd = errorSection.indexOf("</div>");
    if (errorEnd >= 0) {
      console.log("Error section:", errorSection.substring(0, errorEnd + 6));
    }
  }

  // Search for success messages
  const success = content.match(/exito[^<]*<[^>]*>/gi) || [];
  console.log("Success messages found:", success.length);
  success.forEach((s, i) => console.log(`Success ${i+1}:`, s.substring(0, 100)));

  await browser.close();
})().catch(async (error) => { console.error(error); process.exit(1); });