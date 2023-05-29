# Projeto de Web Scraping
    Este projeto é um exemplo de web scraping utilizando Python para extrair dados de produtos de dois sites de equipamentos musicais: Musicalle e Megasom. O objetivo é coletar informações sobre guitarras em ambos os sites e  salvar os dados como arquivos CSV para análises posteriores.

## Tecnologias Utilizadas
    Python
    Bibliotecas Python:
    BeautifulSoup: biblioteca para análise e extração de dados HTML/XML.
    httpx: cliente HTTP assíncrono para realizar requisições web.
    csv: biblioteca para escrever dados em formato CSV.
    Funcionalidades
    Coleta de URLs de produtos: a função get_product_urls é responsável por obter as URLs dos produtos de uma página específica de cada site.
    Coleta de dados do produto: a função get_product_data é responsável por extrair as informações relevantes de um produto, como título, preço e imagem.
    Coleta de dados do site Musicalle: a função get_musicale_product_data realiza a coleta de dados específicos do site Musicalle, utilizando as funções mencionadas acima.
    Coleta de dados do site Megasom: a função get_megasom_product_data realiza a coleta de dados específicos do site Megasom, utilizando as mesmas funções mencionadas acima.
    Armazenamento em arquivo CSV: a função save_csv é responsável por salvar os dados coletados em um arquivo CSV, utilizando a biblioteca csv.
