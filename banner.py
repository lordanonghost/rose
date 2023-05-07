import argparse
import socket
import subprocess
import urllib.request
import whois

def print_banner():
    print("*" * 50)
    print("Web Scanner")
    print("*" * 50)
    print()

def print_help():
    print_banner()
    print("Usage:")
    print("web_scanner.py -u <url> [--whois] [--traceroute] [--index]")
    print()
    print("Options:")
    print("-h, --help\tShow this help message")
    print("-u, --url\tSpecify the URL to scan")
    print("--whois\t\tPerform a WHOIS lookup on the URL's domain")
    print("--traceroute\tPerform a traceroute on the URL's IP address")
    print("--index\t\tCheck if an index.html file exists on the web server")
    print()

def get_ip_address(url):
    try:
        ip_address = socket.gethostbyname(url)
        return ip_address
    except socket.gaierror:
        print("Error: Could not resolve URL to IP address")
        return None

def print_whois_info(url):
    domain = url.split("//")[-1].split("/")[0]
    whois_info = whois.whois(domain)
    print("WHOIS Information:")
    print(f"Domain Name: {whois_info.domain_name}")
    print(f"Registrar: {whois_info.registrar}")
    print(f"Registrant Name: {whois_info.name}")
    print(f"Registrant Email: {whois_info.email}")
    print(f"Creation Date: {whois_info.creation_date}")
    print(f"Expiration Date: {whois_info.expiration_date}")
    print()

def print_traceroute(ip_address):
    print("Traceroute Information:")
    traceroute_output = subprocess.check_output(["traceroute", ip_address])
    print(traceroute_output.decode("utf-8"))
    print()

def check_index(url):
    index_url = url + "/index.html"
    try:
        urllib.request.urlopen(index_url)
        print("Index.html found!")
    except urllib.error.HTTPError:
        print("Index.html not found.")
    print()

def main():
    parser = argparse.ArgumentParser(description="Web Scanner")
    parser.add_argument("-u", "--url", required=True, help="Specify the URL to scan")
    parser.add_argument("--whois", action="store_true", help="Perform a WHOIS lookup on the URL's domain")
    parser.add_argument("--traceroute", action="store_true", help="Perform a traceroute on the URL's IP address")
    parser.add_argument("--index", action="store_true", help="Check if an index.html file exists on the web server")
    args = parser.parse_args()

    print_banner()

    url = args.url
    ip_address = get_ip_address(url)

    if ip_address:
        print(f"IP Address: {ip_address}")
        print()

        if args.whois:
            print_whois_info(url)

        if args.traceroute:
            print_traceroute(ip_address)

        if args.index:
            check_index(url)
# main function
if __name__ == "__main__":
    main()
