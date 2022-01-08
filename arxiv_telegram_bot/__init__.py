from decouple import config
import requests
from bs4 import BeautifulSoup
import lxml
__version__ = "0.1.0"
response = requests.get("http://export.arxiv.org/api/query?search_query=all:electron")
xml_data = BeautifulSoup(response.text, "lxml")
print(xml_data.find_all("entry")[0])
