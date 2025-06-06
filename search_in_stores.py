import os
import time
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdf_utils import criar_pdf_reportlab
from PIL import Image as PILImage
import io

def buscar_produtos(search):
    # Configurações do navegador
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    list_products = []
    
    browser = webdriver.Chrome(options=options)
    
    def search_Itens(element, selector, attribute="text", default="N/A"):
        try:
            elem = element.find_element(By.CSS_SELECTOR, selector)
            return elem.get_attribute(attribute) if attribute != "text" else elem.text
        except:
            return default

    try:
        print(f"🔍 Iniciando busca por: '{search}'")
        browser.get('https://www.google.com/shopping')
        
        # Pesquisa
        search_box = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.NAME, 'q')))
        search_box.send_keys(search)
        search_box.submit()
        time.sleep(random.uniform(2, 4))

        print("🔄 Rolando a página para carregar mais resultados...")
        for i in range(1):
          try:
              browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
              wait_time = random.uniform(3.0, 4.0)  # Entre 1.5 e 3 segundos
              time.sleep(wait_time)
          except Exception as e:
              print(f"\n⚠️ Erro na rolagem {i+1}: {str(e)}")
              continue
        
        # Coleta os itens
        itens = WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.YBo8bb, li.sh-dgr__grid-result')))
        print(f"✅ Encontrados {len(itens)} produtos")

        product_id = 1  # Contador para IDs dos produtos válidos
        for idx, item in enumerate(itens, 1):
            try:
              # Verifica se o item contém uma imagem
              img_url = search_Itens(item, 'img.FsH7wb, img.sh-div__image', 'src')
              if img_url and img_url != 'N/A' and img_url.startswith(('http://', 'https://')):
                try:
                    # Primeiro tenta pegar o link com o seletor específico do Google Shopping
                    link_element = item.find_element(By.CSS_SELECTOR, 'a[data-impdclcc="1"]')
                    link_loja = link_element.get_attribute('href')
                except:
                    try:
                        # Se não encontrar, tenta pegar o link dentro do elemento com class específica
                        link_element = item.find_element(By.CSS_SELECTOR, 'a.plantl.pla-unit-title-link')
                        link_loja = link_element.get_attribute('href')
                    except:
                        try:
                            # Última tentativa com um seletor mais genérico
                            link_element = item.find_element(By.CSS_SELECTOR, 'a.shntl[href]')
                            link_loja = link_element.get_attribute('href')
                        except:
                            link_loja = "Link não disponível"
                    
                # Baixa a imagem
                response = requests.get(img_url, stream=True, timeout=10)
                response.raise_for_status()
                img_data = io.BytesIO(response.content)
                
                # Redimensiona (opcional)
                img = PILImage.open(img_data)
                img.thumbnail((200, 200))  # Tamanho máximo
                img_processed = io.BytesIO()
                img.save(img_processed, format='PNG')
                img_processed.seek(0)
                
                product = {
                  'id': product_id,
                  'nome': search_Itens(item, 'div.gkQHve, .sh-np__product-title, .pymv4e'),
                  'preco_atual': search_Itens(item, 'span.lmQWe, .T14wmb, .e10twf'),
                  'preco_anterior': search_Itens(item, 'div.DoCHT, .OzqkAH'),
                  'loja': search_Itens(item, 'span.WJMUdc, .E5ocAb, .zPEcBd'),
                  'img_data': img_processed,
                  'link_loja': link_loja
                }
                
                list_products.append(product)
                print(f"✅ Item {product_id} adicionado: {product['nome']} - {product['preco_atual']} - {product['loja']} - {link_loja}")
                product_id += 1
                time.sleep(random.uniform(1.0, 3.0))  # Delay aleatório entre produtos
                continue

            except Exception as e:
                print(f"⚠️ Erro ao processar item {idx}: {str(e)}")
                continue

    except Exception as e:
        print(f"❌ Erro na busca: {str(e)}")
    finally:
        browser.quit()
        print("🛑 Navegador fechado")
    
    return list_products

# Exemplo de uso:
if __name__ == "__main__":
    search_text = "Manfinity Homme Casaco com Capuz Forrado Térmico"
    list_products = buscar_produtos(search_text)
    
    print("Gerando PDFs...")
    
    # Usando reportlab
    criar_pdf_reportlab("lista_produtos_reportlab.pdf", list_products)

    print("PDF criado com sucesso!")