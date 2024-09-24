import firebase

def tokenize(sentence):
    # Split the sentence into rough tokens
    tokens = sentence.split()  
    result = []
    inside_quote = False
    current_quote = []


    # Loop through all tokens
    for token in tokens:
        if inside_quote:
            current_quote.append(token)
            if token.endswith('"'):
                # We've reached the end of the quote
                # Join and strip the quotes, then add to the result
                quoted_phrase = " ".join(current_quote)[1:-1]
                result.append(quoted_phrase)
                inside_quote = False
                current_quote = []
        elif token.startswith('"'):
            # We've encountered a token that starts with a quote
            inside_quote = True
            current_quote.append(token)
            if token.endswith('"'):
                # If the same token also ends with a quote, it's a single quoted token
                quoted_phrase = " ".join(current_quote)[1:-1]
                result.append(quoted_phrase)
                inside_quote = False
                current_quote = []
        else:
            # Add regular tokens 
            result.append(token)  

    #if inside_quote:
        #print("Error: Unmatched quotes in input")
    
    return result

# Find the symbol used in the query to correctly call get from firebase, return collection

def find_query(query, connect):
    query_result = []
    # IF query is length 3, example: "title, "==", "tenet", contiue else print try again
    if (len(query) == 3):

        # keywords for fields
        keywords = ["director", "title", "genre", "duration", "rating", "writer", "release_date"]
        
        # if first token is in the keywords continue, else try again
        if (query[0] in keywords):

            # comparison opperators list 
            comparison_opperators = [">", "<", ">=", "<=", "==", "of"]

            # if the 2nd token is in the list continue and send to corresponding functions else print try again
            if (query[1] in comparison_opperators):
                
                # if query operator is of 
                if( query[1] == "of"):

                    query_check = connect.complete_query("title", "==", query[2].title())

                    if ((len(query_check)) > 0):

                        if (query[0] == "director"):
                        
                            query_result.append(query_check[0].director)
                        elif (query[0] == "writer"):
                        
                            query_result.append(query_check[0].writer)

                            if(query_result == [""]):
                                print(f"\"{query[0]}\" of {query[2].title()} not available")

                        elif (query[0] == "genre"):
                        
                            query_result.append(query_check[0].genre)
                        elif (query[0] == "duration"):
                        
                            query_result.append(query_check[0].duration)
                        elif (query[0] == "rating"):
                        
                            query_result.append(query_check[0].rating)
                        elif (query[0] == "release_date"):
                        
                            query_result.append(query_check[0].release_date)
                        else:
                            query_result = None

                        


                # check if keyword isn't an integer variable
                elif ( query[0] == "duration" or query[0] == "rating" or query[0] == "release_date"):

                    if (query[1] == ">" or query[1] == ">=" or  query[1] == "<" or  query[1] == "<=" or query[1] == "=="):

                        query_result = connect.complete_query(query[0], query[1], float (query[2]))
                        
                    # check if comparison is not < > >= <=
                    else:

                        print(f"Cannot use \"{query[1]}\" with keyword: {query[0]}")
                        query_result = None


                    
                
                #  else complete query
                else:
                    if (query[1] == "=="):
                        query_result = connect.complete_query(query[0], query[1], query[2].title())
                    else:
                        print(f"Cannot use \"{query[1]}\" with keyword: {query[0]}")
                        query_result = None
                    
                
            else:
                print(f"{query[1]}: not a comparrison opperator in the system\nTry again or type Help for examples\n\n")
                query_result = None

        else:
            print(f"{query[0]}: not a field in the system\nTry again or type Help for examples\n\n")
            query_result = None

    else:
	
        print ("Query input of wrong size! Try again or type Help for examples\n\n")
        query_result = None
    
    return query_result


if __name__ == "__main__":

    # create instance of Firebase_Connection
    firebase_connect = firebase.FirebaseConnection("movies")
    
    while True:
        # Get user input
        sentence = input("> ").lower()
    
        # Check input
        if sentence == "help":
            # This is the Help Menu, with examples of what the expected input should be 
            print("Help Menu:\n\n")
            print("Help \nThis key will let you access this help menu\nExample: Help\n\n")
            print("Title \nThis key will access the field title \nExample: Title == \"Ratatouille\"\n\n")
            print("Director \nThis key will access the field Director \nExample: Director == \"Quentin Tarantino\"\n\n")
            print("Writer \nThis key will access the field Writer \nExample: Writer == \"Christopher Nolan\"\n\n")
            print("Genre \nThis key will access the field Genre \nExample: Genre == \"Comedy\"\n\n")
            print("Duration \nThis key will access the field duration(min) with conjunction of comparison operators \nExample: Duration > \"90\"\n\n")
            print("Release Date \nThis key will access the field Release Date(year) with conjunction of comparison operators \nExample: Release Date < \"2000\"\n\n")
            print("Rating \nThis key will access the field Rating with conjunction of comparison operators \nExample: Rating == \"9\"\n\n")
            print("Key Words: \n")
            print("OF \nThis key word will find a specific attribute of a movie\nExample: Director OF \"Ratatouille\"\n\n")
            print("AND \nThis key word will find multiple specified attributes of a movie with \nExample: Director == Christopher Nolan And Duration >\"50\"\n\n")
            tokenized = ""
        elif sentence == "quit":
            break
        elif sentence.count('\"') % 2 != 0:
            # Catch incorrect number of quotes
            print("Error: Incorrect number of quotes")
        else:
            # Call tokenize function
            tokenized = tokenize(sentence)
            print(tokenized)


        # Perform query
        # Check if and is in query
        if "and" in tokenized and len(tokenized) > 3:

            # Find the index of 'and'
            and_index = tokenized.index('and')

            # Split the list into before and after
            list_before_and = tokenized[:and_index]
            list_after_and = tokenized[and_index+1:]

            # Call 2 seperate functions for each side of and
            result1 = find_query(list_before_and, firebase_connect)
            print (result1)
            
            result2 = find_query(list_after_and, firebase_connect)

            if(result1 == [] and result2 != []):
                print(f"\"{list_before_and[2]}\" not found with keyword: {list_before_and[0]}")
                

            elif(result1 != [] and result2 ==[]):
                print(f"\"{list_after_and[2]}\" not found with keyword: {list_after_and[0]}")
                

            elif(result1 == [] and result2 == []):
                print(f"\"{list_before_and[2]}\" not found with keyword: {list_before_and[0]} and {list_after_and[2]}\" not found with keyword: {list_after_and[0]}")

            elif(result1 == None or result2 == None):
                continue

            else:
                # Find intersection
                result = [item for item in result1 if item in result2]
                print (result1)
                print (result2)
                print (result)

                if(result == None):
                    continue
            
                # issus here! 
                elif(len(result) == 0):
                
                     print(f"\"Query Not Found: {list_before_and[2]}\" not found with keyword: {list_before_and[0]} and {list_after_and[2]}\" not found with keyword: {list_after_and[0]}")


            
                else:

                    # Print Results
                    for r in result:

                        print(r)

        else:
            
            result = None

            if tokenized != "":

                # Call function for corresponding query
                result = find_query(tokenized, firebase_connect)

            if(result == None):
                continue
            
            elif(len(result) == 0):
                print(f"\"{tokenized[2]}\" not found with keyword: {tokenized[0]}")
            
            else:

                # Print Results
                for r in result:

                    print(r)

            
            
