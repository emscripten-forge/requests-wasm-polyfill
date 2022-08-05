import sys

if "pyodide" not in sys.modules:
    import pyjs

    js = pyjs.js
    use_pyjs = True
else:
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


def parse_get_all_response_headers(request):
    body = r"""
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


__all__ = [
    "js",
    "js_to_py",
    "new_js_object",
    "js_null",
    "parse_get_all_response_headers",
]
