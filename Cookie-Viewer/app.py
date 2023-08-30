from flask_cors import CORS
import http.cookiejar
import urllib.request
import datetime
from flask import Flask, jsonify, request, make_response
import requests
import ssl

app = Flask(__name__)
CORS(app)

def is_first_party_cookie(website_domain, cookie_domain):
    if cookie_domain.startswith('.'):
        cookie_domain = cookie_domain[1:]
    return website_domain.endswith(cookie_domain)

def has_cookie_notice(html):
    keywords = ["cookie policy", "cookie consent", "privacy policy", "use of cookies", "we use cookies"]
    lower_html = html.lower()
    return any(keyword in lower_html for keyword in keywords)


@app.route('/cookies')
def cookies():
    website = request.args.get('website')
    if not website:
        return make_response(jsonify({'error': 'Website not provided'}), 400)
    website = website.lower()
    try:
        cookie_jar = http.cookiejar.CookieJar()
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cookie_jar),
            urllib.request.HTTPSHandler(context=ssl_context)  # Pass the SSL context to the handler
        )
        opener.open(website)


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
        # Use an IP geolocation service to get the client's location
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        if response.status_code == 200:
            city = response.json().get('city', 'Unknown')
            region = response.json().get('region', 'Unknown')
            country_name = response.json().get('country_name', 'Unknown')
            location = f"{city}, {region}, {country_name}"
        else:
            location = 'Unknown'


        # Get the number of pages on the website
        response = opener.open(website)  # Replace urllib.request.urlopen with opener.open
        html = response.read()
        pages = html.count(b'<html')  # Count the number of <html> tags

        cookie_notice_detected = has_cookie_notice(html.decode('utf-8'))

        # Create a list to store the cookies
        cookies = []
        scan_info_list=[]

        # Iterate through the cookies and add them to the list
        for cookie in cookie_jar:
            
            if is_first_party_cookie(website, cookie.domain):
                cookie_category = "First-Party"
            else:
                cookie_category = "Advertising"
            
            cookie_dict = {
                'name': cookie.name,
                'domain': cookie.domain,
                'expires': cookie.expires,
                'secure': cookie.secure,
                'httponly': cookie.has_nonstandard_attr('HttpOnly'),
                'category': cookie_category,
            }
            cookies.append(cookie_dict)

        # Create a dictionary to store the scan information
        scan_info = {
            'date': date,
            'time': time,
            'location': location,
            'pages': pages,
            'is_encrypted': is_encrypted,
            'cookie_notice_detected': cookie_notice_detected,
            'cookie_notice_detected': cookie_notice_detected
        }
        scan_info_list.append(scan_info)
        print(scan_info)

        # Create a dictionary to store the scan results
        scan_results = {
            'scan_info_list': scan_info_list,
            'cookies': cookies
        }

        # Create a JSON response with the scan results
        response = jsonify(scan_results)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        print("Error:", e)
        return make_response(jsonify({'error': 'An error occurred while fetching cookies'}), 500)
       

if __name__ == '__main__':
    app.run(debug=True)




