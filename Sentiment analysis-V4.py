#SO in case you tak tau, the .strip() function is used to remove any leading or trailing whitespace characters from the input string.
# --------------------------------------------------------------
# 1st Function to split sentence into words (credits to Jasper haha)
# --------------------------------------------------------------
def split_words(sentence):
    clean_sentence = ""
    for char in sentence:   # LOOP: check every character
        if char.isalpha() or char == " " or char == "-":   # keep letters, spaces, and "-"
            clean_sentence += char.lower()
    words = clean_sentence.split()   # split into words
    return words

# ---------------------------------------------------------------
# 2nd Function to load AFINN dictionary from file (credits to Jasper)
# ---------------------------------------------------------------
def load_afinn_dict(filepath="C:/Users/Syalinah/OneDrive/Documents/SIT/Python Project/AFINN-en-165.txt"):
    afinn = {}
    file = open(filepath, "r", encoding="utf-8")
    for line in file:
        parts = line.strip().split("\t")   # split word and score
        word = parts[0]
        score = int(parts[1])
        afinn[word] = score
    file.close()
    return afinn

# ------------------------------------------------------------------------------------
# 3rd Function to calculate sentiment score of each words in a sentence(credits to Jasper)
# ------------------------------------------------------------------------------------

def sentiment_score(sentence, afinn):
    words = split_words(sentence)
    score = 0
    for word in words:
        if word in afinn:
            score = score + afinn[word]
    return score

# --------------------------------------------------------------------------------------------------------------------
# This section will load the afinn dictionary, get user input, calculate scores, find positive and negative sentences
# --------------------------------------------------------------------------------------------------------------------

if __name__=='__main__':
    # This is to load the afinn dictionary
    afinn = load_afinn_dict()

    # This will ask user to input some text
    input_text = input("Enter your review(s): ").strip()

    if input_text == "": # check if input is empty
        print("Invalid input. Please enter some text.")
    else:
        # Split the input text into sentences using the regex module (re)
        import re
        sentences = re.split(r'(?<=[.!?]) +', input_text)
        
        # Then calculate score for each sentence
        sentence_scores = [] 
        for sentence in sentences:
            if sentence.strip() != "": # check if sentence is not empty
                score = sentiment_score(sentence, afinn) # calculate score of the sentence using the 2nd function sentiment_score
                sentence_scores.append([sentence, score]) # append into the list 'sentence_scores' [sentence, score]

        # Once you know the score of each sentences, calculate overall score of the text input
        overall_score = 0
        for sentenceLs in sentence_scores: 
            overall_score = overall_score + sentenceLs[1] 

        # Now, this will separate the positive and negative sentences based on their scores
        positive_sentences = []
        negative_sentences = []
        neutral_sentences = []
        for sentenceLs in sentence_scores:
            sentence = sentenceLs[0]
            score = sentenceLs[1]
            if score > 0:
                positive_sentences.append([sentence, score])
            elif score < 0:
                negative_sentences.append([sentence, score])
            else:
                neutral_sentences.append([sentence, score])

        # This will then find the most positive and most negative sentences
        most_positive = None
        most_negative = None 
        for sentenceLs in positive_sentences: 
            if most_positive is None or sentenceLs[1] > most_positive[1]:
                most_positive = sentenceLs
        for sentenceLs in negative_sentences:
            if most_negative is None or sentenceLs[1] < most_negative[1]:
                most_negative = sentenceLs
           

# -----------------------------------------------------------------------------------------------
# OUTPUT SECTION: Display the results
# -----------------------------------------------------------------------------------------------           
     
        # This print will display the scores of each sentences
        print("\nSentence Scores:")
        n=1
        for sentenceLs in sentence_scores:
            print(n,".",sentenceLs[0], " Score:", sentenceLs[1])
            n+=1

        # Will print out the final verdict of the text input
        if overall_score > 0:
            print("\nFinal Verdict for the paragraph: Positive""\nOverall Score:", overall_score)
        elif overall_score < 0:
            print("\nFinal Verdict for the paragraph: Negative""\nOverall Score:", overall_score)
        else:
            print("\nFinal Verdict for the paragraph: Neutral""\nOverall Score:", overall_score)

        # This will print out all the positive, negative, neutral sentences
        print("\nPositive Sentences:")
        n=1
        for sentenceLs in positive_sentences:
            print(n,".",sentenceLs[0])
            n+=1

        print("\nNegative Sentences:")
        n=1
        for sentenceLs in negative_sentences:
            print(n,".",sentenceLs[0])
            n+=1

        print("\nNeutral Sentences:")
        n=1
        for sentenceLs in neutral_sentences:
            print(n,".",sentenceLs[0])
            n+=1


        # This will print out the most positive and most negative sentences
        print("\nMost Positive Sentence:")
        if most_positive:
            print("'" + most_positive[0] + "' Score:", most_positive[1])
        else:
            print("No positive sentences found.")

        print("\nMost Negative Sentence:")
        if most_negative:
            print("'" + most_negative[0] + "' Score:", most_negative[1]) 
        else:
            print("No negative sentences found.")


# -------------------------------------------------------------------------------------
# Additional stuff i guess: identify the positive, negative, and neutral words? or nah
# -------------------------------------------------------------------------------------