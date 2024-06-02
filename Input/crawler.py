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

