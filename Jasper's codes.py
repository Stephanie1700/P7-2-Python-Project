#Load AFINN Dictionary
def load_afinn_dict(path):
    afinn = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            word = parts[0]
            score = int(parts[1])
            afinn[word] = score
    return afinn

# Word Splitting
def split_words(sentence):
    clean_sentence = ""
    for char in sentence:
        if char.isalpha() or char.isspace():
            clean_sentence += char.lower()
    words = clean_sentence.split()
    return words
    
# Sentence Scoring
def sentence_score(sentence, afinn):
    words = split_words(sentence)
    score = 0
    for word in words:
        if word in afinn:
            score += afinn[word]
    return score

# Add sentiment label
def get_label(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"
    
# Loop the sentence scoring and labeling code for all sentences
def analyze_sentences(sentences, afinn):
    results = []
    for s in sentences:
        score = sentence_score(s, afinn)
        label = get_label(score)
        results.append((s, score, label))
    
    most_positive = max(results, key=lambda x: x[1])
    most_negative = min(results, key=lambda x: x[1])
    
    return results, most_positive, most_negative


# Test Run
afinn = load_afinn_dict("C:/Users/Syalinah/OneDrive/Documents/SIT/Python Project/AFINN-en-165.txt")


test_sentences = [
    "I love programming.",
    "This is the worst day ever.",
    "It's a slay experience.",
    "The food was great but the service was terrible.",
    "I am so happy and excited!",
    "I feel sad and lonely."
]

# per sentence score 
results, most_pos, most_neg = analyze_sentences(test_sentences, afinn)
print("Sentence Scores:")
for s, score, label in results:
    print(f"{s} -> {score} ({label})")

# Print the most positive & negative
print("\nMost Positive Sentence:", most_pos[0], "Score:", most_pos[1])
print("Most Negative Sentence:", most_neg[0], "Score:", most_neg[1])