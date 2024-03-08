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

            news_title = soup.find("h1").text
            details = soup.find("div", "namerep")
            news_author = details.a.text  # access news author name
            news_datetime = details.b.text  # access news creation date and time
            article_body = soup.find(
                "div", itemprop="articleBody"
            )  # access news content tags
            article_body = article_body.p.strong
            news_location = ""
            while news_location == "":
                news_location = article_body.text  # access news creation location
                article_body = article_body.next_sibling

            def no_class_and_id(tag):
                return (
                    tag.name == "p"
                    and not tag.has_attr("class")
                    and not tag.has_attr("id")
                )

            paragraphs = soup.find_all(no_class_and_id)

            new_paragraphs = []
            for p in paragraphs:
                if p.text != "" and p.text.rstrip() != "":
                    p_stripped = p.text.strip()
                    new_paragraphs.append(p_stripped)

            for i in range(3):
                new_paragraphs.pop()  # remove watermarks

            new_paragraphs[0] = (
                new_paragraphs[0].removeprefix(news_location).lstrip(" -")
            )
            news_text = " ".join(new_paragraphs)

            news_year = news_datetime.split()[3]

            row.extend(
                [
                    news_title,
                    news_text,
                    news_author,
                    news_datetime,
                    news_year,
                    news_location,
                    url,
                    "Okezone.com",
                ]
            )

            table.append(row)
    return table


# setnov_table = scrape_sites("setnov.txt")
# print(setnov_table)

# with open("setnov.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(setnov_table)

fahri_table = scrape_sites("fahri.txt")
print(fahri_table)

with open("fahri.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(fahri_table)