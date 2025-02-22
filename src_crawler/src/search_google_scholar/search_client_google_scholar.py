from dataclasses import dataclass
from enum import Enum
import re

from scholarly import scholarly, ProxyGenerator

pg = ProxyGenerator()
pg.FreeProxies()
scholarly.use_proxy(pg)

###############################################################
# Dataclasses for Google scholar search query and parameters
###############################################################
class GooglescholarParams(Enum):
    """Enum for Google scholar URL"""

    AUTHOR = "author"
    PAPER = "paper"

#####################
# Search client
#####################
class GooglescholarSearchClient:
    def __init__(self, query_value: str, query_type: str):
        """Initialize Google scholar search client

        Args:
            query_value (str): Query value
            query_type (str): Query type
        """
        assert query_type in [GooglescholarParams.AUTHOR.value, GooglescholarParams.PAPER.value], "Invalid query type"
        self.query_value = query_value
        self.query_type = query_type
        
        
    def fetch_citation(self):
        """Fetch citation from Google scholar search results

        Returns:
            str: Citation value
        """
        
        if self.query_type == GooglescholarParams.AUTHOR.value:
            search_result = scholarly.search_author(self.query_value)
            
        elif self.query_type == GooglescholarParams.PAPER.value:
            search_result = scholarly.search_pubs(self.query_value)
            
        else:
            raise ValueError("Invalid query type")
        
        
        return [r["citedby"] for r in search_result][0]
        
