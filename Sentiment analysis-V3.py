# --------------------------------------------------------------
# Function to split sentence into words (credits to Jasper haha)
# --------------------------------------------------------------
def split_words(sentence):
    clean_sentence = ""
    for char in sentence:   # LOOP: check every character
        if char.isalpha() or char == " " or char == "-":   # keep letters, spaces, and "-"
            clean_sentence += char.lower()
    words = clean_sentence.split()   # split into words
    return words

# ---------------------------------------------------------------
# Function to load AFINN dictionary from file (credits to Jasper)
# ---------------------------------------------------------------
def load_afinn_dict(filepath="C:/Users/Syalinah/OneDrive/Documents/SIT/AFINN-en-165.txt"):
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
# Function to calculate sentiment score of each words in a sentence(credits to Jasper)
# ------------------------------------------------------------------------------------

def sentiment_score(sentence, afinn):
    words = split_words(sentence)
    score = 0
    for word in words:
        if word in afinn:
            score = score + afinn[word]
    return score



if __name__=='__main__':
    # Step 1: Load dictionary
    afinn = load_afinn_dict()

    # Step 2: Ask user for text
    input_text = input("Enter your review(s): ").strip()

    if input_text == "":
        print("Invalid input. Please enter some text.")
    else:
        # Step 3: Split into sentences
        import re
        sentences = re.split(r'(?<=[.!?]) +', input_text)
        
        # Step 4: Calculate score for each sentence
        sentence_scores = [] 
        for sentence in sentences:
            if sentence.strip() != "":
                score = sentiment_score(sentence, afinn)
                sentence_scores.append([sentence, score]) # append into the list 'sentence_scores' [sentence, score]

        # Step 5: Calculate overall score
        overall_score = 0
        for sentenceLs in sentence_scores: 
            overall_score = overall_score + sentenceLs[1]

        # Step 6: Separate positive and negative sentences
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

        # Step 7: Find most positive and most negative
        most_positive = None
        most_negative = None 
        for sentenceLs in positive_sentences: 
            if most_positive is None or sentenceLs[1] > most_positive[1]:
                most_positive = sentenceLs
        for sentenceLs in negative_sentences:
            if most_negative is None or sentenceLs[1] < most_negative[1]:
                most_negative = sentenceLs
           

     
        # Display scores of each sentence
        print("\nSentence Scores:")
        n=1
        for sentenceLs in sentence_scores:
            print(n,".",sentenceLs[0], " Score:", sentenceLs[1])
            n+=1

        # Final Verdict for the whole paragraph
        if overall_score > 0:
            print("\nFinal Verdict for the paragraph: Positive""\nOverall Score:", overall_score)
        elif overall_score < 0:
            print("\nFinal Verdict for the paragraph: Negative""\nOverall Score:", overall_score)
        else:
            print("\nFinal Verdict for the paragraph: Neutral""\nOverall Score:", overall_score)


        print("\nAll Positive Sentences:")
        n=1
        for sentenceLs in positive_sentences:
            print(n,".",sentenceLs[0])
            n+=1

        print("\nAll Negative Sentences:")
        n=1
        for sentenceLs in negative_sentences:
            print(n,".",sentenceLs[0])
            n+=1

        print("\nAll Neutral Sentences:")
        n=1
        for sentenceLs in neutral_sentences:
            print(n,".",sentenceLs[0])
            n+=1

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


