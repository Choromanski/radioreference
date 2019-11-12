from bs4 import BeautifulSoup
import requests, csv

BASE_URL = "https://www.radioreference.com/apps/db/?action=searchZip&from=db&zip="

#zip = int(input("Enter your zip code: "))

zip = 18976

page_response = requests.get(BASE_URL + str(zip))

soup = BeautifulSoup(page_response.content, "html.parser").find("div", {"id": "editarea"})

titles = soup.findAll("div", {"class": "title"})
titleboxes = soup.findAll("div", {"class": "titlebox"})

for i in range(0, len(titleboxes)):
	print(i)
	print(titles[i].text)
	tables = titleboxes[i].findAll("table")
	output_rows = []
	for table in tables:
		for table_row in table.findAll('tr'):
			columns = table_row.findAll('td')
			output_row = []
			for column in columns:
				output_row.append(column.text.replace(u'\xa0', u' '))
			if len(output_row) > 0:
				output_rows.append(output_row)
		for j in output_rows:
			print(j)

#print(len(titles))
#print(len(titleboxes))
#print(titleboxes[0])
#print(soup)

#location: