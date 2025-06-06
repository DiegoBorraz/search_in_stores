# Consultas de Produtos no Google Shopping
Este projeto realiza buscas de produtos no Google Shopping utilizando Selenium e gera um relatório em PDF com os resultados encontrados.




## 🎯 Funcionalidades
- Busca automatizada de produtos no Google Shopping

- Extração de informações como nome, preço, loja e imagem

- Geração de relatório em PDF organizado com os produtos encontrados

- Tratamento de erros e delays aleatórios para evitar bloqueios

## 🧰 Arquivos
- **search_in_stores.py**: Script principal que realiza a busca e coleta dos dados

- **pdf_utils.py**: Módulo auxiliar para geração do PDF usando ReportLab

## 📦 Requisitos
- Python 3.x

- Bibliotecas Python:

- selenium

- requests

- pillow (PIL)

- reportlab

- webdriver-manager (opcional)

## ⚙ Instale as dependências com:


``bash
 pip install selenium requests pillow reportlab
``

Como usar

Execute o script principal:


``
 bash
 python3 search_in_stores.py
``

Por padrão, o script busca por "Manfinity Homme Casaco com Capuz Forrado Térmico"

Para buscar outro produto, modifique a variável search_text no final do arquivo

## 🚀 Saída

**O script gera um arquivo PDF chamado lista_produtos_reportlab.pdf contendo:**

- Imagem do produto

- Nome do produto

- Preço atual

- Loja que vende o produto

## 📖 Detalhes técnicos

**search_in_stores.py**

- Utiliza Selenium WebDriver para automatizar a navegação

- Implementa delays aleatórios entre ações para parecer mais humano

- Extrai dados usando seletores CSS compatíveis com a estrutura do Google Shopping

- Baixa e processa imagens dos produtos

- Organiza os dados em um dicionário estruturado

**pdf_utils.py**

- Cria PDFs usando ReportLab

- Organiza os produtos em um layout limpo com imagem e informações

- Aplica estilos consistentes ao documento

- Trata erros durante a geração do PDF

## 🛠 Personalização
- Modifique search_text para buscar outros produtos

- Ajuste os seletores CSS em search_Itens() se a estrutura do Google Shopping mudar

- Edite criar_pdf_reportlab() para alterar o layout do PDF

##Limitações##

- Dependente da estrutura atual do Google Shopping

- Pode ser bloqueado se muitas requisições forem feitas em curto período

- Requer ChromeDriver instalado ou no PATH

## 🤝 Autor
[Diego Borraz de Avila] - [https://github.com/DiegoBorraz]
