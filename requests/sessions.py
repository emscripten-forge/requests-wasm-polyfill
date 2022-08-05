from .api import request


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
