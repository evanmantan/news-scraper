from bs4 import BeautifulSoup
import requests
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

url = "https://www.tribunnews.com/nasional/2013/07/01/ditanya-dugaan-keterlibatan-setya-novanto-ical-pasrah-putusan-hukum"
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

table = []
row = []

news_title = soup.find("h1").get_text()
news_datetime = soup.find("time").get_text()  # access news creation date and time
news_author = (
    soup.find("div", id="penulis").get_text().strip().removeprefix("Penulis:").lstrip()
)  # access news author name
article_body = soup.find("div", "txt-article")  # access news content tags
if article_body.p.strong.get_text() == article_body.p.get_text():
    news_location = (
        article_body.p.next_sibling.strong.get_text()
    )  # access news creation location
else:
    news_location = article_body.p.strong.get_text()


def no_class_and_id(tag):
    return tag.name == "p" and not tag.has_attr("class") and not tag.has_attr("id")


paragraphs = soup.find_all(no_class_and_id)

new_paragraphs = []
for p in paragraphs:
    if p.text != "" and p.text.rstrip() != "":
        p_stripped = p.text.strip()
        new_paragraphs.append(p_stripped)

# for i in range(3):
#     new_paragraphs.pop()  # remove watermarks

new_paragraphs[0] = new_paragraphs[0].removeprefix(news_location).lstrip(" -")
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
        "Tribunnews.com",
    ]
)
print(row)
