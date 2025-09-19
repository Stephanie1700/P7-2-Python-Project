from flask import Flask, render_template, request
from app import load_afinn_dict, sentiment_score

app = Flask(__name__)

afinn = load_afinn_dict()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    input_text = request.form['review']
    score = sentiment_score(input_text, afinn)
    return render_template('index.html', score=score, review=input_text)

if __name__ == '__main__':
    app.run(debug=True)