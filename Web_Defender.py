import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def scan_form():
    if request.method == 'POST':
        url = request.form['url']
        vulnerabilities = scan_vulnerabilities(url)
        return render_template('results.html', url=url, vulnerabilities=vulnerabilities)
    return render_template('scan_form.html')

def scan_vulnerabilities(url):
    # Make a GET request to the given URL
    response = requests.get(url)

    # Check for cross-site scripting (XSS) vulnerabilities
    if '<script>' in response.text or '</script>' in response.text:
        print("XSS vulnerability found in the URL:", url)

    # Check for SQL injection vulnerabilities
    if 'select' in response.text.lower() or 'insert' in response.text.lower() or 'update' in response.text.lower() or 'delete' in response.text.lower():
        print("SQL injection vulnerability found in the URL:", url)

    # Check for weak authentication vulnerabilities
    if 'login' in url.lower() or 'admin' in url.lower():
        if 'Authorization' not in response.headers and 'Set-Cookie' not in response.headers:
            print("Weak authentication vulnerability found in the URL:", url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check for weak password policies
    if 'password' in soup.get_text().lower():
        print("Weak password policy found in the URL:", url)

    # Check for clickjacking vulnerabilities
    if 'X-Frame-Options' not in response.headers:
        print("Clickjacking vulnerability found in the URL:", url)

    # Check for missing security headers
    security_headers = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Content-Type-Options', 'X-Frame-Options', 'X-XSS-Protection']
    for header in security_headers:
        if header not in response.headers:
            print(f"Missing security header: {header} in the URL:", url)
if __name__ == '__main__':
    app.run()
# Example usage
url = 'https://example.com'
scan_vulnerabilities(url)
