import json
import requests
from bs4 import BeautifulSoup

url: str = "https://quotes.toscrape.com"


headers: dict = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}

def get_quotes(url: str):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(res.text, "html.parser")

        # proses scraping
        contents = soup.find_all("div", attrs={"class": "quote"})
        quotes_list: list = []
        for content in contents:
            quote = content.find("span", attrs={"class": "text"}).text.strip()
            author = content.find("small", attrs={"class": "author"}).text.strip()

            # NGAMBIL URL DETAIL
            author_detail = content.find("a")['href']


            data_dict: dict = {
                "quote": quote,
                "quotes by": author,
                "author detail": url + author_detail,
            }
            quotes_list.append(data_dict)

        # proses pengolahan data
        with open("quotes.json", "w+") as f:
            json.dump(quotes_list, f)

        print("Data Berhasil di Generate")


def get_detail(detail_url: str):
    res = requests.get(detail_url, headers=headers)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")

        # proses scraping
        author_title = soup.find("h3", attrs={"class":"author-title"}).text.strip()
        born = soup.find("span", attrs={"class":"author-born-date"}).text.strip()
        location = soup.find("span", attrs={"class":"author-born-location"}).text.strip()
        description = soup.find("div",attrs={"class": "author-description"}).text.strip()

        # proses mapping
        data_dict = {
            "author": author_title,
            "born": born,
            "born location": location,
            "description": description,
        }

        print(data_dict)

        return data_dict


if __name__ == "__main__":
    get_detail("https://quotes.toscrape.com/author/Thomas-A-Edison")