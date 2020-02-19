
import time
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from functions import html_cleaner

def parse_contrataciones(base_url, fecha):
    seccion = 'tercera'
    rubro = 1711
    return parse_page(base_url, seccion, fecha, rubro)

def parse_page_item(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    title = soup.title.get_text()

    content = soup.find(id = "detalleAviso")
    body = ""

    if content != None:
        article = soup.find(id = "detalleAviso").find(id = "cuerpoDetalleAviso").findAll("p")

        for p in article:
            body = "%s%s " % (body, html_cleaner(p.get_text()))

    return body


def parse_page(url, seccion, fecha, rubro):

    scrap_url = "%s/seccion/%s/%s?rubro=%s" % (url, seccion, fecha, rubro)

    response = requests.get(scrap_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    content = soup.find(id = "avisosSeccionDiv")

    if content == None:
        return

    row = content.findAll("div", {"class": "row"})

    if row != None:
        array_content = str(row).split(',')
    else:
        array_content = None

    url_to_parse = list()

    for item_content in array_content:
        if(item_content.find("href")!=-1):
            link = BeautifulSoup(item_content, "lxml").find_all('a', href=True)
            href = "%s%s" % (url, link[0].get('href'))
            url_to_parse.append(href)

    response = {}

    for u in url_to_parse:
        if(u.find("anexos")==-1):
            body = parse_page_item(u)
            response[u] = body
            time.sleep(2)

    return response
