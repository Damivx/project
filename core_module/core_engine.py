from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from input_module import get_input
from crawler import Crawler
from fuzzer import Fuzzer
from logger import Logger

def start_proxy(url):
    # Configure proxy
    opts = options.Options(listen_host='127.0.0.1', listen_port=8080)
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(None)
    m.server = proxy.server.ProxyServer(pconf)

    # Start crawling
    crawler = Crawler(url)
    endpoints = crawler.crawl()

    # Start fuzzing
    fuzzer = Fuzzer(endpoints)
    fuzzer.start_fuzzing()

    # Logging
    logger = Logger("scan_results.txt")
    logger.log(f"Scanning {url} for vulnerabilities")

    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()

# Example usage
if __name__ == "__main__":
    url = get_input()
    start_proxy(url)

    Crawler Module (crawler.py)

python

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()

    def crawl(self):
        endpoints = []
        self._crawl(self.base_url, endpoints)
        return endpoints

    def _crawl(self, url, endpoints):
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/'):
                href = urljoin(self.base_url, href)
            if href and self.base_url in href:
                endpoints.append(href)
                self._crawl(href, endpoints)

# Example usage
if __name__ == "__main__":
    crawler = Crawler("http://example.com")
    endpoints = crawler.crawl()
    print("Discovered endpoints:", endpoints)

    Fuzzer Module (fuzzer.py)

python

import requests

class Fuzzer:
    def __init__(self, endpoints):
        self.endpoints = endpoints
        self.payloads = ["<script>alert(1)</script>", "' OR '1'='1"]

    def start_fuzzing(self):
        for endpoint in self.endpoints:
            for payload in self.payloads:
                self._fuzz(endpoint, payload)

    def _fuzz(self, endpoint, payload):
        response = requests.get(endpoint + payload)
        if payload in response.text:
            print(f"Potential vulnerability found at {endpoint}")

# Example usage
if __name__ == "__main__":
    fuzzer = Fuzzer(["http://example.com/search?q="])
    fuzzer.start_fuzzing()

