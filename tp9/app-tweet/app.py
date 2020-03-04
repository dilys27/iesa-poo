import json
import os
from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
from joblib import load
		
app = Flask(__name__)

#CORS(app)

tweet=""
clf=load('algo.joblib')

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        tweet = request.form['tweet']
        return redirect(request.url+'results')
    return render_template('home.html')

# 0 - hate speech 1 - offensive language 2 - neither
def return_probas():
  probas = clf.predict_proba([tweet.lower()]) 
  print(tweet)
  print(probas)
  probas_dict = {
                'hate speech':probas[0][0],
                'offensive language':probas[0][1],
                'neither':probas[0][2]
                }
  return jsonify(probas_dict)


@app.route('/results')
def results():
    return render_template('results.html', tweet=tweet, probas=return_probas())
		
if __name__ == '__main__':
    app.run(debug=True)