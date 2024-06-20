import requests
from bs4 import BeautifulSoup
url = "https://supertails.com/search?q=Pedigree&page=1"
r = requests.get(url)
# print(r.text)
soup = BeautifulSoup(r.text,'html.parser')
# print(soup.title.text)
# boxes = soup.findAll('div',class_='findify-components--cards--product__content')
# print(boxes)

all_results = soup.find_all("li",class_="findify-components-common--grid findify-components-common--grid__column-3 product-item")

for result in all_results:
    item ={}
    
    item['Title'] = all_results.find("h2", class_="findify-components--text findify-components--cards--product__title")
    item['Price'] = all_results.find("div", class_="findify-components--cards--product--price__price findify-components--cards--product--price__sale-price")
    print(item['Price'])