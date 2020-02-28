import requests 
import lxml
from bs4 import BeautifulSoup as Bsoup 
from fake_useragent import UserAgent
import time
import Sentimental_Analysis
from matplotlib import pyplot as plt

#Fetching html of main page as well as creating a list that will be filled with automaker names along with indexes for user control
main_url = 'https://www.carwale.com'
response = requests.get(main_url).text
bs_object = Bsoup(response, 'lxml')
brand_list = []
ua = UserAgent()
sentiments_user_reviews = []

#Creating a loop to retrieve reviews of multiple automakers
while True:

#Finding all the automakers enlisted on Carwale
	automakers = bs_object.find(class_='brand-type-container')
	automaker_selector = automakers
	automakers = automakers.find_all('li')
	for i, automaker in enumerate(automakers):
		print(i,automaker.text)
		brand_list.append(automaker)

#Allowing user to choose from the enlisted automakers & fetching car models enlisted by the automaker
	select_automaker = int(input('Select automaker index'))
	automaker_webpage = main_url + brand_list[select_automaker].a['href']
	automaker_webpage_response = requests.get(automaker_webpage).text
	automaker_webpage_soup_object = Bsoup(automaker_webpage_response, 'lxml')
	car_list = automaker_webpage_soup_object.find('ul', id = 'divModels')
	all_car_list = car_list.find_all('li')
	print('')
	for i, each_car in enumerate(automaker_webpage_soup_object.find_all('strong', class_ = 'text-unbold')):
		print(i, each_car.text)
	print('')

#Directing to the page of the selected car model and retrieving the url of the page its user reviews
	car_name = int(input('Select car index from above: '))
	car_reviews = main_url + all_car_list[car_name].a['href'] + 'userreviews/'

#Scraping incomplete reviews on the main page of user reviews. For complete review, each review url has to be fetched and the page scraped
	car_reviews_page = requests.get(car_reviews, headers = {'user-agent':ua.chrome})
	car_reviews_page = Bsoup(car_reviews_page.text, 'lxml')
	all_reviews = car_reviews_page.find('ul', id = 'userReviewListing')
	all_reviews = all_reviews.find_all('li')
	for review in all_reviews:
		review_page = main_url + review.a['href']
		review_page_response = requests.get(review_page).text
		review_page_soup_object = Bsoup(review_page_response, 'lxml')
		review = review_page_soup_object.find('div', attrs = {'categoryname':'userreviews'})
		print(review.find_all('div', class_ = 'mid-box margin-top20')[3].text)
		user_review = review.find_all('div', class_ = 'mid-box margin-top20')[3].text
		polarity, subjectivity = Sentimental_Analysis.review_analysis(user_review)
		polarity = round(polarity, 2)
		subjectivity = round(subjectivity, 2)
		sentiments_user_reviews.append(polarity)
		print('Fetched one review')
		time.sleep(2)

#Creating frequency chart for sentiments
	y = range(0,10,1)
	plt.scatter(sentiments_user_reviews,y)
	plt.xlim(-1.0,1.0)
	plt.ylim(0,10)
	plt.title('Polarity Frequency')
	plt.xlabel('Polairty')
	plt.ylabel('Frequency')
	plt.show()



