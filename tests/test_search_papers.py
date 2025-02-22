import unittest
from src.scheduler.search_papers import DateRangeSearchClient

class TestDateRangeSearchClient(unittest.TestCase):
    def test_fetch_citation(self):
        search_result_arxiv = {
            "title": "LaVCa: LLM-assisted Visual Cortex Captioning",
        }
        client = DateRangeSearchClient()
        result = client.fetch_citation(search_result_arxiv)
        self.assertEqual(type(result["citation_author"]), int)
        self.assertEqual(type(result["citation_paper"]), int)
        
    def test_search_weekly(self):
        client = DateRangeSearchClient()
        client.search_weekly()
        client.search_results_to_csv("doc/output/test_search_results.csv")