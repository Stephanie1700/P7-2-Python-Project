from flask import Flask, render_template, request
from app import load_afinn_dict, sentiment_score, sliding_window, get_most_positive_negative_sentence, analyze_arbitrary_segments,segment,load_english_words
import re

app = Flask(__name__, static_folder='static', template_folder='templates')

afinn = load_afinn_dict()
words_set = load_english_words()

# Combine them into a single set for segmentation
segmentation_words = words_set.union(set(afinn.keys()))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    input_text = request.form['text']
    

    #analyse route
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])', input_text) if s.strip() != ""]

    processed_sentences = []
    for sentence in sentences:
        if sentence.strip() != "":
            clean_sentence = sentence.replace(".", "").replace("!", "").replace("?", "")
            if " " in clean_sentence:
                processed_sentences.append(clean_sentence.strip())
            else:
                segmented_results = segment(clean_sentence.lower(), segmentation_words)
                processed_sentences.append(segmented_results.strip())
    
    sentence_scores = [] 
    for sentence in processed_sentences:
        if sentence.strip() != "":
            score = sentiment_score(sentence, afinn)
            sentence_scores.append([sentence, score]) 
    
    score = sum(sc for _, sc in sentence_scores)


    windows, most_positive, most_negative = sliding_window(processed_sentences, afinn, window_size=3)
    _,_,_,most_positive_sentence, most_negative_sentence = get_most_positive_negative_sentence(sentence_scores)
    arb_pos, arb_neg = analyze_arbitrary_segments(processed_sentences, afinn)

    if score>0:
        label = "Positive"
    elif score<0:
        label = "Negative"
    else:
        label = "Neutral"
    return render_template('analysis.html', 
                           score=score, 
                           review=input_text, 
                           segmented_sentences=processed_sentences,
                           label=label,
                           most_positive_sentence=most_positive_sentence,
                           most_negative_sentence=most_negative_sentence,
                           most_positive=most_positive,
                           most_negative=most_negative,
                           arb_pos=arb_pos,
                           arb_neg=arb_neg                           
                           )

if __name__ == '__main__':
    app.run(debug=True)