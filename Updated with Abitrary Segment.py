# --- Existing functions ---
def load_afinn_dict(path):
    afinn = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            word, score = line.strip().split("\t")
            afinn[word] = int(score)
    return afinn

import re
def split_words(sentence):
    return re.findall(r"[a-z]+", sentence.lower())

def sentence_score(sentence, afinn):
    words = split_words(sentence)
    score = 0
    for word in words:
        if word in afinn:
            score += afinn[word]
    return score

# --- Add sentiment label ---
def get_label(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

def analyze_sentences(sentences, afinn):
    results = []
    for s in sentences:
        score = sentence_score(s, afinn)
        label = get_label(score)
        results.append((s, score, label))
    
    most_positive = max(results, key=lambda x: x[1])
    most_negative = min(results, key=lambda x: x[1])
    
    return results, most_positive, most_negative  

# --- Sliding Window Segments ---
def analyze_segments(sentences, afinn, window_size=3):
    segments = []
    n = len(sentences)
    
    for i in range(n - window_size + 1):
        segment = sentences[i:i+window_size]
        score = sum(sentence_score(s, afinn) for s in segment)
        segments.append((" ".join(segment), score))
    
    most_positive = max(segments, key=lambda x: x[1])
    most_negative = min(segments, key=lambda x: x[1])
    
    return segments, most_positive, most_negative


# --- Arbitrary-length Segments --- It will calc all possible segments based on the input and find the highest and lowest score segment
def analyze_arbitrary_segments(sentences, afinn):
    # Compute sentence scores
    scores = [sentence_score(s, afinn) for s in sentences]

    n = len(scores)
    best_pos = (None, None, float("-inf"))  # (start, end, score)
    best_neg = (None, None, float("inf"))   # (start, end, score)

    # Try all possible segments
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += scores[j]

            # update best positive
            if current_sum > best_pos[2]:
                best_pos = (i, j, current_sum)

            # update best negative
            if current_sum < best_neg[2]:
                best_neg = (i, j, current_sum)

    # Extract actual sentences
    pos_segment = sentences[best_pos[0]:best_pos[1] + 1]
    neg_segment = sentences[best_neg[0]:best_neg[1] + 1]

    return (pos_segment, best_pos[2]), (neg_segment, best_neg[2])



afinn = load_afinn_dict("AFINN-en-165.txt")

text = input("Enter your text: ")

# Separate into sentences by punctuation (.!?)
sentences = re.split(r'[.!?]\s*', text.strip())
sentences = [s for s in sentences if s]  # remove empty

# 1. Sentence-level analysis
results, most_pos, most_neg = analyze_sentences(sentences, afinn)
print("Sentence Scores:")
for s, sc, label in results:
    print(f"{s} -> {sc} ({label})")

print("\nMost Positive Sentence:", most_pos[0], "(Score:", most_pos[1], ")")
print("Most Negative Sentence:", most_neg[0], "(Score:", most_neg[1], ")")

# 2. Segment-level analysis (sliding window of 3)
segments, seg_pos, seg_neg = analyze_segments(sentences, afinn, window_size=3)
print("\nSegment Scores (window=3):")
for seg, sc in segments:
    print(f"[{seg}] -> {sc}")
print("\nMost Positive Segment:", seg_pos[0], "(Score:", seg_pos[1], ")")
print("Most Negative Segment:", seg_neg[0], "(Score:", seg_neg[1], ")")

# 3. Arbitrary-length segment analysis (All posible segments)
arb_pos, arb_neg = analyze_arbitrary_segments(sentences, afinn)
print("\nMost Positive Arbitrary-Length Segment:", arb_pos[0], "(Score:", arb_pos[1], ")")
print("Most Negative Arbitrary-Length Segment:", arb_neg[0], "(Score:", arb_neg[1], ")")
