from flask import Flask, render_template, request,jsonify
import socket
import requests
import threading
from urllib.parse import urlparse
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from auth import auth_page
from auth import db

from middleware import authentication, guest

from flask_admin import Admin
app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='microblog', template_mode='bootstrap3')

app.config['SECRET_KEY'] = 'thisismysecretkey' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.register_blueprint(auth_page, url_prefix="/auth")

db.init_app(app) 


with app.app_context():
    db.create_all()



@app.route('/')
def mainHome():
    return render_template('mainHome.html')

@app.route('/mainhome')
@guest
def mainhome():
    return render_template('mainHome.html')

@app.route('/home')
@authentication

def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/scanner')
def scanner():
    return render_template('scanner.html')


@app.route('/passwordGen')
def passwordGen():
    return render_template('passwordGen.html')



@app.route('/passwordchecker')
def passwordchecker():
    return render_template('passwordchecker.html')


@app.route('/subdomain')
def subdomain():
    return render_template('subdomain.html')


# @app.route('/signup')
# def signup():
#     return render_template('signup.html')

# @app.route('/signin')
# def signin():
#     return render_template('signin.html')

@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')

# from flask import Flask, render_template, request
# import dns.resolver

# app = Flask(__name__)

# def find_subdomains(domain):
#     subdomains = []
#     try:
#         answers = dns.resolver.query(domain, 'CNAME')
#         for rdata in answers:
#             subdomains.append(rdata.target)
#     except dns.resolver.NoAnswer:
#         pass
#     return subdomains

# @app.route('/subdomain', methods=['GET', 'POST'])
# def subdomain():
#     subdomains = []
#     if request.method == 'POST':
#         domain = request.form['domain']
#         if domain:
#             subdomains = find_subdomains(domain)
#     return render_template('subdomain.html', subdomains=subdomains)

# if __name__ == '__main__':
#     app.run(debug=True)



# import time  # Import the time module

# # Function to check for XSS vulnerability
# def check_xss(url):
#     try:
#         # Initialize Chrome WebDriver
#         service = Service('chromedriver.exe')  # Provide the path to your chromedriver executable
#         driver = webdriver.Chrome(service=service)

#         # Open the web page
#         driver.get(url)

#         # List of XSS payloads to test
#         xss_payloads = [
#             '<script>alert("XSS");</script>',
#             '<img src="x" onerror="alert(\'XSS\');">',
#             '"><script>alert("XSS");</script>',
#             '<svg/onload=alert(\'XSS\')>',
#             '<iframe src="javascript:alert(\'XSS\');" />'
#             # Add more payloads as needed
#         ]

#         results = []

#         for payload in xss_payloads:
#             try:
#                 # Use JavaScript to inject the payload into the input field
#                 driver.execute_script('''
#                     var input = document.querySelector('input[type="text"]');
#                     input.value = arguments[0];
#                 ''', payload)

#                 # Pause for a moment to allow the payload to take effect in the browser (adjust the delay as needed)
#                 time.sleep(1)  # Adjust the delay (in seconds) as needed

#                 # Submit the form if available (some websites may not have a form)
#                 form = driver.find_element(By.TAG_NAME, 'form')
#                 form.submit()

#                 # Check if the alert dialog appears (indicating XSS vulnerability)
#                 alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
#                 alert_text = alert.text
#                 alert.accept()

#                 if alert_text:
#                     results.append("The website has an XSS vulnerability with payload: " + payload)
#                 else:
#                     results.append("No alert for payload: " + payload)
#             except Exception as e:
#                 # If no alert is triggered, continue to the next payload
#                 continue

#             # Reload the page for the next payload
#             driver.get(url)

#         # Close the browser
#         driver.quit()

#         if results:
#             return "\n".join(results)
#         else:
#             return "The website is safe from known XSS payloads"
#     except Exception as e:
#         return str(e)


# # Route to handle XSS scanning
# @app.route('/scan', methods=['POST'])
# def scan():
#     url = request.form['url']
#     result = check_xss(url)
#     return jsonify({'result': result})


# if __name__ == '__main__':
#     app.run(debug=True)






# --------------dns_lookup-----------------
# --------------dns_lookup-----------------
# --------------dns_lookup-----------------
# --------------dns_lookup-----------------


def get_ip_address(domain):
    parsed_url = urlparse(domain)
    domain_name = parsed_url.hostname
    port = parsed_url.port

    try:
        addr_info = socket.getaddrinfo(domain_name, port)
        ip_address = addr_info[0][4][0]
        return ip_address
    except socket.gaierror:
        return None

@app.route('/dns_lookup', methods=['GET', 'POST'])
def dns_lookup():
    if request.method == 'POST':
        domain_name = request.form['domain']
        ip_address = get_ip_address(domain_name)

        if ip_address:
            result = f"The IP address of {domain_name} is {ip_address}."
        else:
            result = f"Unable to find the IP address of {domain_name}."

        return render_template('dns_lookup.html', result=result)
    else:
        return render_template('dns_lookup.html')


def scan_port(target, port, results):
    # print("Scanning port:", port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    conn = s.connect_ex((target, port))
    if not conn:
        results.append({"port": port, "status": "Open"})
    s.close()



# ---------------port_scanning---------------------
# ---------------port_scanning---------------------
# ---------------port_scanning---------------------
# ---------------port_scanning---------------------
# ---------------port_scanning---------------------

@app.route('/port_scanning', methods=['GET', 'POST'], endpoint='app.port_scanning')
def port_scanning():
    if request.method == 'POST':
        target = request.form['target']
        start_port = int(request.form['start_port'])
        end_port = int(request.form['end_port'])

        if start_port < 1 or start_port > 65535 or end_port < 1 or end_port > 65535:
            return render_template('port_scanning.html', error="Invalid port number. Port numbers should be between 1 and 65535.")

        results = []
        threads = []

        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=scan_port, args=(target, port, results))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        if not results:
            message = "No open ports found."
        else:
            message = None

        return render_template('port_scanning.html', target=target, results=results, message=message)
    else:
        return render_template('port_scanning.html')
    



# -----------------what is my ip---------------------------
# -----------------what is my ip---------------------------
# -----------------what is my ip---------------------------
# -----------------what is my ip---------------------------

def get_local_ipv6_address():
    try:
        hostname = socket.gethostname()
        addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET6)
        ipv6_addresses = [info[4][0] for info in addr_info]
        return ipv6_addresses
    except socket.error as e:
        print(f"Error occurred while fetching the local IPv6 address: {e}")
    return None


@app.route('/whatismyip')

def whatismyip():
    ipv4_address = socket.gethostbyname(socket.gethostname())
    ipv6_addresses = get_local_ipv6_address()

    return render_template('whatismyip.html', ipv4_address=ipv4_address, ipv6_addresses=ipv6_addresses)

# ---------------------IP_Address_Lookup-----------------------------
# ---------------------IP_Address_Lookup-----------------------------
# ---------------------IP_Address_Lookup-----------------------------
# ---------------------IP_Address_Lookup-----------------------------

import requests

def get_location(ip):
    url = f"http://ipinfo.io/{ip}/json"
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        return None
    
    return {
        'IP': data['ip'],
        'City': data.get('city', 'N/A'),
        'Region': data.get('region', 'N/A'),
        'Country': data.get('country', 'N/A'),
        'Location': data.get('loc', 'N/A'),
        'ISP': data.get('org', 'N/A'),
        'Is Proxy': data.get('proxy', 'N/A'),
        'District': data.get('district', 'N/A'),
        'ZIP Code': data.get('postal', 'N/A'),
        'Category': data.get('category', 'N/A'),
        'Domain': data.get('hostname', 'N/A'),
    }

@app.route('/ip_address_lookup', methods=['GET', 'POST'])
def ip_address_lookup():
    if request.method == 'POST':
        ip = request.form.get('ip')
        location_data = get_location(ip)

        if location_data:
            return render_template('ip_address_lookup.html', location_data=location_data, ip=ip)
        else:
            error_message = "IP address not found or an error occurred."
            return render_template('ip_address_lookup.html', error_message=error_message)
    
    return render_template('ip_address_lookup.html')



if __name__ == '__main__':
    app.run(debug=True)



