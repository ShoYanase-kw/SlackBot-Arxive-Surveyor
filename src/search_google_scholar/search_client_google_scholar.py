from dataclasses import dataclass
from enum import Enum
import re

from bs4 import BeautifulSoup
import urllib.request
    
class GooglescholarURL(Enum):
    """Enum for Google scholar URL
    """    
    AUTHOR = "https://scholar.google.com/scholar?hl=en&q=author%3A"
    PAPER = "https://scholar.google.com/scholar_lookup?hl=en&arxiv_id="
    
    
class GooglescholarElementSelector(Enum):
    """Enum for Google scholar element ID
    """
    
    AUTHOR = "#gs_res_ccl_mid > div:nth-child(1) > table > tr > td:nth-child(2) > div:nth-child(4)"
    PAPER = "#gs_res_ccl_mid > div > div.gs_ri > div.gs_fl.gs_flb > a:nth-child(3)"
    
    
@dataclass
class GooglescholarLookUpQuery:
    """Dataclass for Google scholar search query
    """    
    value: str
    base_url: str
    
    def __str__(self):
        self.value = self.value.replace(" ", "+")
        return f"{self.base_url}{self.value}"
    
    
class GooglescholarSearchClient:
    def __init__(self, query_value: str, query_type: str):
        """Initialize Google scholar search client

        Args:
            search_query (GooglescholarLookUpQuery): Google scholar search query
        """        
        assert query_type.upper() in GooglescholarURL.__members__, f"Invalid query type: {query_type}. Valid query types: {GooglescholarURL.__members__}"
        assert query_type.upper() in GooglescholarElementSelector.__members__, f"Invalid query type: {query_type}. Valid query types: {GooglescholarElementSelector.__members__}"
        
        query_type = query_type.upper()
        self.search_url = GooglescholarLookUpQuery(query_value, GooglescholarURL[query_type].value)
        self.element_selector = GooglescholarElementSelector[query_type].value
        
    
    def fetch_soup_by_url(self):
        """Search Google scholar by URL

        Returns:
            dict: Google scholar search results
        """        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        url = str(self.search_url)
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            return soup
    
    def fetch_element(self):
        """Fetch element from Google scholar search results
        """    
        soup = self.fetch_soup_by_url()
        element = soup.select(self.element_selector)
        assert element, f"Element not found for selector: {self.element_selector}"
        return str(element[0])
    
    @staticmethod
    def get_value_citation(element: str):
        """Get citation value from element

        Args:
            element (str): Element

        Returns:
            str: Citation value
        """        
        str_cite = re.search(r'Cited by \d+',element).group()
        value_cite = re.search(r'\d+',str_cite).group()
        assert value_cite, f"Invalid citation element: {element}"
        return int(value_cite)
    
    def fetch_citation(self):
        """Fetch citation from Google scholar search results

        Returns:
            str: Citation value
        """        
        element = self.fetch_element()
        return self.get_value_citation(element)