from bs4 import BeautifulSoup
import requests, csv

BASE_URL = "https://www.radioreference.com/apps/db/?action=searchZip&from=db&zip="
try:
	zip = int(input("Enter your zip code: "))
except ValueError:
	print("Please enter a valid 5 digit zip code")
	exit()

page_response = requests.get(BASE_URL + str(zip))

soup = BeautifulSoup(page_response.content, "html.parser").find("div", {"id": "editarea"})

try:
	titles = soup.findAll("div", {"class": "title"})
except AttributeError:
	print("Please enter a valid 5 digit zip code")
	exit()

titleboxes = soup.findAll("div", {"class": "titlebox"})

with open(str(zip) + '.csv', 'w+', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(['Agency', 'Group', 'Frequency', 'License', 'Type', 'Tone', 'Alpha Tag', 'Description', 'Mode', 'Tag'])
	for i in range(0, len(titleboxes)):
		tables = titleboxes[i].findAll("table")
		aTitles = titleboxes[i].findAll("a", {'name': lambda L: L and L.startswith('scid-')})
		t = 0
		for table in range(0, len(tables)):
			output_rows = []
			for table_row in tables[table].findAll('tr'):
				columns = table_row.findAll('td')
				output_row = [titles[i].text, aTitles[t].text]
				for column in columns:
					output_row.append(column.text.replace(u'\xa0', u' ').rstrip())
				if len(output_row) > 4:
					output_rows.append(output_row)
			if len(output_rows) > 0:
				t += 1
				writer.writerows(output_rows)

print(str(zip) + ".csv created.")