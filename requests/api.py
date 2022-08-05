import time

from .models import Response
from .utils import js, new_js_object, js_null


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


get = lambda url, **kwargs: request(method="GET", url=url, **kwargs)
put = lambda url, **kwargs: request(method="PUT", url=url, **kwargs)
post = lambda url, **kwargs: request(method="POST", url=url, **kwargs)
update = lambda url, **kwargs: request(method="UPDATE", url=url, **kwargs)
delete = lambda url, **kwargs: request(method="DELETE", url=url, **kwargs)

__all__ = ["get", "put", "post", "update", "delete", "request"]
