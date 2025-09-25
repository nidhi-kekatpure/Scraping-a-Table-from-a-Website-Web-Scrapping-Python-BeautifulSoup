# 🕸️ Web Scraping: Largest U.S. Companies by Revenue

## Business Problem
Businesses, investors, and analysts often need up-to-date information about the **largest companies in the United States by revenue** to track market leaders, analyze industry trends, and support decision-making.  
Manually gathering this data from websites like **Wikipedia** is time-consuming and prone to errors.

## Overview
This project demonstrates **web scraping using Python, BeautifulSoup, and Requests**.  
We scrape data from the [Wikipedia page on largest U.S. companies by revenue](https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue), extract the table containing the top 100 companies, and save the data into a structured **CSV file** for further analysis.

---

## Tools & Libraries
- **Python 3.x**
- [requests](https://docs.python-requests.org/) – to fetch the webpage  
- [BeautifulSoup (bs4)](https://www.crummy.com/software/BeautifulSoup/) – to parse HTML  
- [pandas](https://pandas.pydata.org/) – to structure data and export CSV  

---


**Challenge:**
- Extract a structured dataset of the **Top 100 U.S. companies by revenue**  
- Include details such as **Company Name, Industry, Revenue, Revenue Growth %, Number of Employees, and Headquarters**  
- Save it into a reusable format (**CSV**) for analysis or integration with BI tools  

---

## My Solution with Web Scraping
I solved this problem by building a **Python web scraper** that automatically:  

1. **Fetches** the Wikipedia page containing the largest companies by revenue  
2. **Parses** the HTML table using **BeautifulSoup**  
3. **Extracts** all relevant fields:
   - Rank  
   - Name  
   - Industry  
   - Revenue (USD millions)  
   - Revenue Growth %  
   - Employees  
   - Headquarters  
4. **Cleans** the data into a well-structured **pandas DataFrame**  
5. **Exports** the dataset into a **CSV file** for further business analysis  

---


