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

# Find the symbol used in the query to correctly call get from firebase
def find_query(query):
    # TODO: Find query language used and call that function
    return 0

# TODO: Implement all relationship functions
def less_than(query):
    pass

def less_than_equal_to(query):
    pass

def greater_than(query):
    pass

def greater_than_equal_to(query):
    pass

def equal_to(query):
    pass

def not_in(query):
    pass

def of(query):
    pass


if __name__ == "__main__":
    
    while True:
        # Get user input
        sentence = input("> ").lower()

        # Check input
        if sentence == "help":
            # TODO: add help language
            pass
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
            result1 = find_query(list_before_and)
            result2 = find_query(list_after_and)

            # Find intersection
            result = [item for item in result1 if item in result2]

        elif "or" in tokenized:
            # Find the index of 'or'
            and_index = tokenized.index('or')

            # Split the list into before and after
            list_before_or = tokenized[:and_index]
            list_after_or = tokenized[and_index+1:]

            # Call 2 seperate functions for each side of 'of'
            result1 = find_query(list_before_or)
            result2 = find_query(list_after_or)

            # Find union
            result = list(result1.symmetric_difference(result2))

        else:
            # Call function for corresponding query
            result = find_query(tokenized)