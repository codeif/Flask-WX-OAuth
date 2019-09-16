微信授权demo
===============

文档
-------

- `公众平台测试账号 <http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login>`_ 完成测试

配置文件
----------

在下面文件配置文件不会被提交到git::

    demo/instance/application.cfg

修改授权域名
------------

体验接口权限表 —> 网页授权获取用户基本信息

修改为： your-ip:port, eg. 192.168.1.2:5000 或者 127.0.0.1:5000
