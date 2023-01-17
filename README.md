# Project 2 of the OpenClassRoom Python developper training 

## Summary
This project scraps the data from the website  http://books.toscrape.com/index.html.

The books data are stored in a 'data/' directory in the working directory.
They are stored by books category in 'category'.csv files.

The image files are stored in a 'images/' directory in the vorking directory. The image file name matches the book title.

## Requirements
The modules needed for the scripts are in requirements.txt. In order to install them use the command :
```
pip install < requirements.txt
```
## How to run
You need to have python installed on your computer in order to run the script. Copy extract_data.py in the directory where you wants the data to be stored and run the command : 
```
python extract_data.py
```
The 'data/' and 'images/' directories will be created automatically if they do not exist.