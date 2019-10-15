# -*- coding: utf-8 -*-
# from rauth.compat import is_basestring, parse_qsl, urlencode
# from rauth.service import Service
# from rauth.session import OAUTH2_DEFAULT_TIMEOUT, RauthSession
from urllib.parse import urlencode

import requests

DEFAULT_TIMEOUT = 10
__version__ = '0.2.2'


class WXOAuth:
    """网站应用微信OAuth2.0登录服务"""
    def __init__(self, app=None, appid=None, secret=None):
        """初始化

        :param app: (optional) 使用配置中的WX_APPID和WX_SECRET
        :param appid: (optional) 微信appid
        :param secret: (optional) 微信secret
        """
        self.base_url = 'https://api.weixin.qq.com/sns'
        self.authorize_url = 'https://open.weixin.qq.com/connect/oauth2/authorize'

        self.appid = appid
        self.secret = secret

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """使用app config初始化配置"""
        if not self.appid:
            self.appid = app.config['WX_APPID']
        if not self.secret:
            self.secret = app.config['WX_SECRET']

    def get_authorize_url(self, redirect_uri, scope='snsapi_base',
                          **params):
        """获取用户同意授权，获取code的url"""
        assert redirect_uri
        params.update({
            'appid': self.appid,
            'response_type': 'code',
            'scope': scope,
            'redirect_uri': redirect_uri
        })

        query = urlencode(sorted(params.items()))
        return '{0}?{1}#wechat_redirect'.format(self.authorize_url, query)

    def get_access_token(self, code):
        """通过code获取access_token的接口。返回dict

        正确的返回:

        .. code-block:: json

            {
                "access_token":"ACCESS_TOKEN",
                "expires_in":7200,
                "refresh_token":"REFRESH_TOKEN","openid":"OPENID",
                "scope":"SCOPE"
            }
        """
        url = self.base_url + '/oauth2/access_token'
        params = {
            'appid': self.appid,
            'secret': self.secret,
            'code': code,
            'grant_type': 'authorization_code',
        }
        r = requests.get(url, params=params)
        return r.json()

    def refresh_token(self, refresh_token):
        """access_token是调用授权关系接口的调用凭证，由于access_token有效期（目前为2个小时）较短，当access_token超时后，可以使用refresh_token进行刷新，access_token刷新结果有两种：

        1. 若access_token已超时，那么进行refresh_token会获取一个新的access_token，新的超时时间；

        2. 若access_token未超时，那么进行refresh_token不会改变access_token，但超时时间会刷新，相当于续期access_token。

        refresh_token拥有较长的有效期（30天），当refresh_token失效的后，需要用户重新授权，所以，请开发者在refresh_token即将过期时（如第29天时），进行定时的自动刷新并保存好它。

        正确的返回:

        .. code-block:: json

            {
                "access_token":"ACCESS_TOKEN",
                "expires_in":7200,
                "refresh_token":"REFRESH_TOKEN",
                "openid":"OPENID",
                "scope":"SCOPE"
            }
        """
        url = self.base_url + '/oauth2/refresh_token'
        params = {
            'appid': self.appid,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        r = requests.get(url, params=params)
        return r.json()

    def check_access_token(self, access_token, openid):
        """检验授权凭证（access_token）是否有效

        正确的Json返回结果：

        .. code-block:: json

            {
                "errcode":0,
                "errmsg":"ok"
            }

        错误的Json返回示例:

        .. code-block:: json

            {
                "errcode":40003,
                "errmsg":"invalid openid"
            }
        """
        url = self.base_url + '/auth'
        params = {
            'access_token': access_token,
            'openid': openid,
        }
        r = requests.get(url, params=params)
        return r.json()

    def get_userinfo(self, access_token, openid):
        """此接口用于获取用户个人信息。开发者可通过OpenID来获取用户基本信息。特别需要注意的是，如果开发者拥有多个移动应用、网站应用和公众帐号，可通过获取用户基本信息中的unionid来区分用户的唯一性，因为只要是同一个微信开放平台帐号下的移动应用、网站应用和公众帐号，用户的unionid是唯一的。换句话说，同一用户，对同一个微信开放平台下的不同应用，unionid是相同的。
        请注意，在用户修改微信头像后，旧的微信头像URL将会失效，因此开发者应该自己在获取用户信息后，将头像图片保存下来，避免微信头像URL失效后的异常情况。

        正确的Json返回结果:

        .. code-block:: json

            {
                "openid":"OPENID",
                "nickname":"NICKNAME",
                "sex":1,
                "province":"PROVINCE",
                "city":"CITY",
                "country":"COUNTRY",
                "headimgurl": "头像url",
                "privilege":[
                    "PRIVILEGE1",
                    "PRIVILEGE2"
                ],
                "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }
        """

        url = self.base_url + '/userinfo'
        params = {
            'access_token': access_token,
            'openid': openid,
        }
        r = requests.get(url, params=params)
        if r.encoding == 'ISO-8859-1':
            r.encoding = 'UTF-8'
        return r.json()
