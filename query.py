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

if __name__ == "__main__":
    
    while True:
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
