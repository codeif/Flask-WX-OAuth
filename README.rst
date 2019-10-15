Flask-WX-OAuth
==============

.. inclusion-marker-do-not-remove

官方文档
----------

- `微信网页授权 <https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140842>`_

- `授权后接口调用 <https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1419316518&lang=zh_CN>`_

- `公众平台测试账号 <http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login>`_

安装
-------

.. code-block:: sh

    pip install Flask-WX-OAuth

使用方式
----------

flask扩展的使用方式:

.. code-block:: python

    from flask_wx_oauth import WXOAuth

    wx_oauth = WXOAuth()
    wx_oauth.init_app(app)



也可以每次初始化后使用:

.. code-block:: python

    from flask_wx_oauth import WXOAuth
    wx_oauth = WXOAuth(appid='YOUR APPID', secret='YOUR SECRET')


在view中调用
--------------

.. code-block:: py

    next = request.args.get('next', '/')
    redirect_uri = url_for('.authorized', next=next, _external=True)
    params = dict(
        redirect_uri=redirect_uri,
        scope='snsapi_base',
    )
    return redirect(wx_oauth.get_authorize_url(**params))


运行示例代码
--------------

.. code-block:: sh

    docker build -t flask-wx-oauth .
    docker run -v $(pwd):/app -p 5000:5000 flask-wx-oauth
