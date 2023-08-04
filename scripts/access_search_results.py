from serpapi import GoogleSearch, GoogleScholarSearch
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_RESULTS_NUMBER = 10
def scraped_raw(query, result_number, googlescholarsearch = False):
    print(" ------------------------------------------ ")
    print("            SEARCHING GOOGLE                ")
    print(" ------------------------------------------ ")
    if googlescholarsearch:
        search = GoogleScholarSearch(
            {
                "q": query,
                "api_key": os.getenv('SERP_API_KEY'),
                "num": result_number,
            }
        )
    else:
        search = GoogleSearch(
            {
                "q": query,
                "api_key": os.getenv('SERP_API_KEY'),
                "num": result_number,
            }
        )
    result = search.get_dict()
    print(result_number)
    print(result)
    print(result.keys())
    return result["organic_results"]

def get_raw_links(raw_json):
    print(" ------------------------------------------ ")
    print("           GETTING RAW LINKS                ")
    print(" ------------------------------------------ ")
    result = []
    for dictionary in range(0, len(raw_json)):
        print("Getting Dictionary " + str(dictionary+1) + " of " + str(len(raw_json)))
        result.append(raw_json[dictionary]["link"])
    return result

def perform_all_actions(query, result_number = DEFAULT_RESULTS_NUMBER, googlescholarsearch = False):
    raw = scraped_raw(query, result_number, googlescholarsearch)
    link_list = get_raw_links(raw)
    
    return link_list