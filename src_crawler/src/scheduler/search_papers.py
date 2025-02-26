from concurrent.futures import ThreadPoolExecutor
import os

from tqdm import tqdm
from loguru import logger

import pandas as pd

from src.search_semantic_scholar.search_client_semantic_scholar import S2scholarSearchClient
from src.search_arxiv.search_client_arxiv import ArxivSearchClient
from src.params.load_from_yml import load_from_yml


class DateRangeSearchClient:
    """Date range search client
    """    
    def __init__(self):
        self.yaml_app = load_from_yml("../doc/params/app.yml")
        yaml_arxiv = self.yaml_app["filepath"]["search_arxiv"]
        self.search_client_arxiv = ArxivSearchClient.from_yaml(yaml_arxiv)
        self.threading_enabled =  self.yaml_app["threading"]["enabled"]
        self.threading_num_workers = self.yaml_app["threading"]["num_workers"]
        self.search_results = []

    @staticmethod
    def fetch_citation(search_result_arxiv: dict):
        """Fetch citation from Google Scholar

        Args:
            search_result_arxiv (dict): search result from Arxiv

        Returns:
            dict: search result from Arxiv with citation
        """        
        # get author and paper id
        paper_title = search_result_arxiv["title"]

        # fetch citation
        search_client_paper = S2scholarSearchClient(
            query_value=paper_title, query_type="paper"
        )
        paper_citation_count, author_citation_count = search_client_paper.fetch_paper_with_citation()
        
        search_result_arxiv = search_result_arxiv | {
            "citation_author": author_citation_count,
            "citation_paper": paper_citation_count,
        }
        logger.debug(f"search_result_arxiv: {search_result_arxiv}")
        
        return search_result_arxiv

    def thread_search_wrapper(self, result):
        """Thread search wrapper

        Args:
            result (dict): search result

        Returns:
            dict: search result with citation
        """        
        _result = self.fetch_citation(result)
        print(_result)
        if self.pbar:
            self.pbar.update(1)
        
        return _result

    def search_weekly(self):
        """Search weekly date range
        """        
        # fetch weekly search results from arxiv
        results = self.search_client_arxiv.search_weekly()
        
        # self.pbar = tqdm(total=len(results))
        # if self.threading_enabled:
        #     with ThreadPoolExecutor(max_workers=self.threading_num_workers) as executor:
        #         self.search_results = list(executor.map(self.thread_search_wrapper, results))
        # else:
            # for result in results:
            #     self.search_results.append(self.thread_search_wrapper(result))
        for result in tqdm(results):
            self.search_results.append(self.fetch_citation(result))
        # self.pbar.close()
        return self.search_results
    
    def search_results_to_csv(self, path: str):
        """Save search results to CSV

        Args:
            path (str): path to save CSV
        """        
        results_df = pd.DataFrame(self.search_results)
        # save search results to CSV
        results_df.to_csv(path, index=False)