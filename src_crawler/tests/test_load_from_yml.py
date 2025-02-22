import unittest

from src.params.load_from_yml import load_from_yml

class TestLoadFromYml(unittest.TestCase):
    def test_load_from_yml(self):
        config = load_from_yml('tests/doc_test/test_search_arxiv_loading.yml')
        config_options = config['options']
        self.assertEqual(config_options['max_results'], 1000)
        self.assertEqual(config_options['max_chunk_results'], 1000)
        self.assertEqual(config_options['sort_by'], "relevance")
        self.assertEqual(config_options['sort_order'], "descending")
        self.assertEqual(config_options['id_list'], [])
        
    
        
if __name__ == '__main__':
    unittest.main()