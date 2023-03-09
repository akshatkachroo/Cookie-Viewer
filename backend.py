import http.cookiejar
import urllib.request
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/cookies')
def cookies():
    website = request.args.get('website')
    if not website:
        return 'Website not provided'
    try:
        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
        opener.open(website)
        cookies = []
        for cookie in cookie_jar:
            cookie_dict = {
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path,
                'expires': cookie.expires,
                'secure': cookie.secure,
                'httponly': cookie.has_nonstandard_attr('HttpOnly')
            }
            cookies.append(cookie_dict)
        response = jsonify(cookies)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except:
        return 'Error retrieving cookies'

if __name__ == '__main__':
    app.run(debug=True, host='139.180.138.95', port=8080)



