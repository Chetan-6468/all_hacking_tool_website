from flask import Blueprint, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  



xss_page = Blueprint('xss', __name__, static_folder='static', template_folder='templates')



# Function to check for XSS vulnerability
def check_xss(url):
    try:
        # Initialize Chrome WebDriver
        service = Service('chromedriver.exe')  # Provide the path to your chromedriver executable
        driver = webdriver.Chrome(service=service)

        # Open the web page
        driver.get(url)

        # List of XSS payloads to test
        xss_payloads = [
            '<script>alert("XSS");</script>',
            '<img src="x" onerror="alert(\'XSS\');">',
            '"><script>alert("XSS");</script>',
            '<svg/onload=alert(\'XSS\')>',
            '<iframe src="javascript:alert(\'XSS\');" />'
            # Add more payloads as needed
        ]

        results = []

        for payload in xss_payloads:
            try:
                # Use JavaScript to inject the payload into the input field
                driver.execute_script('''
                    var input = document.querySelector('input[type="text"]');
                    input.value = arguments[0];
                ''', payload)

                # Pause for a moment to allow the payload to take effect in the browser (adjust the delay as needed)
                time.sleep(1)  # Adjust the delay (in seconds) as needed

                # Submit the form if available (some websites may not have a form)
                form = driver.find_element(By.TAG_NAME, 'form')
                form.submit()

                # Check if the alert dialog appears (indicating XSS vulnerability)
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert_text = alert.text
                alert.accept()

                if alert_text:
                    results.append("The website has an XSS vulnerability with payload: " + payload)
                else:
                    results.append("No alert for payload: " + payload)
            except Exception as e:
                # If no alert is triggered, continue to the next payload
                continue

            # Reload the page for the next payload
            driver.get(url)

        # Close the browser
        driver.quit()

        if results:
            return "\n".join(results)
        else:
            return "The website is safe from known XSS payloads"
    except Exception as e:
        return str(e)


@xss_page.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if request.method == 'POST':
        url = request.form['url']
        result = check_xss(url)
        return jsonify({'result': result})
    return render_template('scanner.html')


