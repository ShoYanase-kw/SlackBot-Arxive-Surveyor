from dataclasses import dataclass
from enum import Enum

import re
import json

from typing import Optional

from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, RetryError
from loguru import logger
from urllib import request, parse, error as urllib_error


###############################################################
# Dataclasses for S2 scholar search query and parameters
###############################################################
class S2scholarURL(Enum):
    """Enum for S2 scholar URL"""

    AUTHOR = "https://api.semanticscholar.org/graph/v1/author/search?query="
    PAPER = "https://api.semanticscholar.org/graph/v1/paper/search/match?fields=title,authors,citations.title,citations.abstract&query="
    AUTHOR_BATCH = "https://api.semanticscholar.org/graph/v1/author/batch?fields=url,name,citationCount"


@dataclass
class S2scholarLookUpQuery:
    """Dataclass for S2 scholar search query"""

    value: str
    base_url: str

    def __str__(self):
        
        self.value = parse.quote(self.value, safe="")
        return f"{self.base_url}{self.value}"


#####################
# Search client
#####################
class S2scholarSearchClient:
    def __init__(self, query_value: str, query_type: str):
        """Initialize S2 scholar search client

        Args:
            search_query (S2scholarLookUpQuery): S2 scholar search query
        """
        assert (
            query_type.upper() in S2scholarURL.__members__
        ), f"Invalid query type: {query_type}. Valid query types: {S2scholarURL.__members__}"

        query_type = query_type.upper()
        
        self.search_url = S2scholarLookUpQuery(
            query_value, S2scholarURL[query_type].value
        )

    @retry(stop=stop_after_attempt(7), wait=wait_fixed(5), retry=retry_if_exception_type((urllib_error.HTTPError)))
    def fetch_by_url(
        self, url: Optional[str]=None, data=None, headers: dict=None
    ):
        """Search S2 scholar by URL

        Returns:
            dict: S2 scholar search results
        """
        if not headers or "User-Agent" not in headers:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
            }
        if not url:
            url = str(self.search_url)
        
        logger.debug(f"requesting url: {url}")
        logger.debug(f"headers: {headers}")
        logger.debug(f"data: {data}")
        
        if not data:
            _request = request.Request(url, headers=headers)
        else:
            _request = request.Request(url, headers=headers, data=data)

        with request.urlopen(_request) as response:
            res = response.read()
            return json.loads(res)

    def fetch_paper_with_citation(self):
        """Fetch citation from S2 scholar search results

        Returns:
            str: Citation value
        """
        if self.search_url.base_url != S2scholarURL.PAPER.value:
            raise ValueError("Invalid query type")

        try:
            search_result = self.fetch_by_url()
        except RetryError as e:
            logger.error(f"Failed to fetch citation: {e}")
            return 0,0
        if not search_result:
            return 0,0
        
        if "citations" in search_result:
            paper_citation_count = len(search_result["citations"])
        else:
            paper_citation_count = 0

        logger.debug(f"search_result: {search_result}")
        
        
        result_data = search_result["data"][0]
        result_authors = result_data["authors"]
        author_ids = [author["authorId"] for author in result_authors]
        request_json = {"ids": author_ids}
        request_json = json.dumps(request_json).encode('utf-8')
        
        url = S2scholarURL.AUTHOR_BATCH.value

        response_author = self.fetch_by_url(url, headers=None, data=request_json)

        logger.debug(f"response_author: {response_author}")
        if isinstance(response_author, list) and len(response_author) > 0:
            author_citation_count = sum([d["citationCount"] for d in response_author if d and "citationCount" in d])
            self.search_url.value = parse.unquote(self.search_url.value)
            logger.info(f"Citation Count of Paper \"{self.search_url.value}\": {author_citation_count}")
        else:
            author_citation_count = 0
            
        return paper_citation_count, author_citation_count
