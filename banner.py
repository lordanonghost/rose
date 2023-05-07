
import argparse
import requests
import re
import urllib.parse

def main():
    parser = argparse.ArgumentParser(description='Website information scanner')
    parser.add_argument('url', metavar='url', type=str, help='URL of the website')
    parser.add_argument('--headers', action='store_true', help='Display response headers')
    parser.add_argument('--cookies', action='store_true', help='Display response cookies')
    parser.add_argument('--links', action='store_true', help='Display links')
    parser.add_argument('--emails', action='store_true', help='Display email addresses')
    parser.add_argument('--phone', action='store_true', help='Display phone numbers')
    parser.add_argument('--ip', action='store_true', help='Display IP addresses')
    args = parser.parse_args()

    url = args.url

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    print(f"Status code: {response.status_code}")
    if args.headers:
        print(f"Response headers: {response.headers}")
    if args.cookies:
        print(f"Response cookies: {response.cookies}")
    if args.links:
        links = get_links(response.content, url)
        print(f"Links: {links}")
    if args.emails:
        emails = get_emails(response.content)
        print(f"Email addresses: {emails}")
    if args.phone:
        phone_numbers = get_phone_numbers(response.content)
        print(f"Phone numbers: {phone_numbers}")
    if args.ip:
        ip_addresses = get_ip_addresses(response.content)
        print(f"IP addresses: {ip_addresses}")

def get_links(content, base_url):
    links = []
    for link in re.findall(r'href=[\'"]?([^\'" >]+)', content.decode()):
        absolute_link = urllib.parse.urljoin(base_url, link)
        links.append(absolute_link)
    return links

def get_emails(content):
    emails = set()
    for email in re.findall(r'[\w\.-]+@[\w\.-]+', content.decode()):
        emails.add(email)
    return list(emails)

def get_phone_numbers(content):
    phone_numbers = set()
    for phone_number in re.findall(r'\+?\d[\d -]{8,12}\d', content.decode()):
        phone_numbers.add(phone_number)
    return list(phone_numbers)

def get_ip_addresses(content):
    ip_addresses = set()
    for ip_address in re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', content.decode()):
        ip_addresses.add(ip_address)
    return list(ip_addresses)
# main function
if __name__ == '__main__':
    main()
