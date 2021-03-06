import time

import requests
from requests import Response


class Http:
    def __init__(self):
        self.sess = requests.session()

    @property
    def headers(self):
        return self.sess.headers

    @headers.setter
    def headers(self, value):
        self.sess.headers.update(value)

    def get(self, **kwargs):
        return self._request('GET', **kwargs)

    def post(self, **kwargs):
        return self._request('POST', **kwargs)

    def _request(self, method: str, url: str, params: dict = None, data: dict = None, json: dict = None,
                 encoding: str = 'utf8', headers: dict = None, noprint=False) -> Response:
        """
        http请求
        :param method: 请求方法
        :param url: url
        :param params: 请求参数
        :param data: 请求数据
        :param encoding: 编码
        :return: request之后的Response对象
        """
        if headers:
            self.headers.update(headers)
        url, data, json = self._before_request(url, params, data, json)
        if data is not None:
            res = self.sess.request(method, url=url, data=data, timeout=30)
        else:
            res = self.sess.request(method, url=url, json=json, timeout=30)
        res = self._end_request(res, encoding)
        if not noprint:
            print(method, url, res.status_code)
        time.sleep(.5)
        return res

    @staticmethod
    def _before_request(url: str, params: dict, data: dict, json: dict) -> (str, str):
        """
        request之前的准备，可根据逻辑重载
        :param url: url
        :param params: 请求参数
        :param data: 请求
        :return: url，data元组
        """
        # 逻辑写这里
        return url, data, json

    @staticmethod
    def _end_request(res: Response, encoding: str) -> Response:
        """
        request之后的处理，可根据逻辑重载
        :param res: request之后的Response对象
        :return: 处理之后的Response对象
        """
        res.encoding = encoding
        return res
