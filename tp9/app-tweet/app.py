import os
import sys
from flask import Flask, request, render_template, redirect
from joblib import load
		
app = Flask(__name__)

tweet=""
clf=load('algo.joblib')

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        global tweet 
        tweet = request.form['tweet']
        return redirect(request.url+'results')
    return render_template('home.html')

# 0 - hate speech 1 - offensive language 2 - neither
def return_probas():
    global clf
    global tweet
    probas = clf.predict_proba([tweet.lower()]) 
    probas_dict = {
                'hate speech':str(round(probas[0][0]*100, 2)),
                'offensive language':str(round(probas[0][1]*100, 2)),
                'neither':str(round(probas[0][2]*100, 2))
                }
    return probas_dict


@app.route('/results')
def results():
    return render_template('results.html', tweet=tweet, probas=return_probas())
		
if __name__ == '__main__':
    app.run(debug=True)