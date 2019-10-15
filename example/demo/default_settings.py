from datetime import timedelta

SECRET_KEY = b'\xdc\x9dY\xcc\x89r\xc4o'

DEBUG = True
JSON_AS_ASCII = False

# session过期的相关设置
PERMANENT_SESSION_LIFETIME = timedelta(seconds=10)

WX_APPID = 'YOUR WX APPID'
WX_SECRET = 'YOUR WX SECRET'
