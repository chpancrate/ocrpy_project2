#==========================================================
#
#    Program to scrap data from the website :
#     http://books.toscrape.com/
# 
#  Phase 4 :
#  scraping of category on the site 
#  scraping of the book pages from a category page of the site
#  scraping of the data for each book
#  the data are placed in a ./data/'category name'.csv 
#  the image files are retrieved and stored in a directory./image/'category name' 
#
#==========================================================


import requests
from bs4 import BeautifulSoup
import csv
import os
from slugify import slugify
from extract_functions import image_download, scrap_book, scrap_category, open_category_file

if __name__ == "__main__":

    print("extract script started")
    # define the website to be scraped
    url = "http://books.toscrape.com/index.html"
 
    page = requests.get(url)
   
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup)
        categories = soup.find("ul", class_="nav nav-list").find_all("li")

        # get rid of the first element as it is not a category
        categories.pop(0)

        for category in categories:

                # retrieve partial url 
                category_url=category.find("a")["href"]
                #print("category_url = ", category_url)

                # create the file name from the partial url 
                file_name = category_url.replace("catalogue/category/books/","")
                file_name = file_name.split("_")[0]
                file_name = file_name.lower()
                file_name = file_name.replace("-"," ")
                file_name = 'data/' + file_name + ".csv"
                #print(file_name)
                
                open_category_file(file_name)

                # create the full url from the partial url
                category_url="http://books.toscrape.com/" + category_url
                #print(category_url)

                cat_url = category_url.replace("index.html","") # truncated category url
                #print("cat_url = ", cat_url)    

                scrap_category(category_url, cat_url)
    else:
        print("website url error")

    print("extract script ended")

        


