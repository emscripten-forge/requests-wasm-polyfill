import json

from .utils import js_to_py, parse_get_all_response_headers


class Response(object):
    def __init__(self, request, elapsed):
        self._request = request
        self._request_response = js_to_py(request.response)
        self.content = self._request_response.tobytes()
        self.encoding = "UTF-8"
        self.elapsed = elapsed
        self.status_code = self._request.status
        self.url = self._request.responseURL

    def __bool__(self):
        return self.status_code <= 400

    def close(self):
        pass

    @property
    def headers(self):
        return parse_get_all_response_headers(self._request)

    @property
    def text(self):
        return self.content.decode(self.encoding)

    def json(self):
        return json.loads(self.content.decode(self.encoding))

    def raise_for_status(self):
        if self.status_code > 400:
            raise RuntimeError(f"status code = {self.status_code}. thats bad")
