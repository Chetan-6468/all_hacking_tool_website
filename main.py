from flask import Blueprint, render_template, request
import subprocess
import dns.resolver
import concurrent.futures

main_page = Blueprint('main', __name__, static_folder='static', template_folder='templates')

def resolve_subdomain(subdomain, dns_server):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]
        answers = resolver.query(subdomain, "A")
        ip_addresses = [str(answer) for answer in answers]
        return ip_addresses
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return ["Not Found"]
    except Exception as e:
        return [str(e)]

def resolve_subdomains(subdomains, dns_server):
    subdomain_info = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_subdomain = {executor.submit(resolve_subdomain, subdomain, dns_server): subdomain for subdomain in subdomains}

        for future in concurrent.futures.as_completed(future_to_subdomain):
            subdomain = future_to_subdomain[future]
            try:
                ip_addresses = future.result()
                subdomain_info.append((subdomain, ip_addresses))
            except Exception as e:
                subdomain_info.append((subdomain, [str(e)]))

    return subdomain_info

def find_subdomains(domain):
    subdomains = []

    try:
        # Perform subdomain discovery using sublist3r
        cmd = f'sublist3r -d {domain} -o /tmp/sublist3r_output.txt'
        subprocess.run(cmd, shell=True, check=True)
        with open('/tmp/sublist3r_output.txt', 'r') as file:
            subdomains = file.read().split('\n')

        # Resolve IP addresses for each subdomain in parallel
        dns_server = '8.8.8.8'  # Use a DNS server of your choice
        subdomain_info = resolve_subdomains(subdomains, dns_server)

        return subdomain_info

    except Exception as e:
        return [(f"Error: {str(e)}", ["Not Found"])]

@main_page.route('/subdomain', methods=['GET', 'POST'])
def subdomain():
    subdomains_info = []
    error_message = None

    if request.method == 'POST':
        domain = request.form['domain']
        if domain:
            subdomains_info = find_subdomains(domain)
            if not subdomains_info:
                error_message = f"No subdomains found for '{domain}'"

    return render_template('subdomain.html', subdomains_info=subdomains_info, error_message=error_message)
