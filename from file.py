import requests
from bs4 import BeautifulSoup

def is_url_indexed(url):
    query = f"site:{url}"
    google_search_url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(google_search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find_all("div", class_="g")
        for result in search_results:
            link = result.find("a", href=True)
            if link and link['href'].startswith(url):
                return True
    return False

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

file_path = 'urls.txt'  # Update with the path to your file
urls_to_check = read_urls_from_file(file_path)

for url in urls_to_check:
    indexed = is_url_indexed(url)
    if indexed:
        print(f"The URL {url} is indexed on Google.")
    else:
        print(f"The URL {url} is not indexed on Google.")
