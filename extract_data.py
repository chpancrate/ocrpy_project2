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
import sys
from slugify import slugify
from extract_functions import image_download, scrap_book, scrap_category, open_category_file


def main():
    
     # define the website to be scraped
    url = "http://books.toscrape.com/index.html"
 
    page = requests.get(url)
   
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup)
        categories = soup.find("ul", class_="nav nav-list").find_all("li")

        # get rid of the first element as it is not a category
        categories.pop(0)

        if len(sys.argv) == 1:

            print("extract script normal mode started")

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
                
            print("extract script normal mode ended")
 
        else:
            if sys.argv[1] == "demo":
                
                print("extract script demo mode started")
                
                i = 1 # use to count the number of categories parsed, in demo mode stop at 5
                
                for category in categories:
                
                    if i < 6:
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
                        i += 1
                    else:
                        print("extract script demo mode ended")
                        return
            else:
                print("Bad arguments. Use without argument for normal mode or with the argument demo for the demo mode" )
                return
    else:
        print("website url error")
        return

       
if __name__ == "__main__":
    main()

