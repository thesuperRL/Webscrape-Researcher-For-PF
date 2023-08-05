from scripts import ai_relation_checker

def run_web_query(query_string, googlescholarsearch = False, total_searches = 10, first_responses = 10):
    print(" ------------------------------------------ ")
    print("             STARTING FUNCTION              ")
    print(" ------------------------------------------ ")
    query_data, text_list = ai_relation_checker.construct_query_json(query_string, total_searches, googlescholarsearch)
    response_data = ai_relation_checker.query(query_data)
    sorted_query = ai_relation_checker.match_and_sort(response_data, text_list)
    ai_relation_checker.print_best_match(sorted_query, first_responses)