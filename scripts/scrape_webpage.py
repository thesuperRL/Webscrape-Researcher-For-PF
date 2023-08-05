import requests
from bs4 import BeautifulSoup

headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) '
+'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}

def get_one_scrape(url):
    results = []
    
    # Request
    try:
        r1 = requests.get(url, headers=headers, timeout=10)
        print("    Request Received")
    except:
        print("    REQUEST FAILED, MOVING ON")
        return results
    
    # We'll save in coverpage the cover page content
    coverpage = r1.content
    print("    Coverpage Scraped")
    
    # Soup creation
    soup1 = BeautifulSoup(coverpage, 'lxml')
    print("    Soup Created")
    
    # News identification
    coverpage_news = soup1.find_all('p')
    print("    Identified body")
    
    if len(coverpage_news) == 0:
        print("    Webpage Empty, Moving on...")
        return results
    
    for paragraph in range(0, len(coverpage_news)):
        print("    Paragraph " + str(paragraph+1) + " of " + str(len(coverpage_news)))
        results.append({
            'url' : url,
            'text' : coverpage_news[paragraph].get_text().strip()
        })
        
    return results

def compile_scrapes(url_list):
    print(" ------------------------------------------ ")
    print("        BEGINNING SCRAPE OPERATION          ")
    print(" ------------------------------------------ ")
    results = []
    
    for url in range(0, len(url_list)):
        print("Scraping URL " + str(url+1) + " of " + str(len(url_list)) + ": " + url_list[url])
        results += get_one_scrape(url_list[url])
        
    print("------------SCRAPE FINISHED------------")
    return results