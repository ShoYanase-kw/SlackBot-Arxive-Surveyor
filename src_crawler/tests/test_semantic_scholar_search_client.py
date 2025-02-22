import unittest
import urllib

from src.search_semantic_scholar.search_client_semantic_scholar import S2scholarLookUpQuery, S2scholarSearchClient


class TestS2scholarSearchClient(unittest.TestCase):
    def test_semantic_scholar_search_client_invalid_query_type(self):
        with self.assertRaises(AssertionError):
            S2scholarSearchClient(query_value="arxiv_id", query_type="invalid_query_type")
            
    # def test_semantic_scholar_search_client_fetch_citation_by_author(self):
    #     client_author = S2scholarSearchClient(query_value="Yu Takagi", query_type="author")
    #     citation = client_author.fetch_citation()
    #     self.assertEqual(citation, 614)
        
    def test_semantic_scholar_search_client_fetch_citation_by_paper(self):
        client_author = S2scholarSearchClient(query_value="LLM", query_type="paper")
        with self.assertRaises(urllib.error.HTTPError):
            client_author.fetch_paper_with_citation()
        
    def test_semantic_scholar_search_client_fetch_citation_by_paper(self):
        client_author = S2scholarSearchClient(query_value="LaVCa: LLM-assisted Visual Cortex Captioning", query_type="paper")
        citation = client_author.fetch_paper_with_citation()
        self.assertEqual(type(citation), tuple)