from logging import getLogger
from rester.struct import ResponseWrapper
import json
import requests


class HttpClient(object):
    logger = getLogger(__name__)
    ALLOWED_METHODS = ["get", "post", "put", "delete", "patch"]

    def __init__(self, **kwargs):
        self.extra_request_opts = kwargs

    def request(self, api_url, method, headers, params, data, is_raw):
        self.logger.info(
            '\n Invoking REST Call... api_url: %s, method: %s, headers %s : ', api_url, method, headers)

        try:
            func = getattr(requests, method)
        except AttributeError:
            self.logger.error('undefined HTTP method!!! %s', method)
            raise
        response = func(api_url, headers=headers, params=params, data=data, **self.extra_request_opts)

        if is_raw or 'application/json' not in response.headers.get('content-type', ''):
            payload = {"__raw__": response.text}
        else:    
            payload = response.json()
        self.logger.debug('Status: %s', response.status_code)
        self.log_headers(response.headers)
        if is_raw:
            self.logger.debug('Response:\n%s\n', response.text)
        else:
            self.logger.debug('Response:\n%s\n', json.dumps(payload, sort_keys=True, indent=2))

        return ResponseWrapper(response.status_code, payload, response.headers)
    
    def log_headers(self, headers):
        for header in headers:
            self.logger.debug('Header: %s = %s', header, headers[header])

