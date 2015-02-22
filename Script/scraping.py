import json
import urllib
import csv

#San Francisco coordinates: 37.820497,-122.306156,37.676076,-122.611713
#-122393231,37537874,-122303109,37578562

DEBUG = 0
LO = 2
LAT = 1
ZID = 0
PRICE = 3
#longitude
lo_MIN = -122611713
lo_MAX = -122306156
lo_SCALE = 200
lo_BIAS = 100
lo_RANGE = lo_MAX - lo_MIN
#latitude
lat_MIN = 37676076
lat_MAX = 37820497
lat_RANGE = lat_MAX - lat_MIN
lat_SCALE = 200
lat_BIAS = 100
#price
price_SCALE = 10
price_list = []
i = 0


url = 'http://www.zillow.com/search/GetResults.htm?spt=homes&status=110001&lt=111101&ht=111111&pr=,&mp=,&bd=0,&ba=0,&sf=,&lot=,&yr=,&pho=0&pets=0&parking=0&laundry=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=1&pf=1&zoom=13&rect=-122611713,37676076,-122306156,37820497&p=1&sort=pricea&search=maplist&disp=1&listright=true&isMapSearch=true&zoom=13'

page = urllib.urlopen(url)
content = page.read()

data = json.loads(content)


with open('data.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL) 
#print data['map']['properties'][0]
	highest_price = 0.0
	price = 0.0

	#Get highest price
	for item in data['map']['properties']:
		if DEBUG:
			print item
		if 'M' in item[PRICE]:
			price = float(item[PRICE][item[PRICE].index('$')+1:item[PRICE].index('M')]) * 1000000
		elif 'K' in item[PRICE]:
			price = float(item[PRICE][item[PRICE].index('$')+1:item[PRICE].index('K')]) * 1000	
		price_list.append(price)		
		if price > highest_price:
			highest_price = price

	#price_RANGE = highest_price

	#Get all normalized numbers
	for item in data['map']['properties']:
		i = data['map']['properties'].index(item)
		price_n = price_list[i] * price_SCALE/highest_price
		lo_n = (item[LO]-lo_MIN) * lo_SCALE/lo_RANGE - lo_BIAS
		lat_n = (item[LAT]-lat_MIN) * lat_SCALE/lat_RANGE - lat_BIAS
		writer.writerow([lo_n, lat_n, price_n, item[LO], item[LAT], item[PRICE], item[ZID]])

if DEBUG:
	print highest_price
#[longitude_n, latitude_n, price_n, longitude, latitude, price, id]
