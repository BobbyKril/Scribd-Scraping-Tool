This tool automates the process of scraping text from Scribd documents using OCR. It works by:

Reading a list of Scribd URLs from a file (urls.txt).

Opening each URL in a Chrome browser using Selenium.

Scrolling through the document, taking periodic screenshots.

Using Tesseract OCR to extract text from the screenshots.

Cleaning and saving the extracted text into .txt files.

The output is stored in a folder called scraped_texts.


Collect your scribd URLs in a urls.txt file listed line by line. 
For example:
https://www.scribd.com/document/129813635/Jay-Credit-Report
https://www.scribd.com/document/487124632/CreditReporte
https://www.scribd.com/document/598221810/CreditReporte


Requirements
Python 3.x
selenium
webdriver-manager
pillow
pytesseract
Tesseract-OCR (installed at C:\Program Files\Tesseract-OCR\)

Installation
Install Python dependencies:

pip install -r requirements.txt

Download Tesseract-OCR:
https://github.com/UB-Mannheim/tesseract/wiki

Make sure this path is set in your script:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
