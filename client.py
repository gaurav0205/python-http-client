import requests
from functools import wraps


class Client(object):

    def __init__(self, host=None, api_key=None, headers=None):
        self.host = host
        self.request_headers = {'Authorization': 'Bearer ' + api_key}
        if headers:
            self._set_headers(headers)
        self._count = 0
        self._cache = {}
        self._status_code = None
        self._body = None
        self._headers = None
        self._response = None

    def _reset(self):
        self._count = 0
        self._cache = {}
        self._response = None

    def _add_to_cache(self, value):
        self._cache[self._count] = value
        self._count += 1

    def _build_url(self):
        url = ""
        count = 0
        while count < len(self._cache):
            url += "/" + self._cache[count]
            count += 1
        return self.host + url

    def _set_response(self, response):
        self._status_code = response.status_code
        self._body = response.text
        self._headers = response.headers

    def _set_headers(self, headers):
        self.request_headers.update(headers)

    def _(self, value):
        self._add_to_cache(value)
        return self

    def __getattr__(self, value):
        self._add_to_cache(value)
        return self

    @property
    def status_code(self):
        return self._status_code

    @property
    def body(self):
        return self._body

    @property
    def headers(self):
        return self._headers

    def method_wrapper(func):

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if kwargs['headers']:
                self._set_headers(kwargs['headers'])

            response = func(self, *args, **kwargs)

            self._set_response(self._response)
            self._reset()
            return response

        return wrapper

    @method_wrapper
    def get(self, data=None, params=None, headers=None):
        self._response = requests.get(self._build_url(),
                                      params=params,
                                      data=data,
                                      headers=self.request_headers)
        return self

    @method_wrapper
    def post(self, data=None, params=None, headers=None):
        self._response = requests.post(self._build_url(),
                                       params=params,
                                       data=data,
                                       headers=self.request_headers)
        return self

    @method_wrapper
    def put(self, data=None, params=None, headers=None):
        self._response = requests.put(self._build_url(),
                                      params=params,
                                      data=data,
                                      headers=self.request_headers)
        return self

    @method_wrapper
    def patch(self, data=None, params=None, headers=None):
        self._response = requests.patch(self._build_url(),
                                        params=params,
                                        data=data,
                                        headers=self.request_headers)
        return self

    @method_wrapper
    def delete(self, data=None, params=None, headers=None):
        self._response = requests.delete(self._build_url(),
                                         params=params,
                                         data=data,
                                         headers=self.request_headers)
        return self
