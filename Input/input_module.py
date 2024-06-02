import argparse
import re
from urllib.parse import urlparse

def validate_url(url):
    pattern = re.compile(
        r'^(?:http|https)://'  # http:// or https://
        r'(?:\S+(?::\S*)?@)?'  # optional user:password@
        r'(?:[a-zA-Z0-9.-]+|\[?[a-fA-F0-9:]+\]?)'  # domain or IPv4/IPv6
        r'(?::\d{2,5})?'  # optional port
        r'(?:[/?#]\S*)?$'  # resource path
    )
    return re.match(pattern, url) is not None

def get_input():
    parser = argparse.ArgumentParser(description='Vulnerability Analysis Tool')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    args = parser.parse_args()
    url = args.url

    if validate_url(url):
        return url
    else:
        raise ValueError("Invalid URL format")

# Example usage
if __name__ == "__main__":
    url = get_input()
    print("Valid URL:", url)

