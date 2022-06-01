
import time
import json

if "pyodide" not in sys.modules:
    import pyjs 
    js = pyjs.js
    use_cpyjs = True
else
    import pyodide 
    import js
    use_pyjs = False


def js_to_py(js_object):
    if use_pyjs:
        return pyjs.to_py(js_object)
    else:
        return js_object.to_py()

def new_js_object(js_object, *args):

    if use_pyjs:
        return pyjs.new(js_object, *args)
    else:
        return js_object.new(*args)

def js_null():
    if use_pyjs:
        return pyjs.js_null()
    else:
        return None

def _parse_get_all_response_headers(request):
    body = """
        var allResponseHeaders = request.getAllResponseHeaders()
        var arr = allResponseHeaders.split("\r\n");
        var headers = {};
        allResponseHeaders
          .trim()
          .split(/[\r\n]+/)
          .map(value => value.split(/: /))
          .forEach(keyValue => {
            headers[keyValue[0].trim()] = keyValue[1].trim();
          });
        return headers
    """
    headers = js.Function("request", body)(request)
    return js_to_py(headers)


def request(method, url, headers=None, auth=None, data=None, params=None):

    # setup xml request
    xmlr = new_js_object(js.XMLHttpRequest)

    # url object
    url = new_js_object(js.URL, url)

    # params
    if params is not None:
        for k, v in params.items():
            url.searchParams.set(k, v)

    # basic auth
    if auth is not None:
        xmlr.open(method, url, False, auth[0], auth[1])
        xmlr.setRequestHeader(
            "Authorization", "Basic " + js.btoa(f"{auth[0]}:{auth[1]}")
        )
        xmlr.withCredentials = True
    else:
        xmlr.open(method, url, False)

    # headers
    if headers is None:
        headers = dict()
    for k, v in headers.items():
        xmlr.setRequestHeader(k, v)

    # this allows for easy js-to-py
    xmlr.responseType = "arraybuffer"

    # send xml request and time it
    t0 = time.time()
    if data is None:
        xmlr.send(js_null())
    else:
        request.send("")
    elapsed = time.time() - t0

    # build and return response object
    return Response(xmlr, elapsed)


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
        return status_code <= 400

    def close(self):
        pass

    @property
    def headers(self):
        return _parse_get_all_response_headers(self._request)

    @property
    def text(self):
        return self.content.decode(self.encoding)

    def json(self):
        return json.loads(self.content.decode(self.encoding))

    def raise_for_status(self):
        if self.status_code > 400:
            raise RuntimeError(f"status code = {self.status_code}. thats bad")


class Session(object):
    def __init__(self):
        self.auth = None
        self.headers = dict()

    def request(self, method, url, headers=None, auth=None, data=None, params=None):

        # handle headers
        if headers is None:
            headers = dict()
        headers = {**self.headers, **headers}

        # handle auth
        if auth is None:
            auth = self.auth

        return request(
            method=method, url=url, auth=auth, data=data, params=params, headers=headers
        )

    def get(self, url, **kwargs):
        return self.request(method="GET", url=url, **kwargs)

    def put(self, url, **kwargs):
        return self.request(method="PUT", url=url, **kwargs)

    def post(self, url, **kwargs):
        return self.request(method="POST", url=url, **kwargs)

    def update(self, url, **kwargs):
        return self.request(method="UPDATE", url=url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(method="DELETE", url=url, **kwargs)


get = lambda url, **kwargs: request(method="GET", url=url, **kwargs)
put = lambda url, **kwargs: request(method="PUT", url=url, **kwargs)
post = lambda url, **kwargs: request(method="POST", url=url, **kwargs)
update = lambda url, **kwargs: request(method="UPDATE", url=url, **kwargs)
delete = lambda url, **kwargs: request(method="DELETE", url=url, **kwargs)
