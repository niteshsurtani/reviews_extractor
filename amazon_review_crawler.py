import requests
import os
from bs4 import BeautifulSoup
import pprint 
import json
import re
import pandas as pd
import time

reviews = []
products_list = {}

products = [
	# 'https://www.amazon.com/Aveeno-Baby-Moisture-Delicate-Fragrance/dp/B0030UF6EW/',
	# 'https://www.amazon.com/Aveeno-Baby-Wash-Shampoo-Tear-Free/dp/B00MNSEN82/',
	# 'https://www.amazon.com/Aveeno-Baby-Soothing-Relief-Moisture/dp/B00186RF62/',
	'https://www.amazon.com/Johnsons-Head-Toe-Gentle-Baby/dp/B00MNSEOSG/',
	# 'https://www.amazon.com/Johnsons-Baby-Tear-Free-Shampoo/dp/B00WEBX65O/',
	# 'https://www.amazon.com/Johnsons-Baby-Shampoo-Lavender-15z/dp/B01EMZ9C16/',
	# 'https://www.amazon.com/Johnsons-Baby-Lotion-Moisturizer-Sensitive/dp/B00MNSEPT4/',
	# 'https://www.amazon.com/Babyganics-Daily-Lotion-Fragrance-Ounce/dp/B00UX7Z8UW/',
	# 'https://www.amazon.com/Babyganics-Baby-Shampoo-Body-Fragrance/dp/B00FSCBQV2/',
	# 'https://www.amazon.com/Cetaphil-Baby-Organic-Calendula-Sunflower/dp/B00OKJGLI2/',
	# 'https://www.amazon.com/Shea-Moisture-Butter-Healing-Lotion/dp/B005C2NAO4/',
	# 'https://www.amazon.com/Burts-Bees-Nourishing-Lotion-Original/dp/B01N16I5T1/',
	# 'https://www.amazon.com/Babo-Botanicals-Oatmilk-Calendula-Moisturizing/dp/B003C13D4E/',
	# 'https://www.amazon.com/Seventh-Generation-Lotion-Moisturizing-Coconut/dp/B01JLQFUF8/',
]

def getReviews(page, product_name):
	global reviews

	content = requests.get(page)
	html = content.text
	soup = BeautifulSoup(html, "lxml")
	total = 0

	try:
		for level1 in soup.find_all("div", {'class': 'a-section a-spacing-none reviews-content a-size-base'}):
			for level2 in level1("div", {'id': 'cm_cr-review_list'}):
				for level3 in level2("div", {'class': 'a-section review'}):
					review = {}
					review['product'] = product_name

					# Avoid overwriting of stars
					stars_text = ""

					# Get review ratings and title
					for level4 in level3("div", {'class': 'a-row'}):
						for level5 in level4("span", {'class': 'a-icon-alt'}):
							if stars_text == "":
								stars_text = level5.text.split(" ")[0]
								review['stars'] = stars_text
					
					for level4 in level3("a", {'class': 'a-size-base a-link-normal review-title a-color-base a-text-bold'}):
						review['title'] = level4.text

					# Get review text
					for level4 in level3("div", {'class': 'a-row review-data'}):
						for level5 in level4("span", {'class': 'a-size-base review-text'}):
							text = re.sub(r"<.*>", " ", level5.text)
							review['text'] = text.strip()

					reviews.append(review)
					total += 1

		return total

	except:
		return 0


def extractReviews():
	global reviews

	for product_name, product_page in products_list.items():
		print(product_name)
		reviews =  []

		start_page = 6

		# Set this for required no. of pages
		total_pages = 10000

		total_reviews = 0
		part = 1

		for pageno in range(start_page, total_pages):
			page = product_page + "/ref=cm_cr_getr_d_paging_btm_" + str(pageno) + "?ie=UTF8&reviewerType=all_reviews&pageNumber=" + str(pageno)
			print(page)
			total = getReviews(page, product_name)
			print("Page No. = " + str(pageno))

			if total == 0:
				break

			total_reviews += total

			if pageno % 5 == 0:
				df1 = pd.DataFrame.from_dict(reviews)
				writer = pd.ExcelWriter('storage.tmp/' + product_name + "_part" + str(part) + '.xlsx')
				df1.to_excel(writer)

				reviews = []
				part += 1
				time.sleep(30)

		df1 = pd.DataFrame.from_dict(reviews)
		writer = pd.ExcelWriter('storage.tmp/' + product_name + "_part" + str(part) + '.xlsx')
		df1.to_excel(writer)

		print(total_reviews)



		time.sleep(120)

def updateProductList():
	global products
	global products_list

	for product in products:
		p = product.split("/")
		name = p[3]
		url = "/".join(p[:3]) + '/product-reviews/' + p[5]
		products_list[name] = url

if __name__ == "__main__":
	updateProductList()
	extractReviews()