# --------------------------------------------------------------
# Function to split sentence into words (credits to Jasper haha)
# --------------------------------------------------------------
def split_words(sentence):
    clean_sentence = ""
    for char in sentence:   # LOOP: check every character
        if char.isalpha() or char == " " or char == "-" or char == ",":   # keep letters, spaces, and "-"
            clean_sentence += char.lower()
    words = clean_sentence.split()   # split into words
    return words

# ---------------------------------------------------------------
# Function to load AFINN dictionary from file (credits to Jasper haha)
# ---------------------------------------------------------------
def load_afinn_dict(filepath=r"C:\Users\Stephanie\Downloads\INF1002(Programming Fundemental)\inf1002\pythonProject\AFINN-en-165.txt"): #Ensure the file path is correct
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
# Function to calculate sentiment score of each words in a sentence(credits to Jasper hahaha)
# ------------------------------------------------------------------------------------

def sentiment_score(sentence, afinn):
    words = split_words(sentence)
    score = 0
    for word in words:
        if word in afinn:
            score = score + afinn[word]
    return score

# -----------------------------
# Sliding Window Function
# -----------------------------
def sliding_window(sentences, afinn, window_size=3):
    if len(sentences) < window_size:
        window_size = len(sentences)
    
    windows = []
    for i in range(len(sentences) - window_size + 1):
        window_sentences = sentences[i:i+window_size]
        # sum sentiment scores for this window
        total_score = sum(sentiment_score(s, afinn) for s in window_sentences)
        windows.append((window_sentences, total_score))
    
    # find most positive and most negative window
    most_positive = max(windows, key=lambda x: x[1])
    most_negative = min(windows, key=lambda x: x[1])
    
    return windows, most_positive, most_negative

# ----------------------------------------------------
# Function to load a list of english words from file 
# ----------------------------------------------------
def load_english_words(filepath=r"C:\Users\Stephanie\Downloads\INF1002(Programming Fundemental)\inf1002\pythonProject\englishWords.txt"): #Ensure the file path is correct
    words_set = set()
    with open(filepath, "r") as file:
        for line in file:
            # strip whitespace and convert to lowercase
            words_set.add(line.strip().lower())
    return words_set

# -----------------------------
# Re-insert space Function
# -----------------------------
def segment(sentence, segmentation_words):
    results = []

    # Function to try to segment the sentence 
    def find_segments(sub_sentence, current_segment):
        if not sub_sentence:
            results.append(current_segment)
            return
        
        # check if the word is found
        found_word = False

        # Check substring starting from the first character, and increase one letter at a time
        for i in range(1, len(sub_sentence) + 1):
            # take the first i character
            word_part = sub_sentence[:i]
            # if it matches the word in the dictionary
            if word_part in segmentation_words:
                found_word = True
                # Add the word to the current segment and continue with the rest
                find_segments(sub_sentence[i:], current_segment + [word_part])
        
        # If no word is found in the dictionary, treat the first character as a word by itself. 
        # This will prevent the function from stopping.
        if not found_word:
            find_segments(sub_sentence[1:], current_segment + [sub_sentence[0]])

    find_segments(sentence, [])

    # pick the segmentation with the fewest spaces
    best_segmentation = results[0]
    fewest_spaces = len(best_segmentation)
    # choose the segmentation with the longest valid word 
    for seg in results:
        if len(seg) < fewest_spaces:
            best_segmentation = seg
            fewest_spaces = len(seg)

     # return the chosen segmentation as a sentence with space        
    return " ".join(best_segmentation)

if __name__=='__main__':
    # Step 1: Load dictionary aka the AFINN dict and the English words list
    afinn = load_afinn_dict()
    words_set = load_english_words()
    # Combine them into a single set for segmentation
    segmentation_words = words_set.union(set(afinn.keys()))

    # Step 2: Ask user to input smtg bah
    input_text = input("Enter your review(s): ").strip()

    if input_text == "":
        print("Invalid input. Please enter some text.")
    else:
        # Step 3: Split the input text aka a para... into sentences
        import re
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])', input_text) if s.strip() != ""]

        # Step 4: Segment each sentence before scoring
        processed_sentences = []
        for sentence in sentences:
            # check whether the sentence is empty
            if sentence.strip() != "":
                # remove punctuation like . ! ? of the sentence
                clean_sentence = sentence.replace(".", "").replace("!", "").replace("?", "")
                # if user typed with spaces, leave it as it is 
                if " " in clean_sentence:
                    processed_sentences.append(clean_sentence.strip())
                # else segment the sentence into words using the dictionary
                else:
                    segmented_results = segment(clean_sentence.lower(), segmentation_words)
                    processed_sentences.append(segmented_results.strip())

        # Step 5: Calculate the score for each sentence
        sentence_scores = [] 
        for sentence in processed_sentences: 
            if sentence.strip() != "":
                score = sentiment_score(sentence, afinn)
                sentence_scores.append([sentence, score]) # SYALLL this is to append into the list 'sentence_scores' [sentence, score] okayyyy :D

        # Step 6: Calculate overall score
        overall_score = 0
        for sentenceLs in sentence_scores: 
            overall_score = overall_score + sentenceLs[1]

        # Step 7: Separate positive, negative, & neutral sentences yurh
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

        # Step 8: Find most positive and most negative sentences onlyyy
        most_positive = None
        most_negative = None 
        for sentenceLs in positive_sentences: 
            if most_positive is None or sentenceLs[1] > most_positive[1]:
                most_positive = sentenceLs
        for sentenceLs in negative_sentences:
            if most_negative is None or sentenceLs[1] < most_negative[1]:
                most_negative = sentenceLs
           

        # Display the segmented sentence   
        print("\nSegmented Sentences:")
        n=1
        for seg in processed_sentences:
            print(n,".", seg)
            n+=1
     
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
