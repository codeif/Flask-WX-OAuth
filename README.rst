Flask-WX-OAuth
==============

微信文档: `微信网页授权 <https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140842>`_

安装
-------

.. code-block:: sh

    pip install Flask-WX-OAuth

使用方式
----------

.. code-block:: python

    wx_oauth = WXOAuth()
    wx_oauth.init_app(app)

配置 WX_APPID 和 WX_SECRET

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
    docker run -p 5000:5000 flask-wx-oauth
