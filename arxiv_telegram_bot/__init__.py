from decouple import config
import requests
from bs4 import BeautifulSoup
import lxml

__version__ = "0.1.0"
response = requests.get("https://export.arxiv.org/api/query?search_query=cat:cs.CV+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.AI+OR+cat:cs.NE+OR+cat:cs.RO")
xml_data = BeautifulSoup(response.text, "lxml")
print(xml_data.find_all("entry")[0])
