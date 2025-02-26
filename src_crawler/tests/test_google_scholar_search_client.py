# import unittest

# from src.search_google_scholar.search_client_google_scholar import GooglescholarLookUpQuery, GooglescholarSearchClient


# class TestGooglescholarSearchClient(unittest.TestCase):
#     def test_google_scholar_search_client_invalid_query_type(self):
#         with self.assertRaises(AssertionError):
#             GooglescholarSearchClient(query_value="arxiv_id", query_type="invalid_query_type")
        
#     def test_google_scholar_search_client_fetch_element_invalid_query_type(self):
#         with self.assertRaises(AssertionError):
#             GooglescholarSearchClient(query_value="arxiv_id", query_type="invalid_query_type").fetch_element()
            
#     def test_google_scholar_search_client_fetch_citation_by_author(self):
#         client_author = GooglescholarSearchClient(query_value="Yu Takagi", query_type="author")
#         citation = client_author.fetch_citation()
#         self.assertEqual(citation, 614)
        
#     def test_google_scholar_search_client_fetch_citation_by_paper(self):
#         client_author = GooglescholarSearchClient(query_value="2303.09097", query_type="paper")
#         citation = client_author.fetch_citation()
#         self.assertEqual(citation, 6)