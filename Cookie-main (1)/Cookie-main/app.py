import http.cookiejar
import urllib.request
import datetime
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/cookies')
def cookies():
    website = request.args.get('website')
    if not website:
        return 'Website not provided'

    try:
        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
        opener.open(website)

        # Check if the website is using end-to-end encryption
        # Check if the website is using end-to-end encryption
        is_encrypted = False
        if "https://" in website and "Strict-Transport-Security" in opener.open(website).info().as_string():
            is_encrypted = True


        # Get the current date and time
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')

        # Get the client's IP address from the request object
        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

        # Use an IP geolocation service to get the client's location
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        if response.status_code == 200:
            location = f"{response.json()['city']}, {response.json()['region']}, {response.json()['country_name']}"
        else:
            location = 'Unknown'

        # Get the number of pages on the website
        response = urllib.request.urlopen(website)
        html = response.read()
        pages = html.count(b'<html')  # Count the number of <html> tags

        # Create a list to store the cookies
        cookies = []

        # Iterate through the cookies and add them to the list
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

        # Create a dictionary to store the scan information
        scan_info = {
            'date': date,
            'time': time,
            'location': location,
            'pages': pages,
            'is_encrypted': is_encrypted
        }

        # Create a dictionary to store the scan results
        scan_results = {
            'scan_info': scan_info,
            'cookies': cookies
        }

        # Create a JSON response with the scan results
        response = jsonify(scan_results)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except:
        return 'Error retrieving cookies'

if __name__ == '__main__':
    app.run(debug=True)




