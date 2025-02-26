import requests
import json

from loguru import logger


def check_str_convert_to_json(json_text):
    if isinstance(json_text, str):
        try:
            json_object = json.loads(json_text)
        except json.JSONDecodeError:
            return False
    else:
        return json_text
    return json_object


def check_json_convert_to_str(json_object):
    if isinstance(json_object, dict):
        try:
            json_text = json.dumps(json_object)
        except json.JSONDecodeError:
            return False
    else:
        return json_object
    return json_text


def call_get_request(url, headers, params):
    headers = check_str_convert_to_json(headers)
    params = check_str_convert_to_json(params)
    
    logger.info(f"url({type(url)}): {url}")
    logger.info(f"headers({type(headers)}): {headers}")
    logger.info(f"params({type(params)}): {params}")
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def call_post_request(url, headers, params):
    headers = check_str_convert_to_json(headers)
    params = check_str_convert_to_json(params)
    
    logger.info(f"url({type(url)}): {url}")
    logger.info(f"headers({type(headers)}): {headers}")
    logger.info(f"params({type(params)}): {params}")
    response = requests.post(
        url,
        headers=headers,
        json=params
    )
    return response.json()
