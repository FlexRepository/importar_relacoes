import os
import pandas as pd
import pyperclip
import time
from playwright.sync_api import Playwright, sync_playwright

# Defina o caminho do arquivo CSV
caminho_arquivo = r"C:\Users\Vinicius Garcia\importar relacoes PYTHON\importar_relacoes\relacoes.csv"

# Verificar se o arquivo existe
if not os.path.exists(caminho_arquivo):
    raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

print(f"Usando o arquivo CSV em: {caminho_arquivo}")

# Verificar se o arquivo está vazio
if os.path.getsize(caminho_arquivo) == 0:
    raise ValueError("O arquivo está vazio")

# Leitura CSV com pandas
try:
    df = pd.read_csv(caminho_arquivo, header=None, encoding='utf-8')
except pd.errors.EmptyDataError:
    raise ValueError("O arquivo CSV está vazio ou mal formatado")
except Exception as e:
    raise ValueError(f"Erro ao ler o arquivo: {e}")

# Mudando indexação para iniciar em 1
df.index = range(1, len(df) + 1)

# Variáveis globais
inicio = True
linhasCopiadas = 0 
totalLinhas = max(1, len(df)) #numero de linhas total a ser preenchido
clipboard_content = ""

def copiaLinhas(intervalo):
    global linhasCopiadas
    global clipboard_content

    indiceInicial = linhasCopiadas
    indiceFinal = linhasCopiadas + intervalo

    df.iloc[indiceInicial:indiceFinal].to_clipboard(index=False, header=False, sep=",")

    clipboard_content = pyperclip.paste()
    linhasCopiadas += intervalo

def run(playwright: Playwright) -> None:
    global inicio
    global linhasCopiadas

    if inicio:
        print(f"O CSV tem um total de {totalLinhas} linhas")
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://www.portalselosmecanicos.com.br/")
        page.get_by_placeholder("email").fill("engenharia@flexaseal.com.br")
        page.get_by_placeholder("Senha").fill("12345")
        page.get_by_role("button", name="Login").click()
        inicio = False

    while linhasCopiadas <= totalLinhas:
        page.get_by_role("button", name="Selos").click()
        page.get_by_role("link", name="Importar relação").click()
        copiaLinhas(100)
        page.get_by_placeholder("nome fabricante, nome modelo").fill(clipboard_content)
        page.get_by_role("button", name="Importar").click()
        time.sleep(3)

    print(f"Foram preenchidas {linhasCopiadas} linhas")

with sync_playwright() as playwright:
    run(playwright)
