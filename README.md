# Project 2 of the OpenClassRoom Python developper training 

## Summary
This project scraps the data from the website  http://books.toscrape.com/index.html.

The books data are stored in a 'data/' directory under the working directory.
They are stored by books category in 'category'.csv files.

The image files are stored in 'images/category/' directories under the working directory. The image file name matches the book title.

## Requirements
These scripts run with Python 3.11.1

To install python you can download it here : https://www.python.org/downloads/

If you are new to Python you can find information here : https://www.python.org/about/gettingstarted/ 

It is better to run the scripts in a virtual environment. You can find information on virtual envrionments here : https://docs.python.org/3/library/venv.html 

Once in your virtual environment, the following modules need to be installed :
- bs4            : 0.0.1
- beautifulsoup4 : 4.11.1
- python-slugify : 7.0.0
- requests       : 2.28.2

All the modules needed for the scripts are in requirements.txt. A quick way to install them is to run the command below in a python terminal:
```
pip install -r requirements.txt
```

## How to run

In order to run it, clone the following repository in the directory where you want the data to be stored : https://github.com/chpancrate/ocrpy_project2

### Normal mode
To run the script in normal mode use the command : 
```
python ./extract_data.py
```
The script will retrieve all the data from the website. The 'data/' and 'images/' directories will be created automatically if they do not exist.

### Demo mode
There is a demo mode that will retrieve only the 5 first categories. To run it use the command : 
```
python ./extract_data.py demo
```

