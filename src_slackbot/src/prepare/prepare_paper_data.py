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

def call_paper_prepare_api(span: str = "weekly"):
    yaml_app = load_from_yml("doc/params/bot.yml")
    parameter = yaml_app["crawler"][span]
    url = parameter["url"]
    response = call_get_request(url,headers=None,params=None)
    return response

if __name__ == "__main__":
    response = call_paper_prepare_api()