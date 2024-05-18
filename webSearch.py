import wikipedia

from pprint import pprint

def format_results(raw_res): 
    """
     Parses and formats the results received from the search engine, then parses and saves their 
     respective summaries, titles, and url into a dictionary. Each result gets their own dictionary, and is added
     into one dictionary to hold all results. 

     Parameters:
        raw_res (str): 
            A string returned by the search engine. Contains 4 search results from duckduckgo, each separated 
            by square brackets. 

     Returns:
        all_results (dict): 
            A dictionary containing all of the parsed results and information.

    """
    all_results =  {}
    
    #Holds parsed results, then those results will then be taken and parsed into summary, link, title
    results_list = raw_res.split(']')     #list of results

    result_no = 0 # keeps track of the number of results being looped through to add to result name in dictionary.

   
    for result in results_list: #will loop through the list of results and format each one. 
        
        #checks to see whether the string in the loop is empty first to prevent an error 
        #that was previously being thrown towards the end of the loop due to how the individual 4 results were parsed above.
        if len(result) <=1:
            break
    
        # pprint(result)

        get_result_summary = result.split(', title:',1) # gets summary as one element of list, with title and link in other element
        get_result_link_and_title = result.split('link:') #will separate the title in the first element, and the link in the second for this result


        try:
            get_title = get_result_summary[1].split(', link:',1)#ERROR_ INDEX OUT OF RANGE
        except:
            get_title = "Invalid Source Found"
       

        #save info acqcuired into variables for easier handling 
        snipsum = get_result_summary[0].split('snippet:') #parses out out "[snippet:", to access just the summary text

        try:
            the_summary = snipsum[1]  #summary with "[snippet:" removed 
        except:
            the_summary = "No summary provided"

        the_title = get_title[0]

        try:
            the_link = get_result_link_and_title[1]
        except:
            the_link = "https://www.semrush.com/blog/what-does-error-404-not-found-mean/"
        
        result_no +=1 #increment the result number
        result_no_str = str(result_no) #cast the number as a string to be concatenated below 
        result_dict_name = "result_" + result_no_str

        
        #takes results and puts it into a dictionary, which is then added to the overall dicitonary of results
        new_res_dict =  dict(summary = the_summary, title = the_title, link = the_link)
        all_results[result_dict_name] =  new_res_dict

        #end of for loop
    
    
    return all_results



def print_res(result_dicts):
    """
     Takes in a dictionary and prints the individual search results that were stored in that
     dictionary from duckduckgo and wikipedia.

     Parameters:
        result_dicts (dict): 
        A dictionary that contains the information of individual search results in nested dictionaries.

     Returns:
        Nothing. Just prints out the contents of the dictionary.

    """
    for item, results  in result_dicts.items(): 
           print("--------------" + item + "--------------" ) #print result number
           for info in results:
               print(info + ':', results[info]) #print the summary, title, link from the individual result
           print()


# -------------------Wiki Results  --------------------------------------


def wiki(user_query, results_dict):
    """
     Takes in the user input, search for the result on wikipedia, and save 
     the summary, title, and URL into a dictionary

     Parameters:
        user_query (str): 
            A string containing the query entered by the user to be searched up
        results_dict (dict):
            A dictionary that contains all of the search results from this query, including from duckduckgo.
     Returns:
        results_dict (dict): An updated version of dictionary that was passed
            through that now contains an additional nested dictionary with results from wikipedia.

    """
    try:
        wiki_page = wikipedia.page(user_query)
    

        wiki_summary = wikipedia.summary(user_query) #brief version of the topic from wiki
        wiki_title = wiki_page.title
        wiki_url = wiki_page.url
    

        wiki_dict =  dict(summary = wiki_summary, title = wiki_title, link = wiki_url) #stores wiki results and info into a dict
        results_dict["wiki"] = wiki_dict #adds wiki dictionary as an entry into the overall results dictionary
    except:
        return results_dict

    return results_dict

def remove_invalid(results):
       '''
     Takes in the results once completed, and removes any items in the dictionary that 
     does not have a link or proper result.

     Parameters:
         results (dict): 
            A dictionary that contains nested dictionary with results, their titles, and URLs
            (including any possible invalid results)
       Returns:
           num_results (dict): A updated version of the results dictionary that was passed in with the invalid results removed. 
       
    '''
    new_results = {}
    for result in results:
        if results[result]['link'] == "https://www.semrush.com/blog/what-does-error-404-not-found-mean/":
            continue
        new_results[result] = results[result]
    

    num_results = {}
    for i, result in enumerate(new_results):
        num_results[result[:(len(result)-1)]+str(i+1)] = new_results[result]
    
    return num_results


#----------------CALL FUNCTIONS TO FORMAT AND PRINT RESULTS----------------------------

def get_web_search(engine, query):
    
    '''
     Takes in the user's query and the search engine to be used to conduct the search.

     Parameters:
        user_query (str): 
            A string containing the query entered by the user to be searched up.
        engine (langchain_community.tools.ddg_search.tool.DuckDuckGoSearchResults):
            Search engine to be used for searching information.
     Returns:
        results (dict): 
            A dictionary that contains nested dictionary with results, their titles, and URLs.
        over_rate_limit (boolean): 
            Keeps track of whether or not the user has reached the search rate limit

    '''
    
    over_rate_limit = False
    
    results = []
    raw_results = engine.run(query) #conducts the search
    

    if raw_results != None:
        results = format_results(raw_results) #if this is empty, set overrate limit to true and handle that error
        
    results = remove_invalid(results)
    results = wiki(query, results) #add wiki results to the overall results dictionary

    
    pprint(results)
    return results, over_rate_limit

