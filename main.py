from bs4 import BeautifulSoup
from time import perf_counter
import asyncio
import httpx
import csv


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

def save_csv(results: list[dict], store: str):
    """
    Saves a list of dictionaries to a CSV file.

    Args:
        results (list[dict]): The list of dictionaries to be saved as CSV.
        store (str): The name of the store.

    Returns:
        None
    """
    keys = results[0].keys()

    with open(f'{store}_products.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

async def get_product_urls(session:httpx.AsyncClient, url:str, page_number:int, products_selector:str):
    """
    Retrieves the URLs of the products from a given page.

    Args:
        session (httpx.AsyncClient): The HTTP session.
        url (str): The base URL.
        page_number (int): The page number to retrieve.
        products_selector (str): CSS selector to select the product elements.

    Returns:
        list: A list of product URLs.
    """
    response = await session.get(f"{url}{page_number}", timeout=30)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.select(products_selector)
    product_urls = []
    for product in products:
        product_urls.append(product.find("a").attrs.get("href"))
    return product_urls


async def get_product_data(session:httpx.AsyncClient, product_url:str, title_selector:str, price_selector:str, product_img_selector:str):
    """
    Retrieves data for a given product URL.

    Args:
        session (httpx.AsyncClient): The HTTP session.
        product_url (str): The URL of the product.
        title_selector (str): CSS selector to select the title element.
        price_selector (str): CSS selector to select the price element.
        product_img_selector (str): CSS selector to select the product image element.

    Returns:
        dict: A dictionary containing the product data.
    """
    response = await session.get(product_url, timeout=30)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    title_element = soup.select_one(title_selector)
    title = title_element.get_text(strip=True) if title_element else None

    price_element = soup.select_one(price_selector)
    price = price_element.get_text(strip=True)\
        .replace(".", "")\
        .replace(",", ".")\
        .replace("R$", "")\
        .replace(" ", "") if price_element else None

    try:
        img_element = soup.select_one(product_img_selector)
        img = img_element.attrs["src"] if img_element else None
    except AttributeError:
        img = None
    except:
        img = img_element.attrs["data-src"] if img_element else None

    product_data = {
        "product_link": product_url,
        "product_title": title,
        "product_price": price,
        "product_img": img,
    }
    return product_data


async def get_musicale_product_data(url='https://musicalle.com.br/cordas/guitarra?page=',
                                    products_selector='div.main-products div.product-grid-item',
                                    title_selector='h1',
                                    price_selector=".product-price",
                                    product_img_selector='img#image'):
    """
    Retrieves product data from Musicalle website.

    Args:
        url (str, optional): The base URL. Defaults to 'https://musicalle.com.br/cordas/guitarra?page='.
        products_selector (str, optional): CSS selector to select the product elements. Defaults to 'div.main-products div.product-grid-item'.
        title_selector (str, optional): CSS selector to select the title element. Defaults to 'h1'.
        price_selector (str, optional): CSS selector to select the price element. Defaults to '.product-price'.
        product_img_selector (str, optional): CSS selector to select the product image element. Defaults to 'img#image'.

    Returns:
        list: A list of dictionaries containing the product data.
    """
    async with httpx.AsyncClient(follow_redirects=True, headers=headers) as session:
        page_number = 1
        product_urls = await get_product_urls(session, url, page_number, products_selector)
        dict_list = []
        while product_urls:
            tasks = []
            for product_url in product_urls:
                tasks.append(get_product_data(session, product_url, title_selector, price_selector, product_img_selector))
            product_data_list = await asyncio.gather(*tasks)
            dict_list.extend(product_data_list)
            page_number += 1
            product_urls = await get_product_urls(session, url, page_number, products_selector)
        return dict_list


async def get_megasom_product_data(url='https://www.megasom.com.br/cordas/guitarra?pg=',
                                   products_selector='.item.flex',
                                   title_selector='h1',
                                   price_selector=".preco-avista.precoAvista",
                                   product_img_selector='.zoom img'):
    """
    Retrieves product data from Megasom website.

    Args:
        url (str, optional): The base URL. Defaults to 'https://www.megasom.com.br/cordas/guitarra?pg='.
        products_selector (str, optional): CSS selector to select the product elements. Defaults to '.item.flex'.
        title_selector (str, optional): CSS selector to select the title element. Defaults to 'h1'.
        price_selector (str, optional): CSS selector to select the price element. Defaults to '.preco-avista.precoAvista'.
        product_img_selector (str, optional): CSS selector to select the product image element. Defaults to '.zoom img'.

    Returns:
        list: A list of dictionaries containing the product data.
    """
    async with httpx.AsyncClient(follow_redirects=True, headers=headers) as session:
        page_number = 1
        product_urls = await get_product_urls(session, url, page_number, products_selector)
        dict_list = []
        while product_urls:
            tasks = []
            for product_url in product_urls:
                tasks.append(get_product_data(session, product_url, title_selector, price_selector, product_img_selector))
            product_data_list = await asyncio.gather(*tasks)
            dict_list.extend(product_data_list)
            page_number += 1
            product_urls = await get_product_urls(session, url, page_number, products_selector)
        return dict_list


async def main():
    """
    Main function that retrieves product data from Musicalle and Megasom websites and saves them as CSV files.
    """
    print("Start scrapping...")
    musicale_data = await get_megasom_product_data()
    save_csv(musicale_data, "musicale")

    megasom_data = await get_megasom_product_data()
    save_csv(megasom_data, "megasom")
    print("Finished scrapping...")
    print("Total items scrapped:", len(megasom_data) + len(megasom_data))


if __name__ == "__main__":
    start = perf_counter()
    asyncio.run(main())
    stop = perf_counter()
    print("Time taken in seconds:", stop - start)
