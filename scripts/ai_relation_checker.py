import json
import requests

from scripts.scrape_webpage import compile_scrapes
from scripts.access_search_results import perform_all_actions
import os
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv('HUGGINGFACE_API_KEY')

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/msmarco-distilbert-base-tas-b"
headers = {"Authorization": f"Bearer {api_token}"}

def construct_query_json(source, result_number, googlescholarsearch):
    url_list = perform_all_actions(source, result_number, googlescholarsearch)
    text_list = compile_scrapes(url_list)
    
    print(" ------------------------------------------ ")
    print("        CONSTRUCTING QUERY JSON             ")
    print(" ------------------------------------------ ")
    
    sentences = []
    for json_dict in text_list:
        sentences.append(json_dict["text"])
    
    query_data = {
            "inputs": {
                "source_sentence": source,
                "sentences": sentences
            }
        }
    
    print("    FINISHED JSON CONSTRUCTION")
    return query_data, text_list

def query(query_data):
    print(" ------------------------------------------ ")
    print("        BEGINNING RELEVANCE CHECK           ")
    print(" ------------------------------------------ ")
    response = requests.post(API_URL, headers=headers, json=query_data)
    return response.json()
    
def sorting_function_via_relevance(dictionary):
     return dictionary['relevance']
    
def match_and_sort(response_data, text_list):
    print(" ------------------------------------------ ")
    print("              SORTING RESULTS               ")
    print(" ------------------------------------------ ")
    print("    These two numbers should match:")
    print("    " + str(len(response_data)))
    print("    " + str(len(text_list)))
    for response in range(0, len(response_data)):
        text_list[response]["relevance"] = response_data[response]
        
        
    text_list.sort(key=sorting_function_via_relevance, reverse=True)
    return text_list

def print_best_match(sorted_query, first_responses):
    print(" ------------------------------------------ ")
    print("          PRINTING BEST RESPONSES           ")
    print(" ------------------------------------------ ")
    link_set = set([])
    for item in range(0, first_responses):
        dumped = json.dumps(sorted_query[item])
        link_set.add(sorted_query[item]['url'])
        print(dumped)
    print(link_set)
    
def run_web_query(query_string, first_responses):
    print(" ------------------------------------------ ")
    print("             STARTING FUNCTION              ")
    print(" ------------------------------------------ ")
    query_data, text_list = construct_query_json(query_string)
    response_data = query(query_data)
    sorted_query = match_and_sort(response_data, text_list)
    print_best_match(sorted_query, first_responses)