import re, time
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://www.portalselosmecanicos.com.br/")
    page.get_by_placeholder("email").click()
    page.get_by_placeholder("email").fill("rafaelguida.panicali@gmail.com")
    page.get_by_placeholder("Senha").click()
    page.get_by_placeholder("Senha").fill("z9e6y000")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="RS").click()
    page.get_by_role("link", name="Registrar troca").click()
    page.get_by_placeholder("Digite o nome para filtrar").click()
    page.get_by_placeholder("Digite o nome para filtrar").fill("teste")
    time.sleep(2)
    page.get_by_role("row", name="CARAMURU | SORRISO (Teste").get_by_role("link").click()
    time.sleep(2)
    page.get_by_role("row", name="BIODIESEL Levantamentos").get_by_role("link").click()
    
    time.sleep(20)

    # ---------------------
    # context.close()
    # browser.close()


with sync_playwright() as playwright:
    run(playwright)
