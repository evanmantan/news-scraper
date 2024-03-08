from bs4 import BeautifulSoup
import requests
import csv


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def scrape_sites(url_list):
    table = []
    with open(url_list) as f:
        for url in f:
            print(url)
            url = url.rstrip()
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            row = []

            news_title = soup.find("h1").get_text().strip()
            news_datetime = soup.find(
                "div", "detail__date"
            ).get_text()  # access news creation date and time
            article_body = soup.find(
                "div", "detail__body-text"
            )  # access news content tags
            news_location = article_body.strong.get_text()

            def no_class_and_id(tag):
                return (
                    tag.name == "p"
                    and not tag.has_attr("class")
                    and not tag.has_attr("id")
                )

            paragraphs = article_body.contents

            new_paragraphs = []
            for p in paragraphs:
                if p.text != "" and p.text.rstrip() != "" and not p.text.strip() == "SCROLL TO RESUME CONTENT":
                    p_stripped = p.text.strip()
                    new_paragraphs.append(p_stripped)

            for i in range(3):
                new_paragraphs.pop()  # remove watermarks

            news_text = " ".join(new_paragraphs)
            news_text = news_text.removeprefix(news_location).lstrip(" -")

            news_year = news_datetime.split()[3]

            row.extend(
                [
                    news_title,
                    news_text,
                    "unknown",
                    news_datetime,
                    news_year,
                    news_location,
                    url,
                    "Detik.com",
                ]
            )
            table.append(row)
    return table


setnov_table = scrape_sites("setnov.txt")
# print(setnov_table)

with open("setnov.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(setnov_table)

fahri_table = scrape_sites("fahri.txt")
# print(fahri_table)

with open("fahri.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(fahri_table)
