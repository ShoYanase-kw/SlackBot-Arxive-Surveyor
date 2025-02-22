from util.call_requests import call_post_request, call_get_request
from params.load_from_yml import load_from_yml

def call_paper_data_api(scope: str = "latest"):
    yaml_app = load_from_yml("doc/params/bot.yml")
    parameter = yaml_app["crawler"][scope]
    url = parameter["url"]
    headers = parameter["headers"]
    data = parameter["data"]
    response = call_post_request(url, headers, data)
    return response
