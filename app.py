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

# from xss import xss

app = Flask(__name__)
# app.register_blueprint(xss)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/scanner')
def scanner():
    return render_template('scanner.html')


@app.route('/passwordGen')
def passwordGen():
    return render_template('passwordGen.html')

# # Function to check for XSS vulnerability
# def check_xss(url):
#     try:
#         # Initialize Chrome WebDriver
#         service = Service('chromedriver.exe')  # Provide the path to your chromedriver executable
#         driver = webdriver.Chrome(service=service)

#         # Open the web page
#         driver.get(url)

#         # Find a form element and inject an XSS payload
#         form = driver.find_element(By.TAG_NAME, 'form')
#         input_field = form.find_element(By.TAG_NAME, 'input')
#         input_field.send_keys('<script>alert("XSS");</script>')

#         # Submit the form
#         form.submit()

#         # Check if the alert dialog appears (indicating XSS vulnerability)
#         alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
#         alert_text = alert.text
#         alert.accept()

#         # Close the browser
#         driver.quit()

#         return "The website has an XSS vulnerability" if alert_text else "The website is safe"
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

@app.route('/port_scanning', methods=['GET', 'POST'])
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


