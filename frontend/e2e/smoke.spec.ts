import { expect, test } from "@playwright/test";

test("fluxo completo: cadastro → caderno → editar → recarregar", async ({ page }) => {
  const email = `e2e-${Date.now()}@example.com`;
  const password = "senha1234";
  const notebookName = `Caderno E2E ${Date.now()}`;
  const text = "anotação E2E automática";

  await page.goto("/register");

  await page.getByPlaceholder("E-mail").fill(email);
  await page.getByPlaceholder("Senha (mín. 8 caracteres)").fill(password);
  await page.getByRole("button", { name: "Cadastrar" }).click();

  await expect(page.getByPlaceholder("Nome do caderno")).toBeVisible();

  await page.getByPlaceholder("Nome do caderno").fill(notebookName);
  await page.getByRole("button", { name: "Criar" }).click();

  await page.locator(".notebook-open").click();

  await expect(page.locator(".ProseMirror")).toBeVisible();
  await page.locator(".ProseMirror").click();
  await page.keyboard.type(text);

  await expect(page.locator(".save-status")).toHaveText("Salvo");

  await page.reload();
  await expect(page.locator(".ProseMirror")).toContainText(text);
});
