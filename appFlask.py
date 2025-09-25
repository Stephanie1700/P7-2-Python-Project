from flask import Flask, render_template, request
from app import load_afinn_dict, sentiment_score, sliding_window
import re

app = Flask(__name__, static_folder='static', template_folder='templates')

afinn = load_afinn_dict()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    input_text = request.form['text']
    score = sentiment_score(input_text, afinn)

    #analyse route
    sentences = re.split(r'(?<=[.!?]) +', input_text)
    windows, most_positive, most_negative = sliding_window(sentences, afinn, window_size=3)

    if score>0:
        label = "Positive"
    elif score<0:
        label = "Negative"
    else:
        label = "Neutral"
    return render_template('analysis.html', 
                           score=score, 
                           review=input_text, 
                           label=label,
                           most_positive=most_positive,
                           most_negative=most_negative)

if __name__ == '__main__':
    app.run(debug=True)