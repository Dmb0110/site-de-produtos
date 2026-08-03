import urllib.request

req = urllib.request.Request('http://127.0.0.1:5000/produtos')
try:
    with urllib.request.urlopen(req, timeout=5) as res:
        print('status', res.status)
        print(res.read().decode('utf-8'))
except Exception as e:
    print(type(e).__name__, e)
