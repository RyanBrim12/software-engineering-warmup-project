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
    # IF query is length 3, example: "title, "==", "tenet", contiue else print try again
    if (len(query) == 3):
        
        queryResult = []

        # keywords for fields
        keywords = ["director", "title", "genre", "duration", "rating", "writer", "release date"]
        
        # if first token is in the keywords continue, else try again
        if (query[0] in keywords):

            # comparison opperators list 
            comparisonOpperators = [">", "<", ">=", "<=", "==", "of"]

            # if the 2nd token is in the list continue and send to corresponding functions else print try again
            if (query[1] in comparisonOpperators):
                
                # if query operator is of 
                if( query[1] == "of"):

                    queryResult = connect.complete_query(query[0], "==", query[2])

                # check if keyword isn't an integer variable
                elif ( query[0] != "duration" and query[0] != "rating"):

                    # check if comparison is not < > >= <=
                    if (query[1] != "==" or query[1] != "of"):

                        print(f"Cannot use \"{query[1]}\" with keyword: {query[0]}")
                        
                    else:

                        queryResult = connect.complete_query(query[0], query[1], query[2])
                
                #  else complete query
                else:
                    queryResult = connect.complete_query(query[0], query[1], query[2])
                
            else:
                print(f"{query[1]}: not a comparrison opperator in the system\nTry again or type Help for examples\n\n")

        else:
            print(f"{query[0]}: not a field in the system\nTry again or type Help for examples\n\n")

    else:
	
        print ("Query input of wrong size! Try again or type Help for examples\n\n")
    
    return queryResult


if __name__ == "__main__":

    # create instance of Firebase_Connection
    firebaseConnect = firebase.Firebase_Connection("movies")
    
    while True:
        # Get user input
        sentence = input("> ").lower()
    
        # Check input
        if sentence == "help":
            # This is the Help Menu, with examples of what the expected input should be 
            print("Help Menu:\n\n")
            print("Help \nThis key will let you access this help menu\nExample: Help\n\n")
            print("Title \nThis key will access the field title \nExample: Title = \"Ratatouille\"\n\n")
            print("Director \nThis key will access the field Director \nExample: Director = \"Quentin Tarantino\"\n\n")
            print("Writer \nThis key will access the field Writer \nExample: Writer = \"Christopher Nolan\"\n\n")
            print("Genre \nThis key will access the field Genre \nExample: Genre = \"Comedy\"\n\n")
            print("Duration \nThis key will access the field duration(min) with conjunction of comparison operators \nExample: Duration > \"90\"\n\n")
            print("Release Date \nThis key will access the field Release Date(year) with conjunction of comparison operators \nExample: Release Date < \"2000\"\n\n")
            print("Rating \nThis key will access the field Rating with conjunction of comparison operators \nExample: Rating == \"9\"\n\n")
            print("Key Words: \n")
            print("OF \nThis key word will find a specific attribute of a movie\nExample: Director OF \"Ratatouille\"\n\n")
            print("AND \nThis key word will find multiple specified attributes of a movie with \nExample: Director AND Duration OF \"Ratatouille\"\n\n")
            
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
        if "and" in tokenized:

            # Find the index of 'and'
            and_index = tokenized.index('and')

            # Split the list into before and after
            list_before_and = tokenized[:and_index]
            list_after_and = tokenized[and_index+1:]

            # Call 2 seperate functions for each side of and
            result1 = find_query(list_before_and, firebaseConnect)
            result2 = find_query(list_after_and, firebaseConnect)

            # Find intersection
            result = [item for item in result1 if item in result2]

            if(len(result) == 0):
                print ("Query Not Found, Try Again!")
            
            else:

                # Print Results
                for r in result:

                    print(firebaseConnect)

        elif "or" in tokenized:
            # Find the index of 'or'
            and_index = tokenized.index('or')

            # Split the list into before and after
            list_before_or = tokenized[:and_index]
            list_after_or = tokenized[and_index+1:]

            # Call 2 seperate functions for each side of 'of'
            result1 = find_query(list_before_or, firebaseConnect)
            result2 = find_query(list_after_or, firebaseConnect)

            # Find union
            result = list(result1.symmetric_difference(result2))

            if(len(result) == 0):
                print ("Query Not Found, Try Again!")
            
            else:

                # Print Results
                for r in result:

                    print(firebaseConnect)

        else:
            # Call function for corresponding query
            result = find_query(tokenized, firebaseConnect)

            if(len(result) == 0):
                print ("Query Not Found, Try Again!")
            
            else:

                # Print Results
                for r in result:

                    print(firebaseConnect)

            
            
