import requests 
import lxml
from bs4 import BeautifulSoup as Bsoup 

main_url = 'https://www.carwale.com'
response = requests.get(main_url).text
bs_object = Bsoup(response, 'lxml')
brand_list = []

while True:
	brands = bs_object.find(class_='brand-type-container')
	brand_selector = brands
	brands = brands.find_all('li')
	for i, brand in enumerate(brands):
		print(i,brand.text)
		brand_list.append(brand)
	select_brand = int(input('Select automaker index'))
	brand_webpage = main_url + brand_list[select_brand].a['href']
	brand_webpage_response = requests.get(brand_webpage).text
	brand_webpage_soup_object = Bsoup(brand_webpage_response, 'lxml')
	car_list = brand_webpage_soup_object.find('ul', id = 'divModels')
	all_car_list = car_list.find_all('li')
	print('\n')
	for i, each_car in enumerate(all_car_list):
		if each_car.find_all('div')[1].a.text == '':
			pass
		else:
			print(i, each_car.find_all('div')[1].a.text)
	car_name = int(input('Select car index from above: '))
	car_reviews = brand_webpage + all_car_list[car_name].a['href'] + 'userreviews/'
	car_reviews_page = requests.get(car_reviews)
	print(car_reviews_page.status_code)

	print('\n\n')



