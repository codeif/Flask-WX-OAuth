from functools import wraps

from flask import redirect, request, session, url_for

from .core import wx_oauth


def get_authorize_url():
    redirect_uri = url_for('views.authorized', next=request.full_path, _external=True)
    params = dict(
        redirect_uri=redirect_uri,
        scope='snsapi_userinfo',
    )
    return wx_oauth.get_authorize_url(**params)


def openid_required(func):
    # 检查结果中的gym_id
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'openid' not in session:
            return redirect(get_authorize_url())

        resp = func(*args, **kwargs)

        return resp
    return wrapper
