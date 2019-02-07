import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import os

page = requests.get('http://sejm.gov.pl/Sejm8.nsf/poslowie.xsp?type=A')
soup = BeautifulSoup(page.content, 'html.parser')

deputies = soup.select('.deputies li')
for deputy in deputies:
	deputy_name = deputy.find(class_='deputyName').string
	deputy_link = 'https://sejm.gov.pl%s' % deputy.find('a')['href']
	deputy_page = requests.get(deputy_link)

	deputy_soup = BeautifulSoup(deputy_page.content, 'html.parser')
	img = deputy_soup.find(id='view:_id1:_id2:facetMain:_id108:_id110')['src']

	os.system('mkdir "poslowie/%s"' % deputy_name)
	urllib.request.urlretrieve(img, 'poslowie/%s/pic.jpg' % deputy_name)
	print('downloaded')

