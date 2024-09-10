import os
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


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


def write_urls_to_excel(urls, output_file, title):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = title

    # Write headers
    sheet["A1"] = title

    # Write URLs
    for row, url in enumerate(urls, start=2):
        sheet[f"A{row}"] = url

    workbook.save(output_file)


file_path = 'urls.txt'  # Update with the path to your file
output_directory = os.path.expanduser('~/Documents')  # Use the Documents directory
indexed_output_file = os.path.join(output_directory, 'indexed_urls.xlsx')
not_indexed_output_file = os.path.join(output_directory, 'not_indexed_urls.xlsx')

urls_to_check = read_urls_from_file(file_path)
indexed_urls = []
not_indexed_urls = []

for url in urls_to_check:
    if is_url_indexed(url):
        indexed_urls.append(url)
    else:
        not_indexed_urls.append(url)

write_urls_to_excel(indexed_urls, indexed_output_file, "Indexed URLs")
write_urls_to_excel(not_indexed_urls, not_indexed_output_file, "Not Indexed URLs")

print(f"Indexed URLs written to: {indexed_output_file}")
print(f"Not Indexed URLs written to: {not_indexed_output_file}")
