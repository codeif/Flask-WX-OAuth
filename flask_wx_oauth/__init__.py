# -*- coding: utf-8 -*-
from rauth.compat import is_basestring, parse_qsl, urlencode
from rauth.service import Service
from rauth.session import OAUTH2_DEFAULT_TIMEOUT, RauthSession


class WXOAuth(Service):
    """网站应用微信OAuth2.0登录服务"""
    def __init__(self, app=None):
        #: The provider's access token URL.
        self.access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        #: Object used to construct sessions with.
        self.session_obj = WXSession

        if app is not None:
            self.init_app(app)

        base_url = 'https://api.weixin.qq.com/sns/'
        authorize_url = 'https://open.weixin.qq.com/connect/oauth2/authorize'
        super(WXOAuth, self).__init__('wechat', base_url, authorize_url)

    def init_app(self, app):
        self.appid = app.config['WX_APPID']
        self.secret = app.config['WX_SECRET']

    def get_session(self, access_token=None, openid=None):
        '''
        If provided, the `access_token` and `openid` parameter is used to
        initialize an authenticated session, otherwise an unauthenticated
        session object is generated.
        Returns an instance of :attr:`session_obj`..

        :param access_token: access_token with which to initilize the session.
        :param openid: openid with which to initilize the session.
        '''
        if access_token and openid:
            session = self.session_obj(self.appid,
                                       self.secret,
                                       access_token,
                                       openid,
                                       service=self)
        else:  # pragma: no cover
            session = self.session_obj(self.appid,
                                       self.secret,
                                       service=self)
        return session

    def get_authorize_url(self, redirect_uri=None, scope='snsapi_base',
                          **params):
        '''Returns a formatted authorize URL.'''
        assert redirect_uri
        params.update({'appid': self.appid,
                       'response_type': 'code',
                       'scope': scope,
                       'redirect_uri': redirect_uri})

        query = urlencode(sorted(params.items()))
        return '{0}?{1}#wechat_redirect'.format(self.authorize_url, query)

    def get_auth_session(self, code, method='GET', **kwargs):
        '''ets an access token, intializes a new authenticated session with the
        access token. Returns an instance of :attr:`session_obj`.
        '''
        access_token = self.get_access_token(code, method, **kwargs)
        session = self.get_session(access_token['access_token'],
                                   access_token['openid'])

        return session

    def get_raw_access_token(self, code, method='GET', **kwargs):
        params = {
            'appid': self.appid,
            'secret': self.secret,
            'code': code,
            'grant_type': 'authorization_code',
        }
        kwargs['params'] = params
        session = self.get_session()
        return session.request(method, self.access_token_url, **kwargs)

    def get_access_token(self,
                         code,
                         method='GET',
                         **kwargs):
        '''
        `文档 <https://open.weixin.qq.com/cgi-bin/showdocument?
        action=dir_list&t=resource/res_list&verify=1&id=open1419316505>`_

        正确的返回::

            {
                "access_token":"ACCESS_TOKEN",
                "expires_in":7200,
                "refresh_token":"REFRESH_TOKEN",
                "openid":"OPENID",
                "scope":"SCOPE",
                "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
            }

        =============  =================================================
        参数           说明
        =============  =================================================
        access_token   接口调用凭证
        expires_in     access_token接口调用凭证超时时间，单位（秒）
        refresh_token  用户刷新access_token
        openid         授权用户唯一标识
        scope          用户授权的作用域，使用逗号（,）分隔
        unionid        当且仅当该网站应用已获得该用户的userinfo授权时，
                       才会出现该字段。
        =============  =================================================

        错误返回样例::

            {"errcode":40029,"errmsg":"invalid code"}

        :param code: 授权临时票据code
        :param method: A string representation of the HTTP method to be used,
            defaults to `GET`.
        :type method: str
        :param \*\*kwargs: Optional arguments. Same as Requests.
        :type \*\*kwargs: dict
        '''
        r = self.get_raw_access_token(code, method, **kwargs)
        return r.json()


class WXSession(RauthSession):
    __attrs__ = RauthSession.__attrs__ + ['appid',
                                          'secret',
                                          'access_token',
                                          'openid',
                                          'refresh_token']

    def __init__(self,
                 appid=None,
                 secret=None,
                 access_token=None,
                 openid=None,
                 service=None,
                 access_token_key=None):

        #: Client credentials.
        self.appid = appid
        self.secret = secret

        #: Access token.
        self.access_token = access_token
        self.openid = openid

        #: Access token key, e.g. 'access_token'.
        self.access_token_key = access_token_key or 'access_token'

        super(WXSession, self).__init__(service)

    def request(self, method, url, **req_kwargs):
        '''
        A loose wrapper around Requests' :class:`~requests.sessions.Session`
        which injects OAuth 2.0 parameters.
        :param method: A string representation of the HTTP method to be used.
        :type method: str
        :param url: The resource to be requested.
        :type url: str
        :param \*\*req_kwargs: Keyworded args to be passed down to Requests.
        :type \*\*req_kwargs: dict
        '''
        req_kwargs.setdefault('params', {})

        url = self._set_url(url)

        if is_basestring(req_kwargs['params']):
            req_kwargs['params'] = dict(parse_qsl(req_kwargs['params']))

        if self.access_token and self.openid:
            req_kwargs['params'].update({'access_token': self.access_token,
                                         'openid': self.openid})

        req_kwargs.setdefault('timeout', OAUTH2_DEFAULT_TIMEOUT)

        resp = super(WXSession, self).request(method, url,
                                              **req_kwargs)
        if resp.encoding == 'ISO-8859-1':
            resp.encoding = 'utf-8'
        return resp
