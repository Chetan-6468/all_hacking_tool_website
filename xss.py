# from flask import Blueprint, request, jsonify, render_template
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# xss = Blueprint('xss', __name__)

# MALICIOUS_SCRIPT = '<script>alert("xss")</script>'

# @xss.route('/scanner')
# def scanner():
#     return render_template('scanner.html')


# @xss.route('/scan', methods=['GET'])
# def scan():
#     url = request.args.get('url')
#     has_xss = check_xss(url)
#     return jsonify(has_xss)

# def check_xss(url):
#     chrome_options = Options()
#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         driver.get(url)
        
#         # Inject malicious script into input fields or forms
#         # Trigger actions to execute the script
        
#         # Check if the script executed and update 'has_xss' accordingly
#         has_xss = False
        
#         driver.quit()
#         return has_xss
#     except Exception as e:


#         driver.quit()
#         return str(e)
