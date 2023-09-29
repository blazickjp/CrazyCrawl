import requests
from bs4 import BeautifulSoup
from robotexclusionrulesparser import RobotExclusionRulesParser
from urllib.parse import urljoin
import time


def fetch_robots_txt(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return None
    return response.text


def is_allowed(url, robots_parser):
    return robots_parser.is_allowed("*", url)


def parse(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = [urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True)]
    return links


def crawl(url, robots_parser):
    if not is_allowed(url, robots_parser):
        print(f"Not allowed to crawl {url}")
        return None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return None
    return response.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]
    return links


def main(start_url):
    robots_txt = fetch_robots_txt(start_url)
    robots_parser = RobotExclusionRulesParser()
    robots_parser.parse(robots_txt)

    visited = set()
    to_visit = [start_url]
    while to_visit:
        print(f"Queue size: {len(to_visit)}")

        current_url = to_visit.pop()
        if current_url in visited:
            continue
        print(f"Crawling {current_url}")
        visited.add(current_url)
        html = crawl(current_url, robots_parser)
        if html is None:
            continue
        links = parse(html)
        for link in links:
            # Ensure the URLs are absolute before extending the to_visit list
            abs_link = urljoin(current_url, link)
            to_visit.append(abs_link)
            print(f"Adding {abs_link} to the queue")
            time.sleep(1)  # Be polite and wait between requests


if __name__ == "__main__":
    main("http://books.toscrape.com/")
