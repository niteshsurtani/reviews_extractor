# README #

This project implements a crawler that all (or specified no. of) reviews from Amazon.com for a given product. The module takes two input as: 

product_page: https://www.amazon.com/Seagate-Expansion-Portable-External-STEA2000400/product-reviews/B00TKFEE5S/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1
num_pages: 2

and extract all the reviews for the first two pages.

Output:
total_reviews: total count of reviews extracted, e.g. 20

Writes a reviews.xlsx file in storage.tmp directory.

### How do I get set up? ###

* Install BeautifulSoup4, pandas

### Who do I talk to? ###

* Nitesh Surtani
