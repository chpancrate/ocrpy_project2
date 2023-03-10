#==========================================================
#
#    Definition of functions used to scrap data from the website :
#     http://books.toscrape.com/
# 
#  image_download : retrieve an image file from an url 
#  scrap_book : scrap the data from a book poage
#  scrap_category : retrieve all the books from a category
#  open_category_file : open the csv file where the book data for a category will be stored
#
#==========================================================

import requests
from bs4 import BeautifulSoup
import csv
import os
from slugify import slugify

def image_download(p_image_url, p_category, p_book_title):
    
    file_name_img = slugify(p_book_title)
    file_name_img = "images/" + p_category + "/" + file_name_img + ".jpg" 

    newdir = 'images/' + p_category + "/" 

    if not os.path.exists(newdir):
        os.makedirs(newdir)

    image = requests.get(p_image_url)
    if image.status_code == 200:
        with open(file_name_img, 'wb') as file_img:
            file_img.write(image.content)
            #print('Image sucessfully downloaded: ',file_name)
    else:
        print("Image", p_image_url, " not downloaded")
        return


def scrap_book(p_url):
    ''' parse the url in parameter and retrieve the data from the page
    the url parameter must be a book page from the site http://books.toscrape.com/'''
    
    # get the web page for the book and parse it
    page = requests.get(p_url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup)
    else:
        print("book page url error")
        return

    # find the book title in the main product div and store it
    book_title = soup.find("div", class_="col-sm-6 product_main").h1.string
    #print(book_title)

    # find the table "product information" to retrieve UPC, prices and availability
    find_table = soup.find("table", class_="table table-striped")
    # The result is a list with the data needed in places 0, 2, 3 and 5
    book_upc = find_table.find_all("td")[0].text
    
    book_price_with_tax = find_table.find_all("td")[2].text
    book_price_with_tax = book_price_with_tax.replace("??","")
    
    book_price_without_tax = find_table.find_all("td")[3].text
    book_price_without_tax = book_price_without_tax.replace("??","")
    
    book_availability = find_table.find_all("td")[5].text
    book_availability = book_availability.replace("In stock (","")
    book_availability = book_availability.replace(" available)","")

    # test if the description section exists because some book pages do not have it
    exist_description = soup.find("div", id="product_description")
    #print(exist_description)
    
    if exist_description == None:
        book_description = "pas de description"
    else:
        # The book description is the text from the 4th item in the list of <p> in the <article> "product_page" 
        book_description = soup.find("article", class_="product_page").find_all("p")[3].text
    #print(book_description)   

    # The book category is located in the 3rd item of the breadcrumb 
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].a.text 
    # formatting to match the file name : lower case no -
    category = category.lower()
    category = category.replace("-"," ")
    #print(category)

    # The book rating is in the class name of <p class="star-rating XXXX>  in the main product div
    book_rating_text = str(soup.find("div", class_="col-sm-6 product_main").find_all("p")[2]['class'][1])
    rating_translate = {'One': '1', 'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5'} 
    book_rating = rating_translate[book_rating_text]
    #print(book_rating)

    # find the image url in the carroussel div and store it
    book_image_url = soup.find("div", class_="item active").find_all("img")[0]['src']
    book_image_url = book_image_url.replace("../..", "http://books.toscrape.com")
    #print(book_image_url)

    image_download(book_image_url, category, book_title)
    
    ''' use for debug
    print("page url : " + url)
    print("UPC : " + book_upc)
    print("Title : " + book_title)
    print("Price Tx In : " + book_price_with_tax)
    print("Price Tx Ex : " + book_price_without_tax)
    print("Availability : " + book_availability)
    print("Description : " + book_description)
    print("Category : " + category)
    print("Review Rating : " + book_rating)
    print("image_url : " + book_image_url)
    '''

    file_name = 'data/' + category.lower() + ".csv"

    # open the file <category>.cvs in append mode
    with open(file_name, 'a', encoding="utf-8", newline='') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        
        # write the data
        ligne = [p_url
                ,book_upc
                ,book_title
                ,book_price_with_tax
                ,book_price_without_tax
                ,book_availability
                ,book_description
                ,category
                ,book_rating
                ,book_image_url]
        writer.writerow(ligne)


def open_category_file(p_file_name):
    # open the file and create the header
    newdir = 'data/' 

    # if the directory data/ does not exit we create it
    if not os.path.exists(newdir):
        os.makedirs(newdir)

    file_headers = ["product_page_url"
                ,"universal_product_code"
                ,"title"
                ,"price_including_tax"
                ,"price_excluding_tax"
                ,"number_available"
                ,"product_description"
                ,"category"
                ,"review_rating"
                ,"image_url"]

    # open the new category.csv in write mode
    with open(p_file_name, 'w', encoding="utf-8", newline='') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        # write the headers
        writer.writerow(file_headers)


def scrap_category(p_url, p_cat_url):

    page = requests.get(p_url)
    
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup)
    else:
        print("category page url error")
        return
    
    articles = soup.find_all("article", class_="product_pod")
    for article in articles:
        
        work_url=article.find("div", class_="image_container").find("a")["href"]
        book_url=work_url.replace("../../..", "http://books.toscrape.com/catalogue")
        scrap_book(book_url)
        #print(book_url)

    
    pager = soup.find("li", class_="next")
    if pager != None:
        next_url=pager.find("a")["href"]
        next_url=p_cat_url + next_url
        #print("next_url = ", next_url)
        scrap_category(next_url, p_cat_url) 
    else:
        #print("FIN DES PAGES")
        return

