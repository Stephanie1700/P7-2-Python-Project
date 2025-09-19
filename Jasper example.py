# ------------------------------
# FUNCTION: Load AFINN Dictionary
# ------------------------------
def load_afinn_dict(path):
    afinn = {}
    f = open(path, "r", encoding="utf-8")
    for line in f:  # <-- LOOP
        parts = line.strip().split("\t")
        word = parts[0]
        score = int(parts[1])
        afinn[word] = score
    f.close()
    return afinn


# ------------------------------
# FUNCTION: Word Splitting (basic)
# ------------------------------
def split_words(sentence):
    clean_sentence = ""
    for char in sentence:  # <-- LOOP
        if char.isalpha() or char.isspace():
            clean_sentence += char.lower()
    words = clean_sentence.split()
    return words


# ------------------------------
# FUNCTION: Sentence Scoring
# ------------------------------
def sentence_score(sentence, afinn):
    words = split_words(sentence)
    score = 0
    for word in words:  # <-- LOOP
        if word in afinn:
            score += afinn[word]
    return score


#Test Run
afinn = load_afinn_dict("C:/Users/Syalinah/OneDrive/Desktop/AFINN-en-165.txt")

test_sentence = "The movie was fantastic but the ending was disappointing."
print("Sentence:", test_sentence)
print("Score:", sentence_score(test_sentence, afinn))