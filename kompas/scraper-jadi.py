from bs4 import BeautifulSoup
import requests
import csv


def scrape_sites(url_list):
    table = []
    with open(url_list) as f:
        for url in f:
            print(url)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")

            row = []

            news_title = soup.find("h1").get_text()
            news_author = (
                soup.find("div", "read__credit__item", id="penulis")
                .get_text()
                .removeprefix("Penulis")
                .strip()
            )  # access news author name
            news_datetime = (
                soup.find("div", "read__time")
                .get_text()
                .removeprefix("Kompas.com -")
                .strip()
            )  # access news creation date and time

            news_year = news_datetime[6:10]

            row.extend(
                [
                    news_title,
                    "",
                    news_author,
                    news_datetime,
                    news_year,
                    "",
                    url,
                    "Kompas.com",
                ]
            )
            table.append(row)
    return table


setnov_table = scrape_sites("setnov.txt")
# print(setnov_table)

with open("setnov.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(setnov_table)

# fahri_table = scrape_sites("fahri.txt")
# # print(fahri_table)

# with open("fahri.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(fahri_table)
