from flask import Blueprint, jsonify, redirect, request, url_for

from .core import wx_oauth

bp = Blueprint('demo', __name__)


@bp.route('/')
def index():
    redirect_uri = url_for('.authorized', _external=True)
    params = dict(
        redirect_uri=redirect_uri,
        scope='snsapi_userinfo',
    )
    return redirect(wx_oauth.get_authorize_url(**params))


@bp.route('/authorized')
def authorized():
    code = request.args.get('code')
    if not code:
        return 'missing param code'

    access_token = wx_oauth.get_access_token(code)
    return jsonify(access_token)
