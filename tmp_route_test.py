import json
import urllib.request
import urllib.error


def req(method, path, data=None):
    url = 'http://127.0.0.1:5000' + path
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            print(method, path, r.status, r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(method, path, e.code, e.read().decode('utf-8'))
    except Exception as e:
        print('ERROR', method, path, e)


req('GET', '/produtos')
req('POST', '/produtos', {'nome': 'Teste', 'preco': 12.34, 'foto': 'http://foto.test/img.jpg'})
req('GET', '/produtos')
req('PUT', '/produtos/1', {'preco': 15.0, 'foto': 'http://foto.test/changed.jpg'})
req('GET', '/produtos/1')
req('DELETE', '/produtos/1')
req('GET', '/produtos/1')
