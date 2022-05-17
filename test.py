import requests
from bs4 import BeautifulSoup

html = requests.get("https://turicum.fit/de/blog")

soup = BeautifulSoup(html.text, 'html.parser')

for i, elem in enumerate(soup.find("div", class_="workout-of-the-day").children):
	print(elem)
	print("NEW ELEM", i)

#print(soup.prettify())