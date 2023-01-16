#==========================================================
#
#    Extract data from a book page on the website : 
#     http://books.toscrape.com/
#    and write it in a file called scrap_page.csv
#    for reusability : defines function scrap_book()
#
#==========================================================


import requests
from bs4 import BeautifulSoup
import csv

# write here the url of the page to be scraped :
url = "http://books.toscrape.com/catalogue/william-shakespeares-star-wars-verily-a-new-hope-william-shakespeares-star-wars-4_871/index.html"

def scrap_book(p_url):
    # get the web page for the book and parse it
    page = requests.get(p_url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup)
    else:
        print("erreur d\'url")

    # find the book title in the main product div and store it
    book_title = soup.find("div", class_="col-sm-6 product_main").h1.string
    #print(book_title)

    # find the table "product information" to retrieve UPC, prices and availability
    find_table = soup.find("table", class_="table table-striped")
    # The result is a list with the data needed in places 0, 2, 3 and 5
    book_upc = find_table.find_all("td")[0].text

    book_price_with_tax = find_table.find_all("td")[2].text
    book_price_with_tax = book_price_with_tax.replace("£","")

    book_price_without_tax = find_table.find_all("td")[3].text
    book_price_without_tax = book_price_without_tax.replace("£","")

    book_availability = find_table.find_all("td")[5].text
    book_availability = book_availability.replace("In stock (","")
    book_availability = book_availability.replace(" available)","")
    

    # The book description is the text from the 4th item in the list of <p> in the <article> "product_page" 
    book_description = soup.find("article", class_="product_page").find_all("p")[3].text
    #print(book_description)
    

    # The book category is located in the 3rd item of the breadcrumb 
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].a.text 
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

    # open an new scrap_page.csv in write mode
    with open('scrap_page.csv', 'w', encoding="utf-8", newline='') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        # write the headers
        writer.writerow(file_headers)
        # write the data
        ligne = [url
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

scrap_book(url)
