import requests
from bs4 import BeautifulSoup
import re
import urllib.request 
import os
from selenium import webdriver
import time
from tinydb import TinyDB

db = TinyDB('db.json')

driver = webdriver.Chrome('./chromedriver')

page = requests.get('http://sejm.gov.pl/Sejm8.nsf/poslowie.xsp?type=A')
soup = BeautifulSoup(page.content, 'html.parser')

deputies = soup.select('.deputies li')
for deputy in deputies:
	deputy_name = deputy.find(class_='deputyName').string
	deputy_club = deputy.find('strong').string
	deputy_link = 'https://sejm.gov.pl%s' % deputy.find('a')['href']

	driver.get(deputy_link)
	deputy_page_content = driver.page_source
	soup = BeautifulSoup(deputy_page_content, 'html.parser')

	deputy_data = soup.select('.partia .data')[0]
	deputy_data = deputy_data.find_all('li')
	lista = deputy_data[1].find_all('p')[1].string
	okreg_wyborczy = deputy_data[2].find_all('p')[1].string.replace('&nbsp;', ' ')
	liczba_glosow = int(deputy_data[3].find_all('p')[1].string)

	deputy_data = soup.select('.cv .data')[0]
	deputy_data = deputy_data.find_all('li')
	data_urodzenia, miejsce_urodzenia = "".join(deputy_data[0].find_all('p')[1].strings).split(',')
	miejsce_urodzenia = miejsce_urodzenia.strip()
	wyksztalcenie = deputy_data[1].find_all('p')[1].string
	ukonczona_szkola = deputy_data[2].find_all('p')[1].string
	zawod = deputy_data[3].find_all('p')[1].string

	while True:
		try:
			driver.get(deputy_link)
			button = driver.find_element_by_id('wystapienia')
			button.click()
			time.sleep(0.5)
			osw = driver.find_element_by_xpath("//a[@id='wystapienia']/following-sibling::div")
			sejm_soup = BeautifulSoup(osw.get_attribute('innerHTML'), 'html.parser')
			wystapienia = "".join(sejm_soup.find(class_='left').strings)
			print('RAW:', wystapienia)
			try:
				wystapienia = int(wystapienia.replace(' Wypowiedzi łącznie:\xa0  ', '').strip().split('     ')[0])
			except:
				try:
					wystapienia = int(wystapienia.replace(' Wypowiedzi:   ', ''))
				except:
					wystapienia = '-'
			print(wystapienia)
			break
		except:
			pass

	while True:
		try:
			driver.get(deputy_link)
			button = driver.find_element_by_id('glosowania')
			button.click()
			time.sleep(0.5)
			glosowania = driver.find_element_by_xpath("//a[@id='glosowania']/following-sibling::div")
			sejm_soup = BeautifulSoup(glosowania.get_attribute('innerHTML'), 'html.parser')
			glosowania = sejm_soup.find_all(class_='left')[0].string.replace('Udział w głosowaniach: ', '')
			print(glosowania)
			break
		except:
			pass

	while True:
		try:
			driver.get(deputy_link)
			button = driver.find_element_by_id('osw')
			button.click()
			time.sleep(0.5)
			osw = driver.find_element_by_xpath("//a[@id='osw']/following-sibling::div")
			sejm_soup = BeautifulSoup(osw.get_attribute('innerHTML'), 'html.parser')
			osw = sejm_soup.find_all('tr')[-1].find('a')['href']
			print(osw)
			break
		except:
			pass

	while True:
		try:
			driver.get(deputy_link)
			button = driver.find_element_by_id('view:_id1:_id2:facetMain:_id189:_id276')
			button.click()
			time.sleep(0.5)
			email = driver.find_element_by_xpath("//a[@id='view:_id1:_id2:facetMain:_id189:_id276']")
			sejm_soup = BeautifulSoup(email.get_attribute('innerHTML'), 'html.parser')
			email = sejm_soup
			print(email)
			break
		except:
			pass


	db.insert(
		{
			'imie': deputy_name,
			'klub': deputy_club,
			'link': deputy_link,
			'lista': lista,
			'okreg_wyborczy': okreg_wyborczy,
			'liczba_glosow': liczba_glosow,
			'wystapienia': wystapienia,
			'glosowania': glosowania,
			'data_urodzenia': data_urodzenia,
			'miejsce_urodzenia': miejsce_urodzenia,
			'wyksztalcenie': wyksztalcenie,
			'ukonczona_szkola': ukonczona_szkola,
			'zawod': zawod,
			'osw': osw,
			'email': str(email)
		})
	print('--------------------')