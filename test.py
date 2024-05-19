import requests
from bs4 import BeautifulSoup 

head = {"User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.0; +https://openai.com/gptbot)"}
r = requests.get('https://detail.tmall.hk/hk/item.htm?abbucket=8&id=615143308376&ns=1&priceTId=2147826717161118969284040e7731',
                 headers=head)

html_doc = r.text

with open("response.html", "w", encoding="utf-8") as file:
    file.write(html_doc)

soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())

print(soup.title)

# print(r)
# print(r.text)
