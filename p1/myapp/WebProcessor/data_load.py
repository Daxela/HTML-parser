from bs4 import BeautifulSoup
import requests as req


def load_html(html_doc: str) -> BeautifulSoup:
    resp = req.get(html_doc)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup
