import arxiv
from dataclasses import dataclass

from src.params.load_from_yml import load_from_yml

@dataclass
class ArxivSearchQuery:
    """Dataclass for Arxiv search query
    """    
    ti: str
    au: str
    abs: str
    cat: str
    all: str
    
    submittedDate_from: str = ""
    submittedDate_to: str = ""
    
    def __str__(self):
        # concatenate key:value pairs for query
        query = " AND ".join([f"{key}:{value}" for key, value in self.__dict__.items() if value and key != "submittedDate_from" and key != "submittedDate_to"])
        # concatenate date range for query
        date_range = f"submittedDate:[{self.submittedDate_from} TO {self.submittedDate_to}]"
        if self.submittedDate_from and self.submittedDate_to:
            query = f"{query} AND {date_range}"
        return query

@dataclass
class ArxivSearchParameters:
    """Dataclass for Arxiv search parameters
    """    
    query: str
    max_results: int
    max_chunk_results: int
    sort_by: str
    sort_order: str
    id_list: list
    

class ArxivSearchClient:
    def __init__(self, search_params: ArxivSearchParameters, multi_threading_enabled: bool = False, multi_threading_chunk_size: int = 10, multi_threading_num_workers: int = 16):
        """Initialize Arxiv search client

        Args:
            search_params (ArxivSearchParameters): Arxiv search parameters
            multi_threading_enabled (bool, optional): boolean flag for multi-threading. Defaults to False.
            multi_threading_chunk_size (int, optional): chunk size for multi-threading. Defaults to 10.
            multi_threading_num_workers (int, optional): number of workers for multi-threading. Defaults to 16.
        """        
        self.multi_threading_enabled = multi_threading_enabled
        self.multi_threading_chunk_size = multi_threading_chunk_size
        self.multi_threading_num_workers = multi_threading_num_workers
        self.search_results = []
        
        self.search_params = search_params
        
    @classmethod
    def from_yaml(cls, path: str):
        """Create Arxiv search client from YAML

        Args:
            path (str): Path to YAML file
            
        Returns:
            ArxivSearchClient: Arxiv search client
        """        
        # load search parameters from YAML
        dict_search_params = load_from_yml(path)
        # prepare search query
        search_query = str(ArxivSearchQuery(**dict_search_params['query']))
        # prepare search options
        search_options = dict_search_params['options']
        search_params = ArxivSearchParameters(query=search_query, **search_options)
        
        # prepare multi-threading options
        multi_threading_enabled = dict_search_params.get('enabled', False)
        multi_threading_chunk_size = dict_search_params.get('chunk_size', 1000)
        multi_threading_num_workers = dict_search_params.get('num_workers', 10)
        return cls(search_params, multi_threading_enabled, multi_threading_chunk_size, multi_threading_num_workers)
        
    def apply_query(self):
        """Apply query to Arxiv search API

        Returns:
            arxiv.arxiv.ResultList: Arxiv search results
        """        
        return arxiv.query(**self.search_params.__dict__)
        
