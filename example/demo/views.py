from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from .core import wx_oauth

global_info = {}

bp = Blueprint('demo', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/get-access-token')
def get_access_token():
    if not global_info:
        redirect_uri = url_for('.authorized', _external=True)
        params = dict(
            redirect_uri=redirect_uri,
            scope='snsapi_userinfo',
        )
        return redirect(wx_oauth.get_authorize_url(**params))
    return render_template('access_token.html', items=global_info.items())


@bp.route('/authorized')
def authorized():
    code = request.args.get('code')
    if not code:
        return 'missing param code'
    token_info = wx_oauth.get_access_token(code)
    global global_info
    global_info = token_info
    # return render_template('access_token.html', items=access_token.items())
    return redirect(url_for('.get_access_token'))


@bp.route('/refresh-token')
def refresh_token():
    global global_info
    refresh_token = global_info['refresh_token']
    token_info = wx_oauth.refresh_token(refresh_token)
    global_info = token_info
    return jsonify(token_info)


@bp.route('/check-access-token')
def check_access_token():
    access_token = global_info['access_token']
    openid = global_info['openid']
    result = wx_oauth.check_access_token(access_token, openid)
    return jsonify(result)


@bp.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    if request.method == 'GET':
        return render_template('userinfo.html', info=global_info)
    else:
        access_token = request.form['access_token']
        openid = request.form['openid']
        return jsonify(wx_oauth.get_userinfo(access_token, openid))
