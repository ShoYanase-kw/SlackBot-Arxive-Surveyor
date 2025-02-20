import datetime as dt
import time
import unittest

from src.search_arxiv.arxiv_search_client import ArxivSearchClient, ArxivSearchParameters, ArxivSearchQuery

class TestArxivSearchClient(unittest.TestCase):
    def test_arxiv_search_query(self):
        query = ArxivSearchQuery(ti="title", au="author", abs="abstract", cat="category", all="all")
        self.assertEqual(str(query), "ti:title AND au:author AND abs:abstract AND cat:category AND all:all")
        
    def test_arxiv_search_parameters(self):
        params = ArxivSearchParameters(query="query", max_results=1000, max_chunk_results=1000, sort_by="relevance", sort_order="descending", id_list=[])
        self.assertEqual(params.query, "query")
        self.assertEqual(params.max_results, 1000)
        self.assertEqual(params.max_chunk_results, 1000)
        self.assertEqual(params.sort_by, "relevance")
        self.assertEqual(params.sort_order, "descending")
        self.assertEqual(params.id_list, [])
        
    def test_arxiv_search_client(self):
        client = ArxivSearchClient.from_yaml('tests/doc_test/test_search_arxiv_loading.yml')
        self.assertEqual(client.search_params.query, "ti:title AND au:author AND abs:abstract AND cat:cs.AI AND all:all AND submittedDate:[20250219000000 TO 20250220000000]")
        
    def test_arxiv_search_query(self):
        client = ArxivSearchClient.from_yaml('tests/doc_test/test_search_arxiv_execute.yml')
        response = client.apply_query()
        self.assertEqual(list(response[0].keys()), ['id', 'guidislink', 'updated', 'updated_parsed', 'published', 'published_parsed', 'title', 'title_detail', 'summary', 'summary_detail', 'authors', 'author_detail', 'author', 'arxiv_comment', 'links', 'arxiv_primary_category', 'tags', 'pdf_url', 'affiliation', 'arxiv_url', 'journal_reference', 'doi'])