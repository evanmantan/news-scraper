from bs4 import BeautifulSoup
import requests
import re
import csv

filler_lists = [
    "Segera lengkapi data dirimu untuk ikutan program #JernihBerkomentar.",
    "Tulis komentarmu dengan tagar #JernihBerkomentar dan menangkan e-voucher untuk 90 pemenang!",
    "Periksa kembali dan lengkapi data dirimu.",
    "Data dirimu akan digunakan untuk verifikasi akun ketika kamu membutuhkan bantuan atau ketika ditemukan aktivitas tidak biasa pada akunmu.",
]

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
                soup.find("div", "read__time").get_text().removeprefix("Kompas.com -").strip()
            )  # access news creation date and time

            article_body = soup.find("div", "read__content")  # access news content tags
            # news_location = article_body.strong.get_text()


            def no_class_and_id(tag):
                return tag.name == "p" and not tag.has_attr("class") and not tag.has_attr("id")


            paragraphs = soup.find_all(no_class_and_id)
            new_paragraphs = []

            for p in paragraphs:
                if p.text != "" and p.text.rstrip() != "" and not p.text.strip() in filler_lists:
                    p_stripped = p.text.strip()
                    p_stripped = re.sub(r"\n.*", "", p_stripped)
                    new_paragraphs.append(p_stripped)


            tmp = new_paragraphs[0].split()
            news_location = tmp.pop(0)
            new_paragraphs[0] = " ".join(tmp)
            new_paragraphs[0] = re.sub(r".*KOMPAS\.com", "", new_paragraphs[0])
            new_paragraphs[0] = new_paragraphs[0].lstrip(" —-")
            news_text = " ".join(new_paragraphs)
            news_text = news_text.replace("  \t", "")
            news_year = news_datetime[6:10]

            row.extend(
                [
                    news_title,
                    news_text,
                    news_author,
                    news_datetime,
                    news_year,
                    news_location,
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

fahri_table = scrape_sites("fahri.txt")
# print(fahri_table)

with open("fahri.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(fahri_table)

