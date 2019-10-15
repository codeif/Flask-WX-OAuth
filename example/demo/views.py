from flask import Blueprint, jsonify, redirect, render_template, request, session

from .core import wx_oauth
from .decorators import openid_required

bp = Blueprint('views', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/authorized')
def authorized():
    code = request.args.get('code')
    next_ = request.args.get('next', '/')
    if not code:
        return 'missing param code'
    at_data = wx_oauth.get_access_token(code)
    # session可以过期
    session.permanent = True
    session['openid'] = at_data['openid']
    session['access_token'] = at_data['access_token']
    session['refresh_token'] = at_data['refresh_token']
    return redirect(next_)


@bp.route('/refresh-token')
@openid_required
def refresh_token():
    refresh_token = session['refresh_token']
    at_data = wx_oauth.refresh_token(refresh_token)
    session.permanent = True
    session['openid'] = at_data['openid']
    session['access_token'] = at_data['access_token']
    session['refresh_token'] = at_data['refresh_token']
    return jsonify(at_data)


@bp.route('/check-access-token')
@openid_required
def check_access_token():
    access_token = session['access_token']
    openid = session['openid']
    result = wx_oauth.check_access_token(access_token, openid)
    return jsonify(result)


@bp.route('/userinfo', methods=['GET', 'POST'])
@openid_required
def userinfo():
    access_token = session['access_token']
    openid = session['openid']
    info = wx_oauth.get_userinfo(access_token, openid)
    return jsonify(info)
