Flask-WX-OAuth
==============


使用方式::

    wx_oauth = WXOAuth()
    wx_oauth.init_app(app)

配置 WX_APPID 和 WX_SECRET

在view中调用::

    next = request.args.get('next', '/')
    redirect_uri = url_for('.authorized', next=next, _external=True)
    params = {
        'redirect_uri': redirect_uri,
        'scope': 'snsapi_base',
    }
    return redirect(wx_oauth.get_authorize_url(**params))
